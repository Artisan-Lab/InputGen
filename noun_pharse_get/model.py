import os

import torch
from without_cuda import BiLSTM_CRF


def pre_treat(path):
    original_data = open((path), encoding='utf-8').readlines()
    descriptions = []
    for data in original_data:
        descriptions.append(data.replace("\n", ""))
    description = "".join(descriptions)
    return descriptions, description

def get_pre_treat_data():
    filepath = os.path.abspath("./acm_data")
    paths = os.listdir(filepath)
    pre_treat_data_list = []
    pre_treat_data_str = []
    for path in paths:
        a, b = pre_treat(path)
        pre_treat_data_list.append(a)
        pre_treat_data_str.append(b)
    return pre_treat_data_list, pre_treat_data_str

START_TAG = "<START>"
STOP_TAG = "<STOP>"
EMBEDDING_DIM = 64
HIDDEN_DIM = 64

pre_treat_data_list, pre_treat_data_str = get_pre_treat_data()
tag_to_ix = {'B-NP': 0, 'B-PP': 1, 'I-NP': 2, 'B-VP': 3, 'I-VP': 4, 'O': 5, 'I-PP': 6, START_TAG: 7, STOP_TAG: 8}
model = BiLSTM_CRF(len(pre_treat_data_list), tag_to_ix, EMBEDDING_DIM, HIDDEN_DIM)
model.load_state_dict(torch.load("./model.pth"))
model.eval()


