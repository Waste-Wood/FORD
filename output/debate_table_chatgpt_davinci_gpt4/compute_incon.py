import jsonlines
import sys

task = sys.argv[1]

size = {'anli': 1507, 'csqa': 1221, 'copa': 500, 'ecare': 2122, 'socialiqa': 1935, 'piqa2': 1838, 'strategyqa': 2290}

incon = 0
for i in range(0, 10):
    if i % 3 == 1:
        model = 'chatgpt'
    elif i % 3 == 2:
        model = 'davinci'
    else:
        model = 'gpt4'
    if i == 0:
        data = [d for d in jsonlines.open(f"./round{i}/{task}_candidate.jsonl")]
    else:
        data = [d for d in jsonlines.open(f"./round{i}_{model}/{task}_candidate.jsonl")]
    
    incon = len(data)
    print(f"Round{i}: {incon/size[task]*100}")




