import jsonlines
import logging
import os
from torch.utils.data import Dataset


def read_jsonlines(path):
    questions, answers, options, responses = [], [], [], []
    data = jsonlines.open(path, 'r')
    for e in data:
        questions.append(e['Q'])
        if isinstance(e['A'], list):
            answers.append('\t'.join([str(a) for a in e['A']]))
        else:
            answers.append(e['A'])
        if 'O' in e:
            if 'copa' in path or 'ecare' in path or 'train' in path or 'dev' in path or 'strategyqa' in path:
                options.append(e['O'])
            else:
                options.append(' '.join(e['O']))
        else:
            options.append('None')
        if 'R' in e:
            responses.append(e['R'])
        else:
            responses.append('None')

    return questions, options, answers, responses


def define_logger(hps):
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    logging.basicConfig(format='%(asctime)s %(levelname)-8s: %(message)s', level=logging.INFO)
    logger = logging.getLogger(hps.log_name)

    # console_handler = logging.StreamHandler()
    # console_handler.formatter = formatter
    # console_handler.setLevel(logging.INFO)
    # logger.addHandler(console_handler)

    file_path = os.path.join(hps.log_dir, hps.log_name)
    file_handler = logging.FileHandler(file_path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    return logger


class DynamicDataset(Dataset):
    def __init__(self, *args):
        super(DynamicDataset).__init__()
        self.args = args

    def __len__(self):
        return len(self.args[0])

    def __getitem__(self, idx):
        return tuple(arg[idx] for arg in self.args)


def collate_fn(data):

    return tuple(d[0] for d in data)






































