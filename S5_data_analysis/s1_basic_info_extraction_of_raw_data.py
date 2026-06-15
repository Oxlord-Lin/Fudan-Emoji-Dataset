import os
import pandas as pd
import numpy as np

SUBJECT_ID_COL = "2.您的被试编号（由主试告知您）:"
GENDER_COL = "4.您的性别:"
AGE_COL = "3.您的年龄:"

subject = dict()

base_dir = "./raw_questionaire_data"
male_dir = "./gender_comparison/raw_questionaire_data_male"
female_dir = "./gender_comparison/raw_questionaire_data_female"

for file in os.listdir(base_dir):
    if file.endswith(".xlsx"):
        df = pd.read_excel(os.path.join(base_dir, file))
        # 将SUBJECT_ID_COL列中的值，如果有大写字母，全部换成小写
        df[SUBJECT_ID_COL] = df[SUBJECT_ID_COL].str.lower()

        # 检查被试编号是否有重复值
        if len(df[SUBJECT_ID_COL].unique()) != len(df):
            print(f"{file} 存在重复被试编号！！！")
        for sub_id in df[SUBJECT_ID_COL].unique():
            if sub_id not in subject:
                subject[sub_id] = dict()
                subject[sub_id]["answer"] = 1
                subject[sub_id]["id"] = int(sub_id[1:])
                subject[sub_id]["age"] = int(
                    df[AGE_COL][df[SUBJECT_ID_COL] == sub_id].iloc[0]
                )
                if df[GENDER_COL][df[SUBJECT_ID_COL] == sub_id].iloc[0] in [1, "男"]:
                    subject[sub_id]["gender"] = "male"
                else:
                    subject[sub_id]["gender"] = "female"
            else:
                subject[sub_id]["answer"] += 1

        df_male = df[df[GENDER_COL].isin([1, "男"])]
        df_female = df[df[GENDER_COL].isin([2, "女"])]
        if len(df_male) == 0 or len(df_female) == 0:
            print(f"{file} 男女被试数量不足！！！")
        df_male.to_excel(os.path.join(male_dir, file), index=False)
        df_female.to_excel(os.path.join(female_dir, file), index=False)


print(f"共有 {len(subject)} 个被试参与问卷调查。")
print(
    f"其中男性被试有 {sum(1 for s in subject.values() if s['gender'] =='male')} 个，女性被试有 {sum(1 for s in subject.values() if s['gender'] == 'female')} 个。"
)
print(f"平均年龄为{np.mean([s['age'] for s in subject.values()]):.2f}")
print(f"年龄的标准差为{np.std([s['age'] for s in subject.values()]):.2f}")
