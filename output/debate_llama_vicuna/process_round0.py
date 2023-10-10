import json
import pdb
import jsonlines
import sys
import re
from fuzzywuzzy import fuzz


def get_answer_davinci(content, task=None):
    content = content.replace(" (yes or no) ", " ")
    response = content.strip()
    prediction = re.findall(pattern_davinci, response)
    if len(prediction) >= 1:
        prediction = prediction[0]
    else:
        prediction = "None"
        # print(response)
    if response.endswith('.'):
        response = response[:-1]
    explanation = '.'.join(response.split('.')[:-1])
    if len(explanation) < 5:
        explanation = f"The answer is ({prediction})."
    
    if not explanation.endswith('.'):
        explanation += '.'

    return prediction, explanation



task = sys.argv[1]

pattern = re.compile("Answer: \(?(A|B|C|D|E|Yes|No|yes|no)\)?")
pattern_davinci = re.compile("[So, |Therefore, ]?[t|T]he answer is \(?(A|B|C|D|E|F|G|Yes|No|yes|no)\)?")
pattern_answer = re.compile("(A|B|C|D|E|F|Yes|No|yes|no)")
answer_dict = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F'}
yes_no_dict = {'A': 'yes', 'B': 'no', 'C': 'None', 'D': 'None'}

chagpt_data = jsonlines.open(f'../LLaMA/13B/{task}.jsonl', 'r')
davinci_data = jsonlines.open(f'../vicuna/{task}.jsonl', 'r')

system_instruct = "You are in a debate now. My opinion is not always true, you can ignore any incorrect part of my opinion. And you can refer to my opinion to revise your choice or defend your own. Please remember there should and must be a more plausible answer in the choices."

agreed, candidates = [], []
a_rr, a_ww, c_rw, c_wr, c_ww = 0, 0, 0, 0, 0
count_chat, cout_davinci = 0, 0
for c, d in zip(chagpt_data, davinci_data):
    assert c['Q'] == d['Q']
    u1_predict, u1_explanation = get_answer_davinci(c['R']['text'], task)
    u2_predict, u2_explanation = get_answer_davinci(d['R']['text'], task)

    c['R'] = [{"role": "system", "content": f"{system_instruct}"},
              {"role": "user", "content": f"Question: {c['Q']}\nChoices: {d['O']}"},
              {"role": "assistant", "content": u1_explanation},
              {"role": "user", "content": u2_explanation}]
    c['P'] = ['None', 'None', u1_predict, u2_predict]
    c['M'] = ['system', 'system', 'llama', 'vicuna']
    
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

fo1 = jsonlines.open(f"./round0/{task}_agreed2.jsonl", 'w')
fo2 = jsonlines.open(f"./round0/{task}_candidate2.jsonl", 'w')

num_instances = a_rr + a_ww + c_wr + c_rw + c_ww
print(f"[Number]: {num_instances}")
print(f"[ChatGPT Acc]: {count_chat/num_instances}")
print(f"[Davinci Acc]: {cout_davinci/num_instances}")

print(f"[ARR]: {a_rr}-{a_rr/num_instances}")
print(f"[AWW]: {a_ww}-{a_ww/num_instances}")
print(f"[CWW]: {c_ww}-{c_ww/num_instances}")
print(f"[CRW]: {c_rw}-{c_rw/num_instances}")
print(f"[CWR]: {c_wr}-{c_wr/num_instances}")

fo1.write_all(agreed)
fo2.write_all(candidates)

fo1.close()
fo2.close()


