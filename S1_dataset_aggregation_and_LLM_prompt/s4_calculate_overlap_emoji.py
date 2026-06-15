import pandas as pd

df1 = pd.read_excel("./MLE_union_KK.xlsx")
emoji_set_1 = df1["emoji"].tolist()
print(f"number of emojis in MLE_union_KK.xlsx: {len(emoji_set_1)}")

df2 = pd.read_excel("./FED_20250819.xlsx")
emoji_set_2 = df2["emoji"].tolist()
print(f"number of emojis in FED_20250819.xlsx: {len(emoji_set_2)}")

df3 = pd.read_excel("./Supplementary_material_weibo_emoji_frequency_dataset.xlsx")
df3 = df3[df3['count'] >= 5]
emoji_set_3 = df3["emoji"].tolist()
print(f"number of emojis in high frequent weibo emoji: {len(emoji_set_3)}")

# calculate how many emojis of emojis_set_2 are in emojis_set_1

def count_common_emojis(emoji_set_1, emoji_set_2):
    common_emojis = set(emoji_set_1).intersection(emoji_set_2)
    return len(common_emojis)

common_emojis_count = count_common_emojis(emoji_set_3, emoji_set_1)
print(f"number of common emojis in high frequent weibo emoji and MLE_union_KK.xlsx: {common_emojis_count}")

common_emojis_count = count_common_emojis(emoji_set_3, emoji_set_2)
print(f"number of common emojis in high frequent weibo emoji and FED_20250819.xlsx: {common_emojis_count}")

common_emojis_count = count_common_emojis(emoji_set_1, emoji_set_2)
print(f"number of common emojis in MLE_union_KK.xlsx and FED_20250819.xlsx: {common_emojis_count}")