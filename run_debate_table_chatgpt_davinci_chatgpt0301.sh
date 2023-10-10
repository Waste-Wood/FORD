
task="ecare"

python3 debate_table.py \
  --candidate "./output/debate_table_chatgpt_davinci_chatgpt0301/round0" \
  --dataset $task \
  --api "" \
  --model "gpt-3.5-turbo" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_chatgpt0301/round1_chatgpt' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table.py \
  --candidate "./output/debate_table_chatgpt_davinci_chatgpt0301/round1_chatgpt" \
  --dataset $task \
  --api "" \
  --model "text-davinci-003" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_chatgpt0301/round2_davinci' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table.py \
  --candidate "./output/debate_table_chatgpt_davinci_chatgpt0301/round2_davinci" \
  --dataset $task \
  --api "" \
  --model "gpt-3.5-turbo-0301" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_chatgpt0301/round3_chatgpt0301' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table.py \
  --candidate "./output/debate_table_chatgpt_davinci_chatgpt0301/round3_chatgpt0301" \
  --dataset $task \
  --api "" \
  --model "gpt-3.5-turbo" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_chatgpt0301/round4_chatgpt' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table.py \
  --candidate "./output/debate_table_chatgpt_davinci_chatgpt0301/round4_chatgpt" \
  --dataset $task \
  --api "" \
  --model "text-davinci-003" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_chatgpt0301/round5_davinci' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table.py \
  --candidate "./output/debate_table_chatgpt_davinci_chatgpt0301/round5_davinci" \
  --dataset $task \
  --api "" \
  --model "gpt-3.5-turbo-0301" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_chatgpt0301/round6_chatgpt0301' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table.py \
  --candidate "./output/debate_table_chatgpt_davinci_chatgpt0301/round6_chatgpt0301" \
  --dataset $task \
  --api "" \
  --model "gpt-3.5-turbo" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_chatgpt0301/round7_chatgpt' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table.py \
  --candidate "./output/debate_table_chatgpt_davinci_chatgpt0301/round7_chatgpt" \
  --dataset $task \
  --api "" \
  --model "text-davinci-003" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_chatgpt0301/round8_davinci' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \

python3 debate_table.py \
  --candidate "./output/debate_table_chatgpt_davinci_chatgpt0301/round8_davinci" \
  --dataset $task \
  --api "" \
  --model "gpt-3.5-turbo-0301" \
  --mode "debate" \
  --output_dir './output/debate_table_chatgpt_davinci_chatgpt0301/round9_chatgpt0301' \
  --log_dir "./logger" \
  --num_sequences 1 \
  --max_tokens 512 \
  --temperature 0.0 \




