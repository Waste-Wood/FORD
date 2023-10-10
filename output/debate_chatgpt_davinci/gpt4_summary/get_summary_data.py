import jsonlines


# tasks = ["ecare", 'piqa', 'strategyqa', 'socialiqa', 'copa', 'csqa']
tasks = ['anli']

def get_data(task):
    examples = []
    for i in range(1, 4):
        model = "chatgpt" if i % 2 == 1 else "davinci"
        examples += [d for d in jsonlines.open(f"../round{i}_{model}/{task}_agreed.jsonl", 'r')]
    examples += [d for d in jsonlines.open(f"../round4_davinci/{task}_agreed.jsonl", 'r')]
    examples += [d for d in jsonlines.open(f"../round4_davinci/{task}_candidate.jsonl", 'r')]
    return examples


for task in tasks:
    instances = get_data(task)
    fo = jsonlines.open(f"{task}.jsonl", 'w')
    fo.write_all(instances)
    print('[Task] {}'.format(task))
    print('[Num]: {}'.format(len(instances)))


