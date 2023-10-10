
task="ecare"

python3 debate_table \
  --candidate "./output/debate_table_chatgpt_davinci_gpt4/round0" \
  --dataset $task \
  --api "" \
  --model "gpt-3.5-turbo" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_gpt4/round1_chatgpt' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table \
  --candidate "./output/debate_table_chatgpt_davinci_gpt4/round1_chatgpt" \
  --dataset $task \
  --api "" \
  --model "text-davinci-003" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_gpt4/round2_davinci' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table \
  --candidate "./output/debate_table_chatgpt_davinci_gpt4/round2_davinci" \
  --dataset $task \
  --api "" \
  --model "gpt-4" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_gpt4/round3_gpt4' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table \
  --candidate "./output/debate_table_chatgpt_davinci_gpt4/round3_gpt4" \
  --dataset $task \
  --api "" \
  --model "gpt-3.5-turbo" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_gpt4/round4_chatgpt' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table \
  --candidate "./output/debate_table_chatgpt_davinci_gpt4/round4_chatgpt" \
  --dataset $task \
  --api "" \
  --model "text-davinci-003" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_gpt4/round5_davinci' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table \
  --candidate "./output/debate_table_chatgpt_davinci_gpt4/round5_davinci" \
  --dataset $task \
  --api "" \
  --model "gpt-4" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_gpt4/round6_gpt4' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table \
  --candidate "./output/debate_table_chatgpt_davinci_gpt4/round6_gpt4" \
  --dataset $task \
  --api "" \
  --model "gpt-3.5-turbo" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_gpt4/round7_chatgpt' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table \
  --candidate "./output/debate_table_chatgpt_davinci_gpt4/round7_chatgpt" \
  --dataset $task \
  --api "" \
  --model "text-davinci-003" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_gpt4/round8_davinci' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table \
  --candidate "./output/debate_table_chatgpt_davinci_gpt4/round8_davinci" \
  --dataset $task \
  --api "" \
  --model "gpt-4" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_gpt4/round9_gpt4' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \




