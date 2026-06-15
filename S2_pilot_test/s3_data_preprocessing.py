import os
import pandas as pd
import re 

def findAllExcel(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if "emoji数据库预实验问卷" in f:
                fullname = os.path.join(root, f)
            yield fullname

def main():
    base = './raw_result_of_pilot_test'
    for path in findAllExcel(base):
        pattern = re.compile(r'问卷编号\d+') 
        name = pattern.findall(path)

        df = pd.read_excel(path)

        # 扔掉用户信息和导言区的部分 
        df = df.drop(df.columns[:17], axis=1)

        # 扔掉测谎项
        for c, _ in df.items():
            # print(c)
            if "直接" in c:     
                # print(c)   
                df = df.drop(c, axis=1) 


        # for _, row in df.iterrows():
            # print(row)
        # 保存结果
        df.to_excel('./preprocessed_result_of_pilot_test/'+name[0]+'.xlsx',index=False)

if __name__ == '__main__':
    main()