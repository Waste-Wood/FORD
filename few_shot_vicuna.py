# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the GNU General Public License version 3.

from typing import Tuple
import os
import sys
import pdb
import torch
import fire
import time
import json
from pathlib import Path
from fairscale.nn.model_parallel.initialize import initialize_model_parallel
from llama import ModelArgs, Transformer, Tokenizer, LLaMA
from argparse import ArgumentParser
import tqdm
from tools import DynamicDataset, read_jsonlines
import jsonlines
from torch.utils.data import DataLoader
from argparse import ArgumentParser



def define_hps():
    parser = ArgumentParser(description='LLaMA')

    parser.add_argument('--mode', type=str, default='few_shot')
    parser.add_argument('--task', type=str, default='copa')
    
    parser.add_argument('--data_dir', type=str, default='./data/jsonlines')
    parser.add_argument('--checkpoint', type=str, default='/ssd1/huggingface_transformers/llama/')
    parser.add_argument('--model_size', type=str, default='7B')
    parser.add_argument('--tokenizer', type=str, default='/ssd1/huggingface_transformers/llama/tokenizer.model')
    parser.add_argument('--prompt_dir', type=str, default='./data/prompts')
    parser.add_argument('--log_dir', type=str, default='./output/logger')
    parser.add_argument('--log_name', type=str, default='')
    parser.add_argument('--output_dir', type=str, default='./output/few_shot_LLaMA')
    
    parser.add_argument('--max_seq_len', type=int, default=650)
    parser.add_argument('--max_tokens', type=int, default=20)
    parser.add_argument('--batch_size', type=int, default=10)
    parser.add_argument('--temperature', type=float, default=1.0)
    parser.add_argument('--top_p', type=float, default=1.0)

    hps = parser.parse_args()

    return hps


def setup_model_parallel() -> Tuple[int, int]:
    local_rank = int(os.environ.get("LOCAL_RANK", -1))
    world_size = int(os.environ.get("WORLD_SIZE", -1))

    torch.distributed.init_process_group("nccl")
    initialize_model_parallel(world_size)
    torch.cuda.set_device(local_rank)

    # seed must be the same in all processes
    torch.manual_seed(1)
    return local_rank, world_size


def load(
    ckpt_dir: str,
    tokenizer_path: str,
    local_rank: int,
    world_size: int,
    max_seq_len: int,
    max_batch_size: int,
) -> LLaMA:
    start_time = time.time()
    checkpoints = sorted(Path(ckpt_dir).glob("*.pth"))
    assert world_size == len(
        checkpoints
    ), f"Loading a checkpoint for MP={len(checkpoints)} but world size is {world_size}"
    ckpt_path = checkpoints[local_rank]
    print("Loading")
    checkpoint = torch.load(ckpt_path, map_location="cpu")
    with open(Path(ckpt_dir) / "params.json", "r") as f:
        params = json.loads(f.read())

    model_args: ModelArgs = ModelArgs(
        max_seq_len=max_seq_len, max_batch_size=max_batch_size, **params
    )
    tokenizer = Tokenizer(model_path=tokenizer_path)
    model_args.vocab_size = tokenizer.n_words
    torch.set_default_tensor_type(torch.cuda.HalfTensor)
    model = Transformer(model_args)
    torch.set_default_tensor_type(torch.FloatTensor)
    model.load_state_dict(checkpoint, strict=False)

    generator = LLaMA(model, tokenizer)
    print(f"Loaded in {time.time() - start_time:.2f} seconds")
    return generator


def main():
    parser = ArgumentParser()
    parser.add_argument("--model_size", type=str, default="vicuna_13B_2")
    parser.add_argument("--task", type=str, default="piqa")
    parser.add_argument("--output_dir", type=str, default="./output/vicuna")
    opt = parser.parse_args()

    checkpoint = "/ssd1/huggingface_transformers/llama/"
    # model_size = 'vicuna_13B_2'
    model_size = opt.model_size
    # task = 'anli'
    task = opt.task
    batch_size = 24
    max_seq_len = 1240
    data_dir = "./data/jsonlines"
    prompt_dir = "./data/prompts"
    # output_dir = "./output/vicuna"
    output_dir = opt.output_dir
    max_tokens = 256
    temperature = 0.0
    top_p = 1

    print(f"[Model]: {model_size}")
    print(f"[Task]: {task}")

    local_rank, world_size = setup_model_parallel()
    if local_rank > 0:
        sys.stdout = open(os.devnull, "w")

    generator = load(os.path.join(checkpoint, model_size), os.path.join(checkpoint, 'tokenizer.model'), local_rank, world_size, max_seq_len, batch_size)

    data = read_jsonlines(os.path.join(data_dir, '{}.jsonl'.format(task)))
    DATA = DynamicDataset(*data)
    dataloader = DataLoader(DATA, batch_size=batch_size)

    if task in ['singleeq', 'multiarith', 'svamp', 'addsub', 'gsm8k']:
        prompt = open(os.path.join(prompt_dir, 'manual_cot_{}.txt'.format('mwp')), 'r').read()
    else:
        prompt = open(os.path.join(prompt_dir, 'manual_cot_{}.txt'.format(task)), 'r').read()

    if not os.path.exists(os.path.join(output_dir)):
        os.makedirs(os.path.join(output_dir))

    bar = tqdm.trange(len(dataloader))
    fo = jsonlines.open(os.path.join(output_dir, '{}.jsonl'.format(task)), 'w')
    bar.set_postfix()
    for batch, _ in zip(dataloader, bar):
        questions, options, answers, responses = batch
        if task != 'strategyqa':
            overall_prompt = ["{}\n\nQ: {} Answer Choices: {}\nA:".format(prompt, q, o) for q, o in zip(questions, options)]
        else:
            overall_prompt = ["{}\n\nQ: {}\nA:".format(prompt, q) for q in questions]
        
        results = generator.generate(overall_prompt, max_gen_len=max_tokens, temperature=temperature, top_p=top_p)

        for r, q, o, a, _, p in zip(results, *batch, overall_prompt):
            # pdb.set_trace()
            r = r[len(p):].strip().split('\n\n')[0]
            if isinstance(a, torch.Tensor):
                fo.write({'Q': q, 'A': a.item(), 'O': o, 'R': {'text': r}})
            else:
                fo.write({'Q': q, 'A': a, 'O': o, 'R': {'text': r}})

    fo.close()
    del generator

if __name__ == "__main__":
    fire.Fire(main)