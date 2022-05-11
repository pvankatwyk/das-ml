import shutil
import os
import numpy as np

dataset_path = r'F:/Research/DAS/event_detection_grayscale/'

eqs = os.listdir(dataset_path + 'EQ')
nones = os.listdir(dataset_path + 'None')
num_eqs = len(eqs)
num_none = len(nones)

eq_nums_train = np.random.randint(num_eqs-1, size=int(num_eqs * 0.8))
none_nums_train = np.random.randint(num_none-1, size=int(num_none * 0.8))

eqs_train = list(np.array(eqs)[eq_nums_train])
none_train = list(np.array(nones)[none_nums_train])

if 'train' not in os.listdir(dataset_path+'eq_vs_none/'):
    os.mkdir(dataset_path + 'eq_vs_none/train')
    os.mkdir(dataset_path + 'eq_vs_none/test')
    os.mkdir(dataset_path + 'eq_vs_none/train/EQ')
    os.mkdir(dataset_path + 'eq_vs_none/train/None')
    os.mkdir(dataset_path + 'eq_vs_none/test/EQ')
    os.mkdir(dataset_path + 'eq_vs_none/test/None')

for eq in eqs:
    src = dataset_path + 'EQ/'+eq
    if eq in eqs_train:
        dest = dataset_path + 'eq_vs_none/train/EQ/' + eq
    else:
        dest = dataset_path + 'eq_vs_none/test/EQ/' + eq
    shutil.copyfile(src, dest)

for none_ in nones:
    src = dataset_path + 'None/'+none_
    if none_ in none_train:
        dest = dataset_path + 'eq_vs_none/train/None/'+none_
    else:
        dest = dataset_path + 'eq_vs_none/test/None/'+none_
    shutil.copyfile(src, dest)