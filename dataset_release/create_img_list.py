# -*- coding: utf-8 -*- #
'''
# ------------------------------------------------------------------------
# File Name:        WSOL_RS/dataset/creat_img_list.py
# Author:           JunJie Ren
# Version:          v1.0
# Created:          2021/10/19
# Description:      — — — — — — — — — — — — — — — — — — — — — — — — — — — 
#                           --> 遥感图像, 弱监督目标定位项目代码 <--        
#                   -- 划分数据集(PatternNet, TODO), 生成WSOL_EVAL框架所需的
#                   数据格式, 即：图像路径 标签 bbox, 若同一图像出现多个目标，
#                   生成多行bbox说明
#                                   --> PatternNetV2 <--
#                   -- 样本总数：11*800-16=8784(部分overpass图像没有目标)
#                   -- 训练集：5268(60%) 测试集：1754(20%) 验证集：1757(20%)
#                                 --> NWPU-RESISC45V2 <--
#                   -- 样本总数：16*700-4=11196(overpass,island部分没有目标)
#                   -- 训练集：6798(60%) 测试集：2254(20%) 验证集：2238(20%)
#                   — — — — — — — — — — — — — — — — — — — — — — — — — — — 
# Module called:    <0> None
# Function List:    <0> None
# Class List:       <0> None
#                   
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# History:
#      |  <author>  | <version> |   <time>   |         <desc>
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#  <0> |    rjj     |   v1.0    | 2021/10/19 | split data & generate .txt
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

# Dataset name list
label2name_txt = open(f'../dataset/{DATASET_NAME}/label2name.txt', 'w')
# Train set path
train_image_ids_txt = open(f'../dataset/{DATASET_NAME}/train/image_ids.txt', 'w')
train_class_labels_txt = open(f'../dataset/{DATASET_NAME}/train/class_labels.txt', 'w')
train_image_sizes_txt = open(f'../dataset/{DATASET_NAME}/train/image_sizes.txt', 'w')
train_localization_txt = open(f'../dataset/{DATASET_NAME}/train/localization.txt', 'w')
# test set path
test_image_ids_txt = open(f'../dataset/{DATASET_NAME}/test/image_ids.txt', 'w')
test_class_labels_txt = open(f'../dataset/{DATASET_NAME}/test/class_labels.txt', 'w')
test_image_sizes_txt = open(f'../dataset/{DATASET_NAME}/test/image_sizes.txt', 'w')
test_localization_txt = open(f'../dataset/{DATASET_NAME}/test/localization.txt', 'w')
# validation set path
val_image_ids_txt = open(f'../dataset/{DATASET_NAME}/val/image_ids.txt', 'w')
val_class_labels_txt = open(f'../dataset/{DATASET_NAME}/val/class_labels.txt', 'w')
val_image_sizes_txt = open(f'../dataset/{DATASET_NAME}/val/image_sizes.txt', 'w')
val_localization_txt = open(f'../dataset/{DATASET_NAME}/val/localization.txt', 'w')

train_ratio = 0.8   # train/all
val_ratio = 0.25     # val/train

image_root = data_root+"Images/"
label_root = data_root+"Labels/"
label_list = []
for dir in tqdm(os.listdir(image_root)):
    print(f"Dir: {dir}")
    if dir not in label_list:
        label_list.append(dir)
        label2name_txt.write('{} {}\n'.format(dir, str(len(label_list)-1)))
        data_path = os.path.join(image_root, dir)

        train_list = random.sample(os.listdir(data_path), 
                                   int(len(os.listdir(data_path))*train_ratio))
        val_list = random.sample(train_list, int(len(train_list)*val_ratio))

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
            im_size = root.findall("size")[0]

            if im in train_list:
                if im in val_list:
                    val_image_ids_txt.write(f"Images/{dir}/{im}\n")
                    val_image_sizes_txt.write(f"Images/{dir}/{im},{im_size[0].text},{im_size[1].text}\n")
                    val_class_labels_txt.write(f"Images/{dir}/{im},{str(len(label_list)-1)}\n")
                    for obj in objects:
                        pos = f"{obj[4][0].text},{obj[4][1].text},{obj[4][2].text},{obj[4][3].text}"
                        val_localization_txt.write(f"Images/{dir}/{im},{pos}\n")
                else:
                    train_image_ids_txt.write(f"Images/{dir}/{im}\n")
                    train_image_sizes_txt.write(f"Images/{dir}/{im},{im_size[0].text},{im_size[1].text}\n")
                    train_class_labels_txt.write(f"Images/{dir}/{im},{str(len(label_list)-1)}\n")
                    for obj in objects:
                        pos = f"{obj[4][0].text},{obj[4][1].text},{obj[4][2].text},{obj[4][3].text}"
                        train_localization_txt.write(f"Images/{dir}/{im},{pos}\n")
            else:
                test_image_ids_txt.write(f"Images/{dir}/{im}\n")
                test_image_sizes_txt.write(f"Images/{dir}/{im},{im_size[0].text},{im_size[1].text}\n")
                test_class_labels_txt.write(f"Images/{dir}/{im},{str(len(label_list)-1)}\n")
                for obj in objects:
                    pos = f"{obj[4][0].text},{obj[4][1].text},{obj[4][2].text},{obj[4][3].text}"
                    test_localization_txt.write(f"Images/{dir}/{im},{pos}\n")

train_image_ids_txt.close()
train_class_labels_txt.close()
train_image_sizes_txt.close()
train_localization_txt.close()

test_image_ids_txt.close()
test_class_labels_txt.close()
test_image_sizes_txt.close()
test_localization_txt.close()

label2name_txt.close()