
task="ecare"

python3 debate_chatgpt.py \
  --candidate "./output/debate_chatgpt_davinci/round0" \
  --dataset $task \
  --api "" \
  --model "gpt-3.5-turbo" \
  --mode "debate" \
  --output_dir './output/debate_chatgpt_davinci/round1_chatgpt' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \


python3 debate_davinci.py \
  --candidate "./output/debate_chatgpt_davinci/round1_chatgpt" \
  --dataset $task \
  --api "" \
  --model "text-davinci-003" \
  --mode "debate" \
  --output_dir './output/debate_chatgpt_davinci/round2_davinci' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \


python3 debate_chatgpt.py \
  --candidate "./output/debate_chatgpt_davinci/round2_davinci" \
  --dataset $task \
  --api "" \
  --model "gpt-3.5-turbo" \
  --mode "debate" \
  --output_dir './output/debate_chatgpt_davinci/round3_chatgpt' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \


python3 debate_davinci.py \
  --candidate "./output/debate_chatgpt_davinci/round3_chatgpt" \
  --dataset $task \
  --api "" \
  --model "text-davinci-003" \
  --mode "debate" \
  --output_dir './output/debate_chatgpt_davinci/round4_davinci' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \


python3 debate_chatgpt.py \
  --candidate "./output/debate_chatgpt_davinci/round4_davinci" \
  --dataset $task \
  --api "" \
  --model "gpt-3.5-turbo" \
  --mode "debate" \
  --output_dir './output/debate_chatgpt_davinci/round5_chatgpt' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \


python3 debate_davinci.py \
  --candidate "./output/debate_chatgpt_davinci/round5_chatgpt" \
  --dataset $task \
  --api "" \
  --model "text-davinci-003" \
  --mode "debate" \
  --output_dir './output/debate_chatgpt_davinci/round6_davinci' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

