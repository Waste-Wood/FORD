import sys
import jsonlines

task = sys.argv[1]

size = {'ecare': 2122, 'piqa2': 1838}
init = {'ecare': 1499, 'piqa2': 1220}

print(f'[Round0] {init[task]}/{size[task]} = {init[task]/size[task]}')

for i in range(1, 10):
    if i % 3 == 1:
        model = 'chatgpt'
    elif i % 3 == 2:
        model = 'davinci'
    else:
        model = 'chatgpt0301'
    
    data = [d for d in jsonlines.open(f'./round{i}_{model}/{task}_agreed.jsonl', 'r')]

    # prediction = [[p for p in d['P'] if p in ["A", "B"]] for d in data]

    # prediction = [max(d, key=d.count) for d in prediction]
    # count = sum([1 for p, d in zip(prediction, data) if p == d['A'][1]])

    count = sum([1 if d['P'][-1] == d['A'][1] else 0 for d in data])

    init[task] += count
    print(f'[Round{i}] {init[task]}/{size[task]} = {init[task]/size[task]}')


data = [d for d in jsonlines.open(f'./round{i}_{model}/{task}_candidate.jsonl', 'r')]
prediction = [max(d['P'][2:], key=d['P'][2:].count) for d in data]
count = sum([1 for p, d in zip(prediction, data) if p == d['A'][1]])
init[task] += count
print(f'[Round13] {init[task]}/{size[task]} = {init[task]/size[task]}')



