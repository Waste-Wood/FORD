import json
import pdb
import jsonlines
import sys
import re
from fuzzywuzzy import fuzz


def get_answer_chatgpt(content, choices):
    content = content.strip().replace('\n\n', '\n')
    text = content.strip().split('\n')

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

    # if prediction is None:
    #     print(text, choices)

    return prediction, explanation


def get_answer_davinci(content, task=None):
    # pdb.set_trace()
    # if task == 'strategyqa':
    #     try:
    #         explanation, pred = content.strip().split("Therefore, the answer (yes or no) is")
    #     except:
    #         explanation = content.strip()
    #         return "None", explanation
    #     pred = pred.lower()
    #     pred = re.sub("\"|\'|\n|\.|\s|\:|\,", " ", pred)
    #     pred = pred.split(" ")
    #     pred = [i for i in pred if i in ("yes", "no")]
    #     if len(pred) == 1:
    #         pred = pred[0]
    #     else:
    #         pred = "None"
    #     return pred, explanation
    # pdb.set_trace()
    content = content.replace(" (yes or no) ", " ")
    response = content.strip()
    prediction = re.findall(pattern_davinci, response)
    if len(prediction) == 1:
        prediction = prediction[0]
    else:
        prediction = "None"
        # print(response)
    if response.endswith('.'):
        response = response[:-1]
    explanation = '.'.join(response.split('.')[:-1])

    return prediction, explanation



task = sys.argv[1]

pattern = re.compile("Answer: \(?(A|B|C|D|E|Yes|No|yes|no)\)?")
pattern_davinci = re.compile("[So, |Therefore, ]?[t|T]he answer is \(?(A|B|C|D|E|F|G|Yes|No|yes|no)\)?")
pattern_answer = re.compile("(A|B|C|D|E|F|Yes|No|yes|no)")
answer_dict = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F'}
yes_no_dict = {'A': 'yes', 'B': 'no', 'C': 'None', 'D': 'None'}

chagpt_data = jsonlines.open(f'../chatgpt/{task}2.jsonl', 'r')
davinci_data = jsonlines.open(f'../davinci/{task}.jsonl', 'r')

system_instruct = "You are in a debate now. My opinion is not always true, you can ignore any incorrect part of my opinion. And you can refer to my opinion to revise your choice or defend your own. Please remember there should and must be a more plausible answer in the choices."
# debate_instruct = "Do you think I am more reasonable? Give your final answer starting with \"Answer: (A or B) is more plausible.\" and explain very shortly starting with \"Explanation: \". You should choose only one answer."

agreed, candidates = [], []
a_rr, a_ww, c_rw, c_wr, c_ww = 0, 0, 0, 0, 0
count_chat, cout_davinci = 0, 0
for c, d in zip(chagpt_data, davinci_data):
    assert c['Q'] == d['Q']
    u1_predict, u1_explanation = get_answer_chatgpt(c['R']['text'], c['O'])
    u2_predict, u2_explanation = get_answer_davinci(d['R']['text'], task)

    c['R'] = [{"role": "system", "content": f"{system_instruct}"},
              {"role": "user", "content": f"Question: {c['Q']}\nChoices: {d['O']}"},
              {"role": "assistant", "content": u1_explanation},
              {"role": "user", "content": u2_explanation}]
    c['P'] = ['None', 'None', u1_predict, u2_predict]
    c['M'] = ['system', 'system', 'chatgpt', 'davinci']
    
    answer = re.findall(pattern_answer, c['A'])[0]
    if u1_predict == u2_predict == answer:
        a_rr += 1
        count_chat += 1
        cout_davinci += 1
        agreed.append(c)
    elif u1_predict == u2_predict:
        a_ww += 1
        agreed.append(c)
    elif u1_predict != answer and u2_predict != answer:
        c_ww += 1
        candidates.append(c)
    elif u1_predict == answer:
        c_rw += 1
        count_chat += 1
        candidates.append(c)
    else:
        c_wr += 1
        cout_davinci += 1
        candidates.append(c)

# fo1 = jsonlines.open(f"./round0/{task}_agreed.jsonl", 'w')
# fo2 = jsonlines.open(f"./round0/{task}_candidate.jsonl", 'w')

num_instances = a_rr + a_ww + c_wr + c_rw + c_ww
print(f"[Number]: {num_instances}")
print(f"[ChatGPT Acc]: {count_chat/num_instances}")
print(f"[Davinci Acc]: {cout_davinci/num_instances}")

print(f"[ARR]: {a_rr}-{a_rr/num_instances}")
print(f"[AWW]: {a_ww}-{a_ww/num_instances}")
print(f"[CWW]: {c_ww}-{c_ww/num_instances}")
print(f"[CRW]: {c_rw}-{c_rw/num_instances}")
print(f"[CWR]: {c_wr}-{c_wr/num_instances}")

# fo1.write_all(agreed)
# fo2.write_all(candidates)

# fo1.close()
# fo2.close()


