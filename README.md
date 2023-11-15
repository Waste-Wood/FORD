# Introduction
This repo contain the code and data of the paper: [Examining Inter-Consistency of Large Language Models Collaboration:
An In-depth Analysis via Debate](https://arxiv.org/abs/2305.11595).

To examine whether LLMs can collaborate to ultimately achieve a consensus for the shared goal and whether LLMs easily change their viewpoints, we introduce a Formal Debate framework (FORD) With FORD, we conduct a three-stage debate aligned with real-world scenarios: fair debate, mismatched debate, and roundtable debate. More details can refer to our paper.

# Data Structure
```shell
-data # storing data including datasets and prompts
  -jsonlines # formatted task data
  -prompts # prompts for few-shot cot seetings
  
-logger # storing all logs when conducting debates

-output # storing all outputs and some codes
  -albation_study # outputs and codes for ablation study
  -chatgpt # zero-shot outputs of gpt-3.5-turbo
  -chatpgt0301 # zero-shot outputs of gpt-3.5-turbo-0301
  -dacinvi # few-shot cot outputs of text-davinci-003
  -gpt4 # zero-shot outputs of gpt-4
  -LLaMA # few-shot cot outputs of LLaMA-13B
  -vicuna # few-shot cot outputs of Vicuna-13B
  -debate_chatgpt_chatgpt0301 # outputs of debate between gpt-3.5-turbo and gpt-3.5-turbo-0301
  -debate_chatgpt_davinci # outputs of debate between gpt-3.5-turbo and text-davinci-003
  -debate_chatgpt_gpt4 # outputs of debate between gpt-3.5-turbo and gpt-4
  -debate_llama_chatgpt # outputs of debate between LLaMA-13B and gpt-3.5-turbo
  -debate_llama_vicuna # outputs of debate between LLaMA-13B and vicuna-13B
  -debate_table_chatgpt_davinvi_chatgpt0301 # outputs of debate among gpt-3.5-turbo, text-davinci-003, and gpt-3.5-turbo-0301
  -debate_table_chatgpt_davinci_gpt4 # outputs of debate among gpt-3.5-turbo, text-davinci-003, and gpt-4

-run_debate_chatgpt_davinci.sh # script for debate between gpt-3.5-turbo and text-davinci-003
-run_debate_chatgpt_llama.sh # script for debate between gpt-3.5-turbo and LLaMA-13B
-run_debate_llama_vicuna.sh # script for debate between LLaMA-13B and Vicuna-13B
-run_debate_table_chatgpt_davinci_chatgpt0301.sh # script for debate among gpt-3.5-turbo, text-davinci-003, and gpt-3.5-turbo-0301
-run_debate_table_chatgpt_davinci_gpt4.sh # script for debate among gpt-3.5-turbo, text-davinci-003, and gpt-4
-run_few_shot_cot.sh # script for conducting few-shot-cot on text-davinci-003
-run_few_shot_vicuna_llama.sh # script for conducting few-shot-cot on LLaMA-13B or Vicuna-13B
-run_zero_shot_chatgpt.sh # script for conducting zero-shot reasoning with gpt-3.5-turbo, gpt-3.5-turbo-0301, or gpt-4
```

# Citation
If you want to cite our paper, please use the following bibtex:
```shell
@article{xiong2023examining,
  title={Examining the Inter-Consistency of Large Language Models: An In-depth Analysis via Debate},
  author={Xiong, Kai and Ding, Xiao and Cao, Yixin and Liu, Ting and Qin, Bing},
  journal={arXiv e-prints},
  pages={arXiv--2305},
  year={2023}
}
```



