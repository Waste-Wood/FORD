import sys
import os
import jsonlines
import re


f = '{}.jsonl'.format(sys.argv[1])

pattern = re.compile("[So, |Therefore, ]?[t|T]he answer is \((A|B|C|D|E|F|G|Yes|No|yes|no)\)")
pattern_answer = re.compile("(A|B|C|D|E|F|Yes|No|yes|no)")


def get_answer_explanation(example):
    response = example['R']['text'].strip()
    prediction = re.findall(pattern, response)
    if len(prediction) == 1:
        prediction = prediction[0]
    else:
        prediction = "None"
        print(response)
    if response.endswith('.'):
        response = response[:-1]
    explanation = '.'.join(response.split('.')[:-1])

    return prediction, explanation


def evaluation(hypotheses, references):
    assert len(hypotheses) == len(references)

    hit = 0
    for h, r in zip(hypotheses, references):
        if h == r:
            hit += 1
        else:
            continue
    
    return hit / len(hypotheses)


print("="*300)
data = jsonlines.open(f, 'r')
fo = jsonlines.open("./post/{}".format(f), 'w')
predictions, labels = [], []
for instance in data:
    prediction, explanation = get_answer_explanation(instance)

    instance['R'] = {'P': prediction, 'E': explanation}
    fo.write(instance)
    predictions.append(prediction.lower())
    labels.append(re.findall(pattern_answer, instance['A'])[0].lower())

accuracy = evaluation(predictions, labels)

print('[Task] {}'.format(f[:-6]))
print('[Examples] {}'.format(len(labels)))
print('[Accuracy]: {}'.format(accuracy))
    



