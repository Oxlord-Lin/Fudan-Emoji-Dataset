import re 
import pandas as pd

file_name = "MLE_union_KK_union_weibo.xlsx"


def find_content(text):  
    # 使用正则表达式查找所有以##开头，以##结尾的内容  
    # r'##(.*?)##' 中的 (.*?) 是一个非贪婪匹配，它会匹配尽可能少的内容  
    # re.DOTALL 使 . 可以匹配包括换行符在内的所有字符  
    matches = re.findall(r'##(.*?)##', text, re.DOTALL)  
      
    # 去除开头和结尾的符号，并返回结果列表  
    return [match.strip() for match in matches] 

df = pd.read_excel(file_name)

df['ex1'] = df['ex1'].astype(str)
df['ex2'] = df['ex2'].astype(str)
df['ex3'] = df['ex3'].astype(str)

# 遍历每一行  
for index, row in df.iterrows():  
    exs = find_content(row["raw"]) 
    try:
        df.at[index, 'ex1'] = exs[0]  
        df.at[index, 'ex2'] = exs[1]
        df.at[index, 'ex3'] = exs[2]  
    except Exception:
        print(index,end=', ')
  
# 将修改后的数据框保存回Excel文件  
df.to_excel(file_name, index=False)  # 请替换为你想要保存的文件路径
