#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Date: 2021/7/20 16:06:02
@Software: PyCharm
@Author: lazyn
"""
from re import findall
from argparse import ArgumentParser


def process_video_result(path):
    comparelist = ['LYC_001', 'LYC_002', 'LYC_003', 'LYC_004', 'LYC_005',
                   'LYC_006', 'LYC_007', 'LYC_008', 'LYC_009', 'LYC_010',
                   'LYC_011', 'LYC_012', 'LYC_013', 'LYC_014', 'LYC_015',
                   'LYC_016', 'LYC_017', 'LYC_018', 'LYC_019', 'LYC_020',
                   'LYC_021', 'LYC_022', 'LYC_023', 'LYC_024', 'LYC_025',
                   'LYC_026', 'LYC_027', 'LYC_028', 'LYC_029', 'LYC_030',
                   'LYC_031', 'LYC_032', 'LYC_033', 'LYC_034', 'LYC_035',
                   'LYC_036', 'LYC_037', 'LYC_038', 'LYC_039', 'LYC_040',
                   'LYC_041', 'LYC_042', 'LYC_043', 'LYC_044', 'LYC_045',
                   'LYC_046', 'LYC_047', 'LYC_048', 'LYC_049', 'LYC_050']

    txt = open(path, 'r+')
    acc_dict = {'right_classify': [],
                'wrong_classify': [],
                'no_classify': []}
    for line in txt.readlines():
        label = findall('detect (.*?),', line)[0]
        # 剔除未构建索引的个体
        # if label not in comparelist:
        #     continue
        top = eval(line.split('is')[-1])
        if not top:
            acc_dict['no_classify'].append(label)
            continue
        pre = top[0][0]
        score = top[0][1]
        if label == pre:
            acc_dict['right_classify'].append(label)
        elif score < 0.5:
            acc_dict['no_classify'].append(label)
        else:
            acc_dict['wrong_classify'].append(label)

    print(acc_dict)
    print('right classify is %d, wrong classify is %d, no classify is %d'
          % (len(acc_dict['right_classify']), len(acc_dict['wrong_classify']), len(acc_dict['no_classify'])))
    txt.write('\n' + str(acc_dict) + '\n')
    txt.write('right classify is %d, wrong classify is %d, no classify is %d'
              % (len(acc_dict['right_classify']), len(acc_dict['wrong_classify']), len(acc_dict['no_classify'])))


def process_image_result(path):
    re_dict = {}
    acc_dict = {'right_classify': [],
                'wrong_classify': [],
                'no_classify': []}
    acc_1_dict = {'right_classify': [],
                  'wrong_classify': [],
                  'no_classify': []}
    acc_2_dict = {'right_classify': [],
                  'wrong_classify': [],
                  'no_classify': []}
    txt = open(path, 'r+')
    for line in txt.readlines():
        line = line.rstrip('\n')
        img, pre = line.split('\t')[0], line.split('\t')[1:]
        real = img[:4]
        pre_label, pre_score = pre[0], pre[1]
        if real not in re_dict:
            re_dict[real] = pre
        elif float(pre_score) > float(re_dict[real][1]):
            re_dict[real] = pre
        if '_1_test' in img:
            if pre_label == 'noresult':
                acc_1_dict['no_classify'].append(img[:11])
            elif real == pre_label[-4:]:
                acc_1_dict['right_classify'].append(img[:11])
            else:
                acc_1_dict['wrong_classify'].append(img[:11])
        if '_2_test' in img:
            if pre_label == 'noresult':
                acc_2_dict['no_classify'].append(img[:11])
            elif real == pre_label[-4:]:
                acc_2_dict['right_classify'].append(img[:11])
            else:
                acc_2_dict['wrong_classify'].append(img[:11])

    txt.write('\n' + str(re_dict) + '\n')
    for k in re_dict:
        pre_label = re_dict[k][0]
        if pre_label == 'noresult':
            acc_dict['no_classify'].append(k)
        elif k == pre_label[-4:]:
            acc_dict['right_classify'].append(k)
        else:
            acc_dict['wrong_classify'].append(k)
    # print(acc_dict)
    print('right classify is %d, wrong classify is %d, no classify is %d'
          % (len(acc_dict['right_classify']), len(acc_dict['wrong_classify']), len(acc_dict['no_classify'])))
    txt.write('\n' + str(acc_dict) + '\n')
    txt.write('right classify is %d, wrong classify is %d, no classify is %d\n'
              % (len(acc_dict['right_classify']), len(acc_dict['wrong_classify']), len(acc_dict['no_classify'])))
    if not acc_1_dict['right_classify'] == acc_1_dict['wrong_classify'] == acc_1_dict['no_classify'] == [] and not \
            acc_2_dict['right_classify'] == acc_2_dict['wrong_classify'] == acc_2_dict['no_classify'] == []:
        txt.write('\n' + str(acc_1_dict) + '\n')
        txt.write('right classify is %d, wrong classify is %d, no classify is %d\n'
                  % (len(acc_1_dict['right_classify']), len(acc_1_dict['wrong_classify']), len(acc_1_dict['no_classify'])))
        txt.write('\n' + str(acc_2_dict) + '\n')
        txt.write('right classify is %d, wrong classify is %d, no classify is %d\n'
                  % (len(acc_2_dict['right_classify']), len(acc_2_dict['wrong_classify']), len(acc_2_dict['no_classify'])))
    txt.close()


# result_path = 'output/242+395_1/result1.txt'
# process_video_result(result_path)
#
# result_path = 'output/LYC_fourth_logo_200e_L20.00007_REID_without_200test_1790+200_Flat/result_200test.txt'
# process_image_result(result_path)

parser = ArgumentParser()
parser.add_argument("-rt", "--result_txt", type=str, help="path of process result txt")
parser.add_argument("-m", "--mode", type=str, help="choose process image_result or video_result")
args = parser.parse_args()
if args.mode == 'video':
    process_video_result(args.result_txt)
if args.mode == 'image':
    process_image_result(args.result_txt)
