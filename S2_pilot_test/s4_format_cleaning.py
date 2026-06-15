import os
import pandas as pd 
import emoji as emoji_helper
import numpy as np
import re
from collections import Counter
from collections import OrderedDict as dict

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if "预清洗" in f:
                fullname = os.path.join(root, f)
                yield fullname


def main():
    # base = './raw_result_of_pilot_test'
    count = 0
    d = dict()
    all_files = ["./preprocessed_result_of_pilot_test\preprocessed_问卷编号1.xlsx",
                "./preprocessed_result_of_pilot_test\preprocessed_问卷编号2.xlsx",
                "./preprocessed_result_of_pilot_test\preprocessed_问卷编号3.xlsx",
                "./preprocessed_result_of_pilot_test\preprocessed_问卷编号4.xlsx",
                "./preprocessed_result_of_pilot_test\preprocessed_问卷编号5.xlsx",
                "./preprocessed_result_of_pilot_test\preprocessed_问卷编号6.xlsx",
                "./preprocessed_result_of_pilot_test\preprocessed_问卷编号7.xlsx",
                "./preprocessed_result_of_pilot_test\preprocessed_问卷编号8.xlsx",
                "./preprocessed_result_of_pilot_test\preprocessed_问卷编号9.xlsx",
                "./preprocessed_result_of_pilot_test\preprocessed_问卷编号10.xlsx",
                "./preprocessed_result_of_pilot_test\preprocessed_问卷编号11.xlsx",
                "./preprocessed_result_of_pilot_test\preprocessed_问卷编号12.xlsx",]
    # for path in findAllFile(base):
    for path in all_files:
        print(path)
        df = pd.read_excel(path,header=None)

        for index, row in df.iterrows():

            if index == 0: # 这一行是问题部分
                for col_index in range(0,len(row),4):
                    # print(row[col_index])
                    k = col_index//4 + count*30
                    d[k] = dict()
                    d[k]['emoji'] = emoji_helper.emoji_list(row[col_index])[0]['emoji']
                    d[k]['valence'] = []
                    d[k]['arousal'] = []
                    d[k]['emotion_raw'] = []
                    d[k]['meaning_raw'] = []

            else: # 剩下的几行都是被试的回答
                for col_index in range(len(row)):
                    k = col_index//4 + count*30
                    if col_index % 4 == 0:
                        d[k]['valence'].append(row[col_index])
                    if col_index % 4 == 1:
                        d[k]['arousal'].append(row[col_index])
                    if col_index % 4 == 2:
                        d[k]['emotion_raw'].append(row[col_index])
                    if col_index % 4 == 3:
                        d[k]['meaning_raw'].append(row[col_index])
        count += 1

    for key in d:
        d[key]['valence_mean'] = np.mean(d[key]['valence'])
        d[key]['valence_std']  = np.std(d[key]['valence'])
        d[key]['arousal_mean'] = np.mean(d[key]['arousal'])
        d[key]['arousal_std']  = np.std(d[key]['arousal'])
        # 整理emotion的答案
        pattern = r'[\s，、；]'  
        d[key]['emotion'] = []
        for r in d[key]['emotion_raw']:
            split_text = re.split(pattern, r) 
            d[key]['emotion'].extend(split_text)
        d[key]['emotion'] = Counter(d[key]['emotion'])
        d[key]['emotion'] = sorted(zip(d[key]['emotion'].keys(),d[key]['emotion'].values()),key=lambda x:x[1],reverse=True)

        # 整理meaning的答案
        pattern = r'[\s，、；]'  
        d[key]['meaning'] = []
        for r in d[key]['meaning_raw']:
            split_text = re.split(pattern, r) 
            d[key]['meaning'].extend(split_text)
        d[key]['meaning'] = Counter(d[key]['meaning'])
        d[key]['meaning'] = sorted(zip(d[key]['meaning'].keys(),d[key]['meaning'].values()),key=lambda x : x[1],reverse=True)

    # 写入excel表格
    # 准备列名和数据列表  
    headers = [  
        'emoji', 'valence_mean', 'valence_std', 'arousal_mean', 'arousal_std',  
        'emotion', 'meaning'  
    ]  
    rows = []  
    
    # 遍历字典的每一项  
    for key, value in d.items():  
        # 提取需要的信息  
        emoji = value['emoji']  
        if emoji=='🌍':
            print("不考虑非洲地球")
            continue
        valence_mean = value['valence_mean']  
        valence_std = value['valence_std']  
        arousal_mean = value['arousal_mean']  
        arousal_std = value['arousal_std']  
        emotion = ', '.join([k+'('+str(v)+')' for k,v in value['emotion']])  
        meaning = ', '.join([k+'('+str(v)+')' for k,v in value['meaning']])  
        
        # 将提取的信息添加到数据列表中  
        rows.append([emoji, valence_mean, valence_std, arousal_mean, arousal_std, emotion, meaning])  
    
    # 创建一个DataFrame  
    df = pd.DataFrame(rows, columns=headers)  
    
    # 在DataFrame中添加一个新的列，作为原始的键  
    # df['key'] = list(d.keys())  
    
    # 将DataFrame写入Excel文件  
    df.to_excel('aggregated_preprocessed_results_of_pilot_test.xlsx', index=False)




if __name__ == '__main__':
    main()
