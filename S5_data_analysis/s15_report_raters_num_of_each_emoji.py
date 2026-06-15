import pandas as pd
import os

seperate_dir = "./seperate_data_of_each_emoji"

df_FED = pd.read_excel("./FED.xlsx")
for index, row in df_FED.iterrows():
    emoji_index = row["index"]
    file_name = f"{emoji_index}.xlsx"
    file_path = os.path.join(seperate_dir, file_name)
    df = pd.read_excel(file_path)
    df_FED.loc[index, "Number_of_raters"] = len(df)

df_FED.to_excel("FED.xlsx", index=False)