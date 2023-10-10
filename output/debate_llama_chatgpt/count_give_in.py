import jsonlines
import sys
import os


task = sys.argv[1]

modelA_givein_num, modelB_givein_num = 0, 0
givein_num = 0

for i in range(1, 7):
    model = 'llama' if i % 2 == 1 else 'chatgpt'
    data = [d for d in jsonlines.open(f'./round{i}_{model}/{task}_agreed.jsonl', 'r')]
    givein_num += len(data)

    if model == 'chatgpt':
        modelA_givein_num += len(data)
    else:
        modelB_givein_num += len(data)

print(f'[Given in Num]: {givein_num}')
print(f'[ChatGPT Give in Num]: {modelA_givein_num}')
print(f'[Davinci Give in Num]: {modelB_givein_num}')

print(f'[ChatGPT Give in Rate]: {modelA_givein_num/givein_num}')
print(f'[Davinci Give in Rate]: {modelB_givein_num/givein_num}')


