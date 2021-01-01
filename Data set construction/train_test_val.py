# -*- coding：utf-8 -*-
# -*- python3.5
"""
需要修改的地方：
1. xmlfilepath
2. txtsavepath
"""

import os
import random

def Create_Main_Txts(trainval_percent, train_percent):
    # trainval_percent = 0.8
    # train_percent = 1

    # xmlfilepath = 'data/VOCdevkit/VOC2012/Annotations/'
    # txtsavepath = 'data/VOCdevkit/VOC2012/ImageSets/Main'
    xmlfilepath = "data/New Data-jpg/IGBT_Labels"
    txtsavepath = 'data/New Data-jpg/Main'

    if not os.path.exists(txtsavepath):
        os.makedirs(txtsavepath)

    total_xml = os.listdir(xmlfilepath)

    num = len(total_xml)
    list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)

    ftrainval = open(txtsavepath + '/trainval.txt', 'w')
    ftest = open(txtsavepath + '/test.txt', 'w')
    ftrain = open(txtsavepath + '/train.txt', 'w')
    fval = open(txtsavepath + '/val.txt', 'w')

    for i in list:
        name = total_xml[i][:-4] + '\n'
        if i in trainval:
            ftrainval.write(name)
            if i in train:
                ftrain.write(name)
            else:
                fval.write(name)
        else:
            ftest.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()
    print('Well Done！！！')

# if __name__ == "__main__":
#     pass