import jsonlines
import sys
import re


task = sys.argv[1]
data = jsonlines.open('{}.jsonl'.format(task), 'r')
pat1 = re.compile('answer is (A|B|C|D|E|F|yes|no).')
pat2 = re.compile('[A|a]nswer: (A|B|C|D|E|F|yes|no).')
pat3 = re.compile(' (A|B|C|D|E|F|yes|no)[ |.|,]')
pat4 = re.compile('\((A|B|C|D|E|F|yes|no)\)')


def match(text):
    res = re.findall(pat1, text)
    if len(res) == 0:
        res = re.findall(pat2, text)
    if len(res) == 0:
        res = re.findall(pat3, text)
    if len(res) == 0:
        res = re.findall(pat4, text)
    return res


count, total = 0, 0
for i, d in enumerate(data):
    if d['U1'] == True:
        continue
    
    total += 1
    answer = d['A'][1]
    text = d['R'][-1]['content']

    matched = match(text)

    if len(matched) == 0:
        print("{}-{}".format(i, text))
    else:
        if answer == matched[0]:
            count += 1


print('[Task]: {}'.format(task))
print('[Total]: {}'.format(total))
print('[Count]: {}'.format(count))



