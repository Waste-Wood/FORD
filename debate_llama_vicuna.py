import pdb
import time
from argparse import ArgumentParser
from tools import read_jsonlines, define_logger
import jsonlines
from tqdm import tqdm
import os
import torch
import re
from fairscale.nn.model_parallel.initialize import initialize_model_parallel
from typing import Tuple
from llama import ModelArgs, Transformer, Tokenizer, LLaMA
from pathlib import Path
import json
from tools import DynamicDataset, collate_fn
from torch.utils.data import DataLoader



def get_prediction_explanation(task, response):
    text = response['choices'][0]['text'].strip()
    try:
        prediction, explanation = text.split('Explanation: ')
        predictions = re.findall(pattern, prediction.replace("Answer", 'answer'))
        if len(prediction) >= 1:
            prediction = predictions[0]
        else:
            prediction = "None"
    except:
        explanation = text.strip()
        prediction = "None"
    if task == 'strategyqa':
        prediction = prediction.lower()
    return prediction, explanation


def load(ckpt_dir: str, tokenizer_path: str, local_rank: int, world_size: int, max_seq_len: int, max_batch_size: int):
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

    model_args: ModelArgs = ModelArgs(max_seq_len=max_seq_len, max_batch_size=max_batch_size, **params)
    tokenizer = Tokenizer(model_path=tokenizer_path)
    model_args.vocab_size = tokenizer.n_words
    torch.set_default_tensor_type(torch.cuda.HalfTensor)
    model = Transformer(model_args)
    torch.set_default_tensor_type(torch.FloatTensor)
    model.load_state_dict(checkpoint, strict=False)
    # print([model.state_dict()[key].device for key in model.state_dict().keys()])

    generator = LLaMA(model, tokenizer)
    print(f"Loaded in {time.time() - start_time:.2f} seconds")
    return generator


def setup_model_parallel() -> Tuple[int, int]:
    local_rank = int(os.environ.get("LOCAL_RANK", -1))
    world_size = int(os.environ.get("WORLD_SIZE", -1))

    torch.distributed.init_process_group("nccl")
    initialize_model_parallel(world_size)
    torch.cuda.set_device(local_rank)

    torch.manual_seed(1)
    return local_rank, world_size


def hyper_parameters():
    parser = ArgumentParser('Few-Shot')

    parser.add_argument('--candidate', type=str, default='./output/debate_llama_vicuna/round0')
    parser.add_argument('--dataset', type=str, default='anli')
    parser.add_argument('--checkpoint', type=str, default='/ssd1/huggingface_transformers/llama/')
    parser.add_argument('--model_size', type=str, default='13B_2')
    parser.add_argument('--model', type=str, default='llama')
    parser.add_argument('--mode', type=str, default='llama_vicuna')
    # parser.add_argument('--pattern', type=str, default='\(?(A|B)\)?')

    parser.add_argument('--log_dir', type=str, default='./logger')
    parser.add_argument('--log_name', type=str, default='')

    parser.add_argument('--output_dir', type=str, default='./output/debate_llama_vicuna/round1_llama')
    parser.add_argument('--max_seq_len', type=int, default=1224)
    parser.add_argument('--max_tokens', type=int, default=256)
    parser.add_argument('--batch_size', type=int, default=24)
    parser.add_argument('--temperature', type=float, default=0.0)

    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    hps = hyper_parameters()
    hps.log_name = '{}_{}.txt'.format(hps.mode, hps.dataset)

    logger = define_logger(hps)

    logger.info('[HPS]: {}'.format(hps))
    logger.info('[API Key]: {}'.format(hps.model_size))
    logger.info('[Data]: {}'.format(hps.dataset))
    logger.info('[Model]: {}'.format(hps.model))

    candidates = jsonlines.open(os.path.join(hps.candidate, '{}_candidate.jsonl'.format(hps.dataset)), 'r')
    candidates = [c for c in candidates]
    DATA = DynamicDataset(candidates)
    Loader = DataLoader(DATA, batch_size=hps.batch_size, drop_last=False, shuffle=False, collate_fn=collate_fn)

    local_rank, world_size = setup_model_parallel()
    generator = load(os.path.join(hps.checkpoint, hps.model_size), os.path.join(hps.checkpoint, 'tokenizer.model'), local_rank, world_size, hps.max_seq_len, hps.batch_size)

    fo1 = jsonlines.open(os.path.join(hps.output_dir, '{}_agreed.jsonl'.format(hps.dataset)), 'w')
    fo2 = jsonlines.open(os.path.join(hps.output_dir, '{}_candidate.jsonl'.format(hps.dataset)), 'w')
    
    system = "You are in a debate now. My opinion is not always true, you can ignore any incorrect part of my opinion. And you can refer to my opinion to revise your choice or defend your own. Use your general knowledge and understanding to read my opinion carefully and compare it with your opinion based on the question. Please remember there should and must be a more plausible answer in the choices."
    debate_instruction = "Please defend your opinion or give in to my opinion. Give your final explanation. Do not copy other's opinion."
    
    if hps.dataset == "strategyqa":
        pattern = re.compile("\(?(Yes|No|yes|no)\)?")
    elif hps.dataset == "socialiqa":
        pattern = re.compile("\(?(A|B|C)\)?")
    elif hps.dataset == "csqa":
        pattern = re.compile("\(?(A|B|C|D|E)\)?")
    else:
        assert hps.dataset in ['anli', 'copa', 'ecare', 'piqa']
        pattern = re.compile("\(?(A|B)\)?")

    candidate, summary = [], []

    for batch in tqdm(Loader):

        rounds = (len(batch[0]['R']) - 2) // 2 * 2
        role1 = "You"
        role2 = "Me"
        debate_process = ["\n".join([f"{role1 if i%2==0 else role2}: {d['content']}" for i, d in enumerate(c['R'][-rounds:])]) for c in batch]
        if hps.dataset == 'strategyqa':
            prompt = [f"{system}\n\nQuestion: {c['Q']}\nChoices: (A) yes. (B) no.\n{d} {debate_instruction}\nYou:" for c, d in zip(batch, debate_process)]
        else:    
            prompt = [f"{system}\n\nQuestion: {c['Q']}\nChoices: {c['O']}\n{d} {debate_instruction}\nYou:" for c, d in zip(batch, debate_process)]
        
        if len(candidate + summary) == 0:
            print(prompt[0])
            print(len(prompt))

        results = generator.generate(prompt, max_gen_len=hps.max_tokens, temperature=hps.temperature, top_p=1)
        results = [r[len(p):].strip().split('\n')[0] for r, p in zip(results, prompt)]

        prompt = [f"{p} {r} Therefore, the answer is (" for p, r in zip(prompt, results)]
        answers = generator.generate(prompt, max_gen_len=5, temperature=hps.temperature, top_p=1, mode="predict", task=hps.dataset)
        if hps.dataset == "strategyqa":
            answers = ["yes" if a == "A" else "no" for a in answers]

        for c, r, a, p in zip(batch, results, answers, prompt):
            c['R'].append({"role": "user", "content": r})
            c['M'].append("llama" if "vicuna" not in hps.model_size else "vicuna")
        
            prediction = a
            # predictions = re.findall(pattern, a[len(p):].strip().split('\n')[0])
            # if len(predictions) >= 1:
            #     prediction = predictions[0]
            # else:
            #     prediction = "None"
            c['P'].append(prediction)
            if c['P'][-1] == c['P'][-2]:
                summary.append(c)
                fo1.write(c)
            else:
                candidate.append(c)
                fo2.write(c)

    fo1.close()
    fo2.close()
