import pandas as pd

df1 = pd.read_excel("./Scheffler2024.xlsx")

df2 = pd.read_excel("./Jaeger2019.xlsx")


def remove_symbol(string):
    symbol_to_remove = [":", "_", " "]
    return "".join([char for char in string if char not in symbol_to_remove])

df1["emoji_unicode_name"] = df1["emoji_unicode_name"].apply(remove_symbol)

df2["Emoji name"] = df2["Emoji name"].apply(remove_symbol)

# calculate intersection number

set1 = set(df1["emoji_unicode_name"])
set2 = set(df2["Emoji name"])

intersection_num = len(set1.intersection(set2))

print(intersection_num)