import os
import pandas as pd
import numpy as np

SUBJECT_ID_COL = "2.您的被试编号（由主试告知您）:"
AGE_COL = "3.您的年龄:"
GENDER_COL = "4.您的性别:"

subject = dict()

base_dir = "./raw_result_of_pilot_test"

for file in os.listdir(base_dir):
    if file.endswith(".xlsx"):
        df = pd.read_excel(os.path.join(base_dir, file))
        # # 将SUBJECT_ID_COL列中的值，如果有大写字母，全部换成小写
        # df[SUBJECT_ID_COL] = df[SUBJECT_ID_COL].str.lower()
        
        # 检查被试编号是否有重复值
        if len(df[SUBJECT_ID_COL].unique()) != len(df):
            print(f"{file} 存在重复被试编号！！！")
        for sub_id in df[SUBJECT_ID_COL].unique():
            if sub_id not in subject:
                subject[sub_id] = dict()
                subject[sub_id]["answer"] = 1
                subject[sub_id]["id"] = sub_id
                subject[sub_id]["age"] = int(df[AGE_COL][df[SUBJECT_ID_COL] == sub_id].iloc[0])
                if df[GENDER_COL][df[SUBJECT_ID_COL] == sub_id].iloc[0] == 1:
                    subject[sub_id]["gender"] = "male"
                else:
                    subject[sub_id]["gender"] = "female"
            else:
                subject[sub_id]["answer"] += 1


print(f"共有 {len(subject)} 个被试参与问卷调查。")
print(f"其中男性被试有 {sum(1 for s in subject.values() if s['gender'] =='male')} 个，女性被试有 {sum(1 for s in subject.values() if s['gender'] == 'female')} 个。")
print(f"平均年龄为{np.mean([s['age'] for s in subject.values()]):.2f}")
print(f"年龄的标准差为{np.std([s['age'] for s in subject.values()]):.2f}")

# raise NotImplementedError

# # 找到完成问卷数量的最大值和最小值
# max_answer_num = max(s["answer"] for s in subject.values())
# min_answer_num = min(s["answer"] for s in subject.values())

# # 找出所有完成数量等于最大值的被试
# max_answer_subjects = [s for s in subject.values() if s["answer"] == max_answer_num]

# # 找出所有完成数量等于最小值的被试
# min_answer_subjects = [s for s in subject.values() if s["answer"] == min_answer_num]

# print(f"完成问卷数量最大的被试有 {len(max_answer_subjects)} 个，分别是：")
# for s in max_answer_subjects:
#     print(f"{s['id']}，性别：{s['gender']}，完成问卷数量：{s['answer']}")

# print(f"完成问卷数量最小的被试有 {len(min_answer_subjects)} 个，分别是：")
# for s in min_answer_subjects:
#     print(f"{s['id']}，性别：{s['gender']}，完成问卷数量：{s['answer']}")

# id_list = list(s["id"] for s in subject.values())
# if len(id_list) != len(set(id_list)):
#     print("存在重复被试编号！！！")
# id_list = list(id_list)
# id_list.sort()

# # print(f"所有被试的编号为：\n{id_list}")