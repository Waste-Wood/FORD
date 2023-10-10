torchrun --nproc_per_node=4 debate_llama_vicuna.py \
  --candidate "./output/debate_llama_vicuna/round0" \
  --dataset "socialiqa" \
  --model_size "13B" \
  --output_dir "./output/debate_llama_vicuna/round1_llama" \
  --max_seq_len 1224 \
  --max_tokens 256 \
  --batch_size 24


torchrun --nproc_per_node=4 debate_llama_vicuna.py \
  --candidate "./output/debate_llama_vicuna/round1_llama" \
  --dataset "socialiqa" \
  --model_size "vicuna_13B" \
  --output_dir "./output/debate_llama_vicuna/round2_vicuna" \
  --max_seq_len 1224 \
  --max_tokens 256 \
  --batch_size 24


torchrun --nproc_per_node=4 debate_llama_vicuna.py \
  --candidate "./output/debate_llama_vicuna/round2_vicuna" \
  --dataset "socialiqa" \
  --model_size "13B" \
  --output_dir "./output/debate_llama_vicuna/round3_llama" \
  --max_seq_len 1224 \
  --max_tokens 256 \
  --batch_size 24


torchrun --nproc_per_node=4 debate_llama_vicuna.py \
  --candidate "./output/debate_llama_vicuna/round3_llama" \
  --dataset "socialiqa" \
  --model_size "vicuna_13B" \
  --output_dir "./output/debate_llama_vicuna/round4_vicuna" \
  --max_seq_len 1224 \
  --max_tokens 256 \
  --batch_size 24


torchrun --nproc_per_node=4 debate_llama_vicuna.py \
  --candidate "./output/debate_llama_vicuna/round4_vicuna" \
  --dataset "socialiqa" \
  --model_size "13B" \
  --output_dir "./output/debate_llama_vicuna/round5_llama" \
  --max_seq_len 1424 \
  --max_tokens 256 \
  --batch_size 24


torchrun --nproc_per_node=4 debate_llama_vicuna.py \
  --candidate "./output/debate_llama_vicuna/round5_llama" \
  --dataset "socialiqa" \
  --model_size "vicuna_13B" \
  --output_dir "./output/debate_llama_vicuna/round6_vicuna" \
  --max_seq_len 1424 \
  --max_tokens 256 \
  --batch_size 24