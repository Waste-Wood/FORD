import jsonlines
import sys

task = sys.argv[1]

size = {'anli': 1507, 'csqa': 1221, 'copa': 500, 'ecare': 2122, 'socialiqa': 1935, 'piqa': 1838, 'strategyqa': 2290}

incon = 0
for i in range(0, 7):
    model = "davinci" if i % 2 == 1 else "chatgpt"
    if i == 0:
        data = [d for d in jsonlines.open(f"./round{i}/{task}_candidate.jsonl")]
    else:
        data = [d for d in jsonlines.open(f"./round{i}_{model}/{task}_candidate.jsonl")]
    
    incon = len(data)
    print(f"Round{i}: {incon/size[task]*100}")




