import json
import jsonlines
import sys
import re


# def get_count(data):
#     count = 0
#     for d in data:
#         answer = re.findall(pattern, d['A'])[0]
#         if d['P'][-1] == answer:
#             count += 1
#         else:
#             continue
#     return count

def get_count(data):
    count = 0
    for d in data:
        answer = re.findall(pattern, d['A'])[0]
        # if d['P'][-1] == answer:
        candidates = [p for p in d["P"] if p != "None"]
        if len(candidates) == 0:
            candidates = d['P'][2:]
        if max(candidates, key=candidates.count) == answer:
            count += 1
        else:
            continue
    return count


task = sys.argv[1]
pattern = re.compile("(A|B|C|D|E|yes|no)")

init_agreed = [d for d in jsonlines.open(f'./round0/{task}_agreed2.jsonl', 'r')]
init_candidate = [d for d in jsonlines.open(f'./round0/{task}_candidate2.jsonl', 'r')]

right_count = 0
number = len(init_agreed) + len(init_candidate)
right_count += get_count(init_agreed)

print(f"[Number] {number}")
print(f"[Round0] {right_count}/{number} = {right_count/number}")

for i in range(1, 7):
    model = 'chatgpt' if i % 2 == 1 else 'davinci'
    agreed = [d for d in jsonlines.open(f'./round{i}_{model}/{task}_agreed3.jsonl', 'r')]
    right_count += get_count(agreed)
    print(f"[Round{i}] {right_count}/{number} = {right_count/number}")

final_candidate = [d for d in jsonlines.open(f'./round6_davinci/{task}_candidate3.jsonl', 'r')]
for d in final_candidate:
    answer = re.findall(pattern, d['A'])[0]
    # candidates = d['P'][2:]
    candidates = [p for p in d["P"] if p != "None"]
    if len(candidates) == 0:
        candidates = d['P'][2:]
    prediction = max(candidates, key=candidates.count)
    if prediction == answer:
        right_count += 1
    else:
        continue

print(f"[Round7] {right_count}/{number} = {right_count/number}")



