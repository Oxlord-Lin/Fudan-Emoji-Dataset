import pandas as pd

file_name_1 = "MLE_union_KK.xlsx"
file_name_2 = "weibo_emoji.XLSX"
file_name_result = "MLE_union_KK_union_weibo.xlsx"


df1 = pd.read_excel(file_name_1)
df2 = pd.read_excel(file_name_2)

df_dict = df1.to_dict(orient="records")

emoji_set = set()

for index, row in df1.iterrows():
    emoji = row["emoji"]
    emoji_set.add(emoji)

for index, row in df2.iterrows():
    emoji = row["emoji"]
    count = row["count"]
    if emoji not in emoji_set and count>=5 :
        item = {"index":len(df_dict),"emoji":emoji,"raw":"","ex1":"","ex2":"","ex3":"",}
        df_dict.append(item)

df = pd.DataFrame(df_dict)

df.to_excel(file_name_result,index=False)