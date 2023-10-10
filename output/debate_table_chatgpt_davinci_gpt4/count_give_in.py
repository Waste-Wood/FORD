import jsonlines
import sys
import os


task = sys.argv[1]

modelA_givein_num, modelB_givein_num, modelC_givein_num = 0, 0, 0
givein_num = 0

for i in range(1, 10):
    if i % 3 == 1:
        model = 'chatgpt'
    elif i % 3 == 2:
        model = 'davinci'
    else:
        model = 'gpt4'
    
    # data = [d for d in jsonlines.open(f'./round{i}_{model}/{task}_agreed.jsonl', 'r') if len(set(d['P'][2:]))==3]
    data = [d for d in jsonlines.open(f'./round{i}_{model}/{task}_agreed.jsonl', 'r')]
    givein_num += len(data)

    if model == 'chatgpt':
        modelB_givein_num += len(data)
        # if i <= 1:
        #     modelC_givein_num += len([d for d in data if d['P'][-1]==d['P'][4]])
    elif model == 'davinci':
        modelC_givein_num += len(data)
        # if i <= 1:
        #     modelA_givein_num += len([d for d in data if d['P'][-1] == d['P'][2]])
    else:
        modelA_givein_num += len(data)
        # if i <= 1:
        #     modelB_givein_num += len([d for d in data if d['P'][-1] == d['P'][3]])

givein_num = modelC_givein_num + modelA_givein_num + modelB_givein_num
print(f'[Given in Num]: {givein_num}')
print(f'[GPT-3.5 Give in Num]: {modelA_givein_num}')
print(f'[Davinci Give in Num]: {modelB_givein_num}')
print(f'[GPT-4 Give in Num]: {modelC_givein_num}')

print(f'[GPT-3.5 Give in Rate]: {modelA_givein_num/givein_num}')
print(f'[Davinci Give in Rate]: {modelB_givein_num/givein_num}')
print(f'[GPT-4 Give in Rate]: {modelC_givein_num/givein_num}')


