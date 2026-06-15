import pandas as pd
import numpy as np

df = pd.read_excel("./emoji_set_for_experiment.xlsx")

print(df.columns)

def count_options(s:str):
    if not isinstance(s, str):
        return 0
    opts = s.split("、")
    return len(opts)

df['emotion_op_counts'] = df["emotion_selected"].apply(count_options)
df["meaning_op_counts"] = df["meaning_selected"].apply(count_options)

# print(df["emotion_op_counts"].describe())
print(df["meaning_op_counts"].describe())