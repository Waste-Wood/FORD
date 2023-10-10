
python3 debate_chatgpt.py \
  --candidate "./round0" \
  --dataset "ecare" \
  --api "" \
  --model "gpt-3.5-turbo-0301" \
  --mode "debate" \
  --output_dir './round1_chatgpt0301' \
  --log_dir "../../../logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0


python3 debate_chatgpt.py \
  --candidate "./round1_chatgpt0301" \
  --dataset "ecare" \
  --api "" \
  --model "gpt-3.5-turbo" \
  --mode "debate" \
  --output_dir './round2_chatgpt' \
  --log_dir "../../../logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0


python3 debate_chatgpt.py \
  --candidate "./round2_chatgpt" \
  --dataset "ecare" \
  --api "" \
  --model "gpt-3.5-turbo-0301" \
  --mode "debate" \
  --output_dir './round3_chatgpt0301' \
  --log_dir "../../../logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0


python3 debate_chatgpt.py \
  --candidate "./round3_chatgpt0301" \
  --dataset "ecare" \
  --api "" \
  --model "gpt-3.5-turbo" \
  --mode "debate" \
  --output_dir './round4_chatgpt' \
  --log_dir "../../../logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0


python3 debate_chatgpt.py \
  --candidate "./round4_chatgpt" \
  --dataset "ecare" \
  --api "" \
  --model "gpt-3.5-turbo-0301" \
  --mode "debate" \
  --output_dir './round5_chatgpt0301' \
  --log_dir "../../../logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0


python3 debate_chatgpt.py \
  --candidate "./round5_chatgpt0301" \
  --dataset "ecare" \
  --api "" \
  --model "gpt-3.5-turbo" \
  --mode "debate" \
  --output_dir './round6_chatgpt' \
  --log_dir "../../../logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0

