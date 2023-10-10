import json
import jsonlines
import sys


task = sys.argv[1]

data = [d for d in jsonlines.open(f'{task}_summary.jsonl', 'r')]

base = {'anli': 1042, 'csqa': 833, 'copa': 469, 'ecare': 1527, 'socialiqa': 1213, 'piqa': 1260, 'strategyqa': 1331}
size = {'anli': 1507, 'csqa': 1221, 'copa': 500, 'ecare': 2122, 'socialiqa': 1935, 'piqa': 1838, 'strategyqa': 2290}

data1 = [d for d in jsonlines.open(f'../round1_chatgpt/{task}_agreed.jsonl', 'r')]
data2 = [d for d in jsonlines.open(f'../round2_davinci/{task}_agreed.jsonl', 'r')]
data3 = [d for d in jsonlines.open(f'../round3_chatgpt/{task}_agreed.jsonl', 'r')]
data4 = [d for d in jsonlines.open(f'../round4_davinci/{task}_agreed.jsonl', 'r')]
data5 = [d for d in jsonlines.open(f'../round5_chatgpt/{task}_agreed.jsonl', 'r')]
data6 = [d for d in jsonlines.open(f'../round6_davinci/{task}_agreed.jsonl', 'r')] + [d for d in jsonlines.open(f'../round6_davinci/{task}_candidate.jsonl', 'r')]


data1 = data[:len(data1)]
data = data[len(data1):]

data2 = data[:len(data2)]
data = data[len(data2):]

data3 = data[:len(data3)]
data = data[len(data3):]

data4 = data[:len(data4)]
data = data[len(data4):]

data5 = data[:len(data5)]
data = data[len(data5):]

data6 = data[:len(data6)]
data = data[len(data6):]

assert len(data) == 0

data1 = [d for d in data1 if d['SP']['Answer']==d['SP']['Summary']]
data2 = [d for d in data2 if d['SP']['Answer']==d['SP']['Summary']] + data1
data3 = [d for d in data3 if d['SP']['Answer']==d['SP']['Summary']] + data2
data4 = [d for d in data4 if d['SP']['Answer']==d['SP']['Summary']] + data3
data5 = [d for d in data5 if d['SP']['Answer']==d['SP']['Summary']] + data4
data6 = [d for d in data6 if d['SP']['Answer']==d['SP']['Summary']] + data5


print(f'[Round0] {base[task]}: {base[task]/size[task]}')
print(f'[Round1] {base[task]+len(data1)}: {(base[task]+len(data1))/size[task]}')
print(f'[Round2] {base[task]+len(data2)}: {(base[task]+len(data2))/size[task]}')
print(f'[Round3] {base[task]+len(data3)}: {(base[task]+len(data3))/size[task]}')
print(f'[Round4] {base[task]+len(data4)}: {(base[task]+len(data4))/size[task]}')
print(f'[Round5] {base[task]+len(data5)}: {(base[task]+len(data5))/size[task]}')
print(f'[Round6] {base[task]+len(data6)}: {(base[task]+len(data6))/size[task]}')














