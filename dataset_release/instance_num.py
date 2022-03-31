# -*- coding: utf-8 -*- #
'''
# ------------------------------------------------------------------------
# File Name:        WSOL_RS/dataset/creat_img_list.py
# Author:           JunJie Ren
# Version:          v1.0
# Created:          2021/10/19
# Description:      — — — — — — — — — — — — — — — — — — — — — — — — — — — 
#                           --> 遥感图像, 弱监督目标定位项目代码 <--        
#                   -- 划分数据集实例样本量统计
#                   — — — — — — — — — — — — — — — — — — — — — — — — — — — 
# Module called:    <0> None
# Function List:    <0> None
# Class List:       <0> None
#                   
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# History:
#      |  <author>  | <version> |   <time>   |         <desc>
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#  <0> |    rjj     |   v1.0    | 2021/12/5 | split data & generate .txt
# ------------------------------------------------------------------------
'''

import os
import sys
sys.path.append('/media/hp3090/HDD-2T/renjunjie/WSOL_RS/')

import random
from tqdm import tqdm
import xml.etree.ElementTree as ET

DATASET_NAME = "C45V2"
data_root = f"/media/hp3090/HDD-2T/renjunjie/WSOL_RS/dataset/{DATASET_NAME}/"

# # Dataset name list
# label2name_txt = open(f'../dataset/{DATASET_NAME}/label2name.txt', 'w')
# # Train set path
# train_image_ids_txt = open(f'../dataset/{DATASET_NAME}/train/image_ids.txt', 'w')
# train_class_labels_txt = open(f'../dataset/{DATASET_NAME}/train/class_labels.txt', 'w')
# train_image_sizes_txt = open(f'../dataset/{DATASET_NAME}/train/image_sizes.txt', 'w')
# train_localization_txt = open(f'../dataset/{DATASET_NAME}/train/localization.txt', 'w')
# # test set path
# test_image_ids_txt = open(f'../dataset/{DATASET_NAME}/test/image_ids.txt', 'w')
# test_class_labels_txt = open(f'../dataset/{DATASET_NAME}/test/class_labels.txt', 'w')
# test_image_sizes_txt = open(f'../dataset/{DATASET_NAME}/test/image_sizes.txt', 'w')
# test_localization_txt = open(f'../dataset/{DATASET_NAME}/test/localization.txt', 'w')
# # validation set path
# val_image_ids_txt = open(f'../dataset/{DATASET_NAME}/val/image_ids.txt', 'w')
# val_class_labels_txt = open(f'../dataset/{DATASET_NAME}/val/class_labels.txt', 'w')
# val_image_sizes_txt = open(f'../dataset/{DATASET_NAME}/val/image_sizes.txt', 'w')
# val_localization_txt = open(f'../dataset/{DATASET_NAME}/val/localization.txt', 'w')

train_ratio = 0.8   # train/all
val_ratio = 0.25     # val/train

image_root = data_root+"Images/"
label_root = data_root+"Labels/"
label_list = {}
for dir in tqdm(os.listdir(image_root)):
    print(f"Dir: {dir}")
    label_list[dir] = 0
    # if dir not in label_list:
    #     label_list.append(dir)
    #     label2name_txt.write('{} {}\n'.format(dir, str(len(label_list)-1)))
    data_path = os.path.join(image_root, dir)

    #     train_list = random.sample(os.listdir(data_path), 
    #                                int(len(os.listdir(data_path))*train_ratio))
    #     val_list = random.sample(train_list, int(len(train_list)*val_ratio))

    for im in os.listdir(data_path):
        xml_file = label_root+dir+'/'+im[:-3]+"xml"
        try:
            tree = ET.parse(xml_file)
        except:
            print(f"{xml_file} is not exit!")
            continue
        root = tree.getroot()
        objects = root.findall("object")
        if len(objects)==0:
            print(f"{xml_file} has no objects!")
            continue
        # im_size = root.findall("size")[0]
        # print(len(objects))
        label_list[dir] += len(objects)

from matplotlib import pyplot as plt
a = []
b = []
for key,value in label_list.items():
    a.append(key)
    b.append(value)

plt.figure(figsize=(15, 7))
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# 绘制条形图
b = plt.barh(range(len(a)), b, height=0.4)

#添加数据标签
for rect in b:
    w=rect.get_width()
    plt.text(w,rect.get_y()+rect.get_height()/2,'%d'%int(w),ha='left',va='center')
# 对应x轴与字符串
plt.yticks(range(len(a)), a, rotation=0)
# 添加网格 alpha参数是设置网格的透明度的
# plt.grid(alpha=0)
# 保存图片
plt.xlabel('Number of instances')
plt.title('PN2')
plt.savefig("./bar1.png")
plt.show()
