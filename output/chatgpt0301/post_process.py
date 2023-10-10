import jsonlines
import sys
import re
import pdb
from fuzzywuzzy import fuzz


def get_prediction(text, choices):
    text = text.replace('\n\n', '\n')
    text = text.strip().split('\n')
    matched = re.findall(pattern, text[0])
    prediction = None
    if len(matched) >= 1:
        prediction = matched[0]
    else:
        predict_text = text[0][8:]
        if predict_text.endswith('.'):
            predict_text = predict_text[:-1]
        choices = choices[1:].split('(')
        for i, c in enumerate(choices):
            if fuzz.ratio(c[3:].lower(), predict_text.lower()) >= 85 or predict_text.lower() in c.lower():
                prediction = answer_dict[str(i)]
                break
            else:
                continue
    if len(text) == 1:
        explanation = '.'.join(text[0].split('.')[1:])
    else:
        explanation = text[1].replace('Explanation: ', '')
    if explanation.strip().startswith('.'):
        explanation = explanation.strip()[1:]
    
    if task == 'strategyqa' and prediction is not None and prediction not in ['Yes', 'No', 'yes', 'no']:
        prediction = yes_no_dict[prediction]
    elif prediction is not None and task == 'strategyqa':
        prediction = prediction.lower()

    if prediction is None:
        print(text, choices)

    return prediction, explanation


def evaluation(hypotheses, references):
    print('====================================')
    count = 0
    for h, r in zip(hypotheses, references):
        if h == r:
            count += 1
        else:
            print(h, r)
    return count / len(references)


if __name__ == "__main__":
    task = sys.argv[1]

    answer_dict = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F'}
    yes_no_dict = {'A': 'yes', 'B': 'no', 'C': 'None', 'D': 'None'}

    pattern = re.compile("Answer: \(?(A|B|C|D|E|Yes|No|yes|no)\)?")

    data = jsonlines.open('{}.jsonl'.format(task), 'r')
    fo = jsonlines.open('./post/{}.jsonl'.format(task), 'w')
    print('+++++++++++++++++++++++++++++++++++')
    labels, predictions = [], []
    for example in data:
        # pdb.set_trace()
        labels.append(example['A'] if task == 'strategyqa' else example['A'][1:-1])

        prediction, explanation = get_prediction(example['R']['text'], example['O'])

        predictions.append(prediction)
        example['R'] = {'P': prediction, 'E': explanation, 'C': prediction==labels[-1]}
        fo.write(example)
    
    fo.close()


    accuracy = evaluation(predictions, labels)

    print('[Model] ChatGPT (gpt3.5-turbo-0301)')
    print('[Task] {}'.format(task))
    print('[Examples]: {}'.format(len(labels)))
    print('[Accuracy]: {}'.format(accuracy))










