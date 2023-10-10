import jsonlines
import re
import sys


def answer_cleansing(dataset, pred, answer_trigger, must_choice=False):
    # print("pred_before : " + pred)

    preds = pred.split(answer_trigger[dataset])
    answer_flag = True if len(preds) > 1 else False
    pred = preds[-1]

    if dataset in ("aqua", "csqa", "copa", "ecare", "socialiqa", 'piqa', 'anli'):
        pred = re.findall(r'A|B|C|D|E', pred)
    elif dataset in ("gsm8k", "addsub", "multiarith", "svamp", "singleeq"):
        if must_choice:
            pred = re.findall(r'A|B|C|D', pred)
        else:
            pred = pred.replace(",", "")
            pred = [s for s in re.findall(r'-?\d+\.?\d*', pred)]
    elif dataset in ("strategyqa", "coin"):
        pred = pred.lower()
        pred = re.sub("\"|\'|\n|\.|\s|\:|\,", " ", pred)
        pred = pred.split(" ")
        pred = [i for i in pred if i in ("yes", "no")]
    elif dataset == "letter":
        pred = re.sub("\"|\'|\n|\.|\s", "", pred)
        pred = [pred]
    else:
        raise ValueError("dataset is not properly defined ...")

    # If there is no candidate in list, null is set.
    if len(pred) == 0:
        pred = ""
    else:
        if answer_flag:
            # choose the first element in list ...
            pred = pred[0]
        else:
            # choose the last element in list ...
            pred = pred[-1]

    # (For arithmetic tasks) if a word ends with period, it will be omitted ...
    if pred != "":
        if pred[-1] == ".":
            pred = pred[:-1]

    # print("pred_after : " + pred)

    if dataset in ("gsm8k", "addsub", "multiarith", "svamp", "singleeq") and pred == '':
        pred = 'inf'

    return pred


def evaluate(hypotheses, references, dataset, instances):
    count = 0
    for i, h, r in zip(instances, hypotheses, references):
        if dataset in ['addsub', 'multiarith', 'gsm8k', 'singleeq', 'svamp']:
            h, r = str(h).replace(',', ''), str(r).replace(',', '')
            if abs(float(h)-float(r)) <= 1e-5:
                count += 1
            else:
                print('[Wrong]: {}'.format(i))
                continue
        elif dataset in ['aqua', 'csqa', 'copa', 'ecare', 'socialiqa', 'piqa', 'anli']:
            r = r[1]
            if h == r:
                count += 1
            else:
                print('[Wrong]: {}'.format(i))
                continue
        else:
            if h == r:
                count += 1
            else:
                print('[Wrong]: {}'.format(i))
                continue
    return count / len(references)


if __name__ == '__main__':

    # mode = 'few_shot_cot'
    # task = 'aqua'
    mode = sys.argv[1]
    task = sys.argv[2]

    choice = False
    if task in ['aqua', 'csqa', 'copa', 'ecare', 'socialiqa', 'piqa', 'anli']:
        choice = True

    if 'cot' in mode or 'LLaMA' in mode or 'curie' in mode:
        triggers = {
            "aqua": "Therefore, the answer is",
            "csqa": "Therefore, the answer is",
            "letter": "Therefore, the answer is",
            "addsub": "Therefore, the answer (arabic numerals) is",
            "gsm8k": "Therefore, the answer (arabic numerals) is",
            "multiarith": "Therefore, the answer (arabic numerals) is",
            "singleeq": "Therefore, the answer (arabic numerals) is",
            "svamp": "Therefore, the answer (arabic numerals) is",
            "coin": "Therefore, the answer (yes or no) is",
            "strategyqa": "Therefore, the answer (yes or no) is",
            "copa": "Therefore, the answer is",
            "ecare": "Therefore, the answer is",
            "socialiqa": "Therefore, the answer is",
            "piqa": "Therefore, the answer is",
            "anli": "Therefore, the answer is"
        }
    else:
        triggers = {
            "aqua": "The answer is",
            "csqa": "The answer is",
            "letter": "The answer is",
            "addsub": "The answer (arabic numerals) is",
            "gsm8k": "The answer (arabic numerals) is",
            "multiarith": "The answer (arabic numerals) is",
            "singleeq": "The answer (arabic numerals) is",
            "svamp": "The answer (arabic numerals) is",
            "coin": "The answer (yes or no) is",
            "strategyqa": "The answer (yes or no) is",
            "copa": "The answer is",
            "ecare": "The answer is",
            "socialiqa": "The answer is",
            "piqa": "The answer is",
            "anli": "The answer is"
        }

    data = jsonlines.open('./output/{}/{}.jsonl'.format(mode, task))
    examples = []

    predictions, answers = [], []
    for example in data:
        examples.append(example)
        prediction = example['R']['text'].strip().split('\n')[0]
        predictions.append(answer_cleansing(task, prediction, triggers, must_choice=choice))
        if isinstance(example['A'], list):
            answer = example['A'][0]
            answers.append(answer)
        else:
            answers.append(example['A'])

    accuracy = evaluate(predictions, answers, task, examples)

    print('[Mode]: {}'.format(mode))
    print('[Dataset]: {}'.format(task))
    print('[Size]: {}'.format(len(predictions)))
    print('[Accuracy]: {}'.format(accuracy))




