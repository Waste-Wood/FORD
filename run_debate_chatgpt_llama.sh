torchrun --nproc_per_node=4 debate_llama_vicuna.py \
  --candidate "./output/debate_vicuna_chatgpt/round0" \
  --dataset "piqa" \
  --model_size "vicuna_13B" \
  --output_dir "./output/debate_vicuna_chatgpt/test" \
  --max_seq_len 1224 \
  --max_tokens 256 \
  --batch_size 24


 python3 debate_chatgpt.py \
   --candidate "./output/debate_vicuna_chatgpt/round1_vicuna" \
   --dataset "piqa" \
   --api "" \
   --model "gpt-3.5-turbo" \
   --mode "debate" \
   --output_dir './output/debate_vicuna_chatgpt/round2_chatgpt' \
   --log_dir "./logger" \
   --max_tokens 512 \
   --temperature 0.0


 torchrun --nproc_per_node=4 debate_llama_vicuna.py \
   --candidate "./output/debate_vicuna_chatgpt/round2_chatgpt" \
   --dataset "piqa" \
   --model_size "vicuna_13B" \
   --output_dir "./output/debate_vicuna_chatgpt/round3_vicuna" \
   --max_seq_len 1224 \
   --max_tokens 256 \
   --batch_size 24


 python3 debate_chatgpt.py \
   --candidate "./output/debate_vicuna_chatgpt/round3_vicuna" \
   --dataset "piqa" \
   --api "" \
   --model "gpt-3.5-turbo" \
   --mode "debate" \
   --output_dir './output/debate_vicuna_chatgpt/round4_chatgpt' \
   --log_dir "./logger" \
   --max_tokens 512 \
   --temperature 0.0


 torchrun --nproc_per_node=4 debate_llama_vicuna.py \
   --candidate "./output/debate_vicuna_chatgpt/round4_chatgpt" \
   --dataset "piqa" \
   --model_size "vicuna_13B" \
   --output_dir "./output/debate_vicuna_chatgpt/round5_vicuna" \
   --max_seq_len 1224 \
   --max_tokens 256 \
   --batch_size 24


 python3 debate_chatgpt.py \
   --candidate "./output/debate_vicuna_chatgpt/round5_vicuna" \
   --dataset "piqa" \
   --api "" \
   --model "gpt-3.5-turbo" \
   --mode "debate" \
   --output_dir './output/debate_vicuna_chatgpt/round6_chatgpt' \
   --log_dir "./logger" \
   --max_tokens 512 \
   --temperature 0.0
