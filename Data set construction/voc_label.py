# -*- coding: utf-8 -*-
"""
需要修改的地方：
1. sets中替换为自己的数据集
2. classes中替换为自己的类别
"""

import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets=[('2012', 'train'), ('2012', 'val'), ('2012', 'test')]  #替换为自己的数据集

# classes = ["person", "bird", "cat", "cow", "dog", "horse", "sheep",
#            "aeroplane", "bicycle", "boat", "bus", "car", "motorbike", "train",
#            "bottle", "chair", "dining table", "potted plant", "sofa", "tv/monitor"]   #修改为自己的类别

#进行归一化
def Convert(size, box):  # size[w,h] box[xmin, xmax, ymin. ymax]
    dw = 1./(size[0])  # size[0] 为宽
    dh = 1./(size[1])  # size[1] 为高
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def Convert_Annotation(year, image_id, classes):
    # 打开VOCdevkit/VOC2012/Annotations/2008_000008.xml
    in_file = open('data/VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id), 'r', encoding='utf-8')  #将数据集放于当前目录下
    # 结果写入VOCdevkit/VOC2012/Label/2008_000008.xml
    out_file = open('data/Label/%s.txt'%(image_id), 'w')
    tree = ET.parse(in_file)    #  解析XML
    root = tree.getroot()    # 获得根节点
    size = root.find('size')    # 找到size 值
    w = int(size.find('width').text)    # 找到宽
    h = int(size.find('height').text)    # 找到 boundingbox 的高

    #  找到"object" 的根节点
    for obj in root.iter('object'):
        # difficult = obj.find('difficult').text
        cls = obj.find('name').text
        # if cls not in classes or int(difficult) == 1:
        if cls not in classes:   # 检索xml中的缺陷名称
            continue
        cls_id = classes.index(cls) # 获取标签名字的编号
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = Convert((w,h), b)    # 转化为yolov3 的数据格式
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

# wd = getcwd()
#
# for year, image_set in sets:
#     if not os.path.exists('data/VOCdevkit/VOC%s/Label/'%(year)):
#         os.makedirs('data/VOCdevkit/VOC%s/Label/'%(year))
#     image_ids = open('data/VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
#     list_file = open('data/VOCdevkit/VOC%s_%s.txt'%(year, image_set), 'w')
#     for image_id in image_ids:
#         list_file.write('data/VOCdevkit/VOC%s/JPEGImages/%s.jpg\n'%(year, image_id))
#         Convert_Annotation(year, image_id, classes)
#     list_file.close()

def Get_Voc_Lable(classes):
    for year, image_set in sets:
        if not os.path.exists('data/Label/'):
            os.makedirs('data/Label/')
        image_ids = open('data/VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
        # # print(image_ids)
        # print('*' * 20)
        list_file = open('data/VOC%s_%s.txt' % (year, image_set), 'w')
        for image_id in image_ids:
            # image_id = image_id[:-1]
            print(image_id)
            if image_set == 'test':
                image_set = 'val'
            list_file.write('data/images/%s%s/%s.jpg\n' % (image_set, year, image_id))
            Convert_Annotation(year, image_id, classes)
        list_file.close()