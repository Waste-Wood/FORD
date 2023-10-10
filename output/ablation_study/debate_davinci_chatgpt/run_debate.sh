
python3 debate_davinci.py \
  --candidate "./round0" \
  --dataset "piqa" \
  --api "" \
  --model "text-davinci-003" \
  --mode "debate" \
  --output_dir './round1_davinci' \
  --log_dir "../../../logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0



python3 debate_chatgpt.py \
  --candidate "./round1_davinci" \
  --dataset "piqa" \
  --api "" \
  --model "gpt-3.5-turbo" \
  --mode "debate" \
  --output_dir './round2_chatgpt' \
  --log_dir "../../../logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0


python3 debate_davinci.py \
  --candidate "./round2_chatgpt" \
  --dataset "piqa" \
  --api "" \
  --model "text-davinci-003" \
  --mode "debate" \
  --output_dir './round3_davinci' \
  --log_dir "../../../logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0



python3 debate_chatgpt.py \
  --candidate "./round3_davinci" \
  --dataset "piqa" \
  --api "" \
  --model "gpt-3.5-turbo" \
  --mode "debate" \
  --output_dir './round4_chatgpt' \
  --log_dir "../../../logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0



python3 debate_davinci.py \
  --candidate "./round4_chatgpt" \
  --dataset "piqa" \
  --api "" \
  --model "text-davinci-003" \
  --mode "debate" \
  --output_dir './round5_davinci' \
  --log_dir "../../../logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0



python3 debate_chatgpt.py \
  --candidate "./round5_davinci" \
  --dataset "piqa" \
  --api "" \
  --model "gpt-3.5-turbo" \
  --mode "debate" \
  --output_dir './round6_chatgpt' \
  --log_dir "../../../logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0


