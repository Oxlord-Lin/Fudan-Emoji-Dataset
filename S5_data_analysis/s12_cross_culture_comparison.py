import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from scipy import stats
from scipy.stats import spearmanr

## Emotional dimension comparison

FED = pd.read_excel("FED.xlsx")

PREVIOUS_DATASET_DIR = "./previous_dataset"
LEED2018 = pd.read_excel(os.path.join(PREVIOUS_DATASET_DIR, "LEED2018.xlsx"))
Scheffler2024 = pd.read_excel(os.path.join(PREVIOUS_DATASET_DIR, "Scheffler2024.xlsx"))
Kimura2017 = pd.read_excel(os.path.join(PREVIOUS_DATASET_DIR, "Kimura2017.xlsx"))
MLE2022 = pd.read_excel(os.path.join(PREVIOUS_DATASET_DIR, "MLE2022.xlsx"))
Emoji_Sp = pd.read_excel("./previous_dataset/Emoji-Sp.xlsx")
Emoji_Dis = pd.read_excel("./previous_dataset/Emoji-Dis.xlsx")

################################# LEED2018 ##########################################
FED["Unicode_meaning"] = FED["Unicode_meaning"].str.lower()
LEED2018["Intended Meaning"] = LEED2018["Intended Meaning"].str.lower()
# 只保留iOS系统
LEED2018 = LEED2018[LEED2018["System"] == "iOS"]

# 去掉FED["Unicode_meaning"]末尾的'\n'
FED["Unicode_meaning"] = FED["Unicode_meaning"].str.rstrip("\n")


FED_LEED2018 = pd.merge(
    FED, LEED2018, left_on="Unicode_meaning", right_on="Intended Meaning", how="inner"
)

# 计算Valence_mean和Arousal_mean的相关系数
valence_corr, valence_pvalue = spearmanr(
    FED_LEED2018["Valence_mean"], FED_LEED2018["Valence_M"], nan_policy="omit"
)
arousal_corr, arousal_pvalue = spearmanr(
    FED_LEED2018["Arousal_mean"], FED_LEED2018["Arousal_M"], nan_policy="omit"
)


print("-" * 50)
print("FED-LEED2018 comparison")
print("Total number of LEED2018-related FED:", len(FED_LEED2018))
print(f"Valence: Corr:{valence_corr:.3f}, p-value: {valence_pvalue:.3f}")
print(f"Arousal: Corr:{arousal_corr:.3f}, p-value: {arousal_pvalue:.3f}")

# 计算距离
FED_LEED2018["difference"] = np.abs(
    FED_LEED2018["Valence_mean"] - FED_LEED2018["Valence_M"]
) + np.abs(FED_LEED2018["Arousal_mean"] - FED_LEED2018["Arousal_M"])

# 找到difference的top-5
print("Top 5 FED-LEED2018 pairs with Greatest difference:")
top5_difference = FED_LEED2018.sort_values(by="difference", ascending=False)[:5]
for index, row in top5_difference.iterrows():
    print(row["emoji"], end="")

print()
# 找到difference的bottom-5
print("Bottom 5 FED-LEED2018 pairs with Least difference:")
bottom5_difference = FED_LEED2018.sort_values(by="difference", ascending=True)[:5]
for index, row in bottom5_difference.iterrows():
    print(row["emoji"], end="")

FED_LEED2018 = FED_LEED2018[
    [
        "index",
        "emoji",
        "difference",
        "Valence_mean",
        "Arousal_mean",
        "Valence_M",
        "Arousal_M",
    ]
]
FED_LEED2018.sort_values(by="difference", ascending=False, inplace=True)
# FED_LEED2018.to_excel("FED_LEED2018.xlsx", index=False)

print("\n")

# raise NotImplementedError

####################################### Scheffler2024 ###############################################
FED_Scheffler2024 = pd.merge(
    FED, Scheffler2024, left_on="emoji", right_on="unicode_char", how="inner"
)
# print("Total number of Scheffler2024-related FED:", len(FED_Scheffler2024))

# 将valence_rating_mean和arousal_rating_mean线性变换到[1,7]之间
FED_Scheffler2024["valence_rating_mean"] = (
    FED_Scheffler2024["valence_rating_mean"] / 100 * 6 + 1
)
FED_Scheffler2024["arousal_rating_mean"] = (
    FED_Scheffler2024["arousal_rating_mean"] / 100 * 6 + 1
)

# 计算Valence_mean和Arousal_mean的相关系数
# valence_corr = FED_Scheffler2024["Valence_mean"].corr(FED_Scheffler2024["valence_rating_mean"])
# arousal_corr = FED_Scheffler2024["Arousal_mean"].corr(FED_Scheffler2024["arousal_rating_mean"])
valence_corr, valence_pvalue = spearmanr(
    FED_Scheffler2024["Valence_mean"],
    FED_Scheffler2024["valence_rating_mean"],
    nan_policy="omit",
)
arousal_corr, arousal_pvalue = spearmanr(
    FED_Scheffler2024["Arousal_mean"],
    FED_Scheffler2024["arousal_rating_mean"],
    nan_policy="omit",
)

print("-" * 50)
print("FED-Scheffler2024 comparison")
print("Total number of Scheffler2024-related FED:", len(FED_Scheffler2024))
print(f"Valence: Corr:{valence_corr:.3f}, p-value: {valence_pvalue:.3f}")
print(f"Arousal: Corr:{arousal_corr:.3f}, p-value: {arousal_pvalue:.3f}")

# 计算距离
FED_Scheffler2024["difference"] = np.abs(
    FED_Scheffler2024["Valence_mean"] - FED_Scheffler2024["valence_rating_mean"]
) + np.abs(FED_Scheffler2024["Arousal_mean"] - FED_Scheffler2024["arousal_rating_mean"])

# 找到difference的top-5
print("Top 5 FED-Scheffler2024 pairs with Greatest difference:")
top5_difference = FED_Scheffler2024.sort_values(by="difference", ascending=False)[:5]
for index, row in top5_difference.iterrows():
    print(row["emoji"], end="")

print()
# 找到difference的bottom-5
print("Bottom 5 FED-Scheffler2024 pairs with Least difference:")
bottom5_difference = FED_Scheffler2024.sort_values(by="difference", ascending=True)[:5]
for index, row in bottom5_difference.iterrows():
    print(row["emoji"], end="")

FED_Scheffler2024 = FED_Scheffler2024[
    [
        "index",
        "emoji",
        "difference",
        "Valence_mean",
        "Arousal_mean",
        "valence_rating_mean",
        "arousal_rating_mean",
    ]
]
FED_Scheffler2024.sort_values(by="difference", ascending=False, inplace=True)
# FED_Scheffler2024.to_excel("FED_Scheffler2024.xlsx", index=False)

print("\n")

#################################################### Kimura2017 ###########################################
FED_Kimura2017 = pd.merge(
    FED, Kimura2017, left_on="emoji", right_on="Emoji", how="inner"
)

print("-" * 50)
print("FED-Kimura2017 comparison")
print("Total number of Kimura2017-related FED:", len(FED_Kimura2017))

# 将Kimura2017的情绪分数线性变换到[1,7]之间
FED_Kimura2017["Happiness"] = (
    MinMaxScaler().fit_transform(FED_Kimura2017[["Happiness"]].values) * 6 + 1
)
FED_Kimura2017["Anger"] = (
    MinMaxScaler().fit_transform(FED_Kimura2017[["Anger"]].values) * 6 + 1
)
FED_Kimura2017["Disgust"] = (
    MinMaxScaler().fit_transform(FED_Kimura2017[["Disgust"]].values) * 6 + 1
)
FED_Kimura2017["Sadness"] = (
    MinMaxScaler().fit_transform(FED_Kimura2017[["Sadness"]].values) * 6 + 1
)

pairs = [
    ("Enjoyment_mean", "Happiness"),
    ("Anger_mean", "Anger"),
    ("Disgust_mean", "Disgust"),
    ("Sadness_mean", "Sadness"),
]
print("Correlation between Kimura2017 and FED:")
for pair in pairs:
    corr, pvalue = spearmanr(
        FED_Kimura2017[pair[0]], FED_Kimura2017[pair[1]], nan_policy="omit"
    )
    print(f"{pair[0]} and {pair[1]} Corr:{corr:.3f}, p-value: {pvalue:.3f}")

# 计算距离
FED_Kimura2017["difference"] = np.sum(
    [np.abs(FED_Kimura2017[pair[0]] - FED_Kimura2017[pair[1]]) for pair in pairs],
    axis=0,
)

# 找到difference的top-5
print("Top 5 FED-Kimura2017 pairs with Greatest difference:")
top5_difference = FED_Kimura2017.sort_values(by="difference", ascending=False)[:5]
for index, row in top5_difference.iterrows():
    print(row["emoji"], end="")

print()
# 找到difference的bottom-5
print("Bottom 5 FED-Kimura2017 pairs with Least difference:")
bottom5_difference = FED_Kimura2017.sort_values(by="difference", ascending=True)[:5]
for index, row in bottom5_difference.iterrows():
    print(row["emoji"], end="")

    # ("Enjoyment_mean", "Happiness"),
    # ("Anger_mean", "Anger"),
    # ("Disgust_mean", "Disgust"),
    # ("Sadness_mean", "Sadness"),

FED_Kimura2017 = FED_Kimura2017[
    [
        "index",
        "emoji",
        "difference",
        "Enjoyment_mean",
        "Anger_mean",
        "Disgust_mean",
        "Sadness_mean",
        "Happiness",
        "Anger",
        "Disgust",
        "Sadness",
    ]
]

FED_Kimura2017.sort_values(by="difference", ascending=False, inplace=True)
# FED_Kimura2017.to_excel("FED_Kimura2017.xlsx", index=False)

print("\n")

############################################# MLE2022 #############################################
FED_MLE2022 = pd.merge(FED, MLE2022, left_on="emoji", right_on="emoji", how="inner")
print("-" * 50)
print("FED-MLE2022 comparison")
print("Total number of MLE2022-related FED:", len(FED_MLE2022))

# 将MLE2022的情绪分数线性变换到[1,7]之间
FED_MLE2022["joy"] = MinMaxScaler().fit_transform(FED_MLE2022[["joy"]].values) * 6 + 1
FED_MLE2022["anger"] = (
    MinMaxScaler().fit_transform(FED_MLE2022[["anger"]].values) * 6 + 1
)
FED_MLE2022["disgust"] = (
    MinMaxScaler().fit_transform(FED_MLE2022[["disgust"]].values) * 6 + 1
)
FED_MLE2022["sadness"] = (
    MinMaxScaler().fit_transform(FED_MLE2022[["sadness"]].values) * 6 + 1
)
FED_MLE2022["fear"] = MinMaxScaler().fit_transform(FED_MLE2022[["fear"]].values) * 6 + 1
FED_MLE2022["surprise"] = (
    MinMaxScaler().fit_transform(FED_MLE2022[["surprise"]].values) * 6 + 1
)

pairs = [
    ("Enjoyment_mean", "joy"),
    ("Anger_mean", "anger"),
    ("Disgust_mean", "disgust"),
    ("Sadness_mean", "sadness"),
    ("Fear_mean", "fear"),
    ("Surprise_mean", "surprise"),
]
print("Correlation between MLE2022 and FED:")
for pair in pairs:
    corr, pvalue = spearmanr(
        FED_MLE2022[pair[0]], FED_MLE2022[pair[1]], nan_policy="omit"
    )
    print(f"{pair[0]} and {pair[1]} Corr:{corr:.3f}, p-value: {pvalue:.3f}")

# 计算距离
FED_MLE2022["difference"] = np.sum(
    [np.abs(FED_MLE2022[pair[0]] - FED_MLE2022[pair[1]]) for pair in pairs], axis=0
)

# 找到difference的top-5
print("Top 5 FED-MLE2022 pairs with Greatest difference:")
top5_difference = FED_MLE2022.sort_values(by="difference", ascending=False)[:5]
for index, row in top5_difference.iterrows():
    print(row["emoji"], end="")

print()
# 找到difference的bottom-5
print("Bottom 5 FED-MLE2022 pairs with Least difference:")
bottom5_difference = FED_MLE2022.sort_values(by="difference", ascending=True)[:5]
for index, row in bottom5_difference.iterrows():
    print(row["emoji"], end="")

# raise NotImplementedError

print()
print("-" * 50)
# 找到Surprise_mean和surprise差距最大的3个emoji
print(
    "Top 5 FED-MLE2022 pairs with Greatest difference between Surprise_mean and surprise:"
)
FED_MLE2022["Surprise_mean - surprise"] = np.abs(
    FED_MLE2022["Surprise_mean"] - FED_MLE2022["surprise"]
)
top5_surprise_diff = FED_MLE2022.sort_values(
    by="Surprise_mean - surprise", ascending=False
)[:5]
for index, row in top5_surprise_diff.iterrows():
    print(
        row["index"],
        row["emoji"],
        f'diff:{row["Surprise_mean - surprise"]:.3f}',
        f'FED: {row["Surprise_mean"]:.3f}',
        f'MLE2022: {row["surprise"]:.3f}',
        end=" |\n",
        sep=" | ",
    )

    # ("Enjoyment_mean", "joy"),
    # ("Anger_mean", "anger"),
    # ("Disgust_mean", "disgust"),
    # ("Sadness_mean", "sadness"),
    # ("Fear_mean", "fear"),
    # ("Surprise_mean", "surprise"),

FED_MLE2022 = FED_MLE2022[
    [
        "index",
        "emoji",
        "difference",
        "Enjoyment_mean",
        "Anger_mean",
        "Disgust_mean",
        "Sadness_mean",
        "Fear_mean",
        "Surprise_mean",
        "joy",
        "anger",
        "disgust",
        "sadness",
        "fear",
        "surprise",
    ]
]
FED_MLE2022.sort_values(by="difference", ascending=False, inplace=True)
# FED_MLE2022.to_excel("FED_MLE2022.xlsx", index=False)


####################################### Emoji-Sp ###############################################
FED_EmojiSp = pd.merge(FED, Emoji_Sp, left_on="emoji", right_on="emoji", how="inner")

# 将valence_rating_mean和arousal_rating_mean线性变换到[1,7]之间
FED_EmojiSp["val"] = (FED_EmojiSp["val"] - 1) / 8 * 6 + 1
FED_EmojiSp["aro"] = (FED_EmojiSp["aro"] - 1) / 8 * 6 + 1

# 计算Valence_mean和Arousal_mean的相关系数
valence_corr, valence_pvalue = spearmanr(
    FED_EmojiSp["Valence_mean"],
    FED_EmojiSp["val"],
    nan_policy="omit",
)
arousal_corr, arousal_pvalue = spearmanr(
    FED_EmojiSp["Arousal_mean"],
    FED_EmojiSp["aro"],
    nan_policy="omit",
)

print("-" * 50)
print("FED-EmojiSp comparison")
print("Total number of FED_EmojiSp-related FED:", len(FED_EmojiSp))
print(f"Valence: Corr:{valence_corr:.3f}, p-value: {valence_pvalue:.3f}")
print(f"Arousal: Corr:{arousal_corr:.3f}, p-value: {arousal_pvalue:.3f}")

# 计算距离
FED_EmojiSp["difference"] = np.abs(
    FED_EmojiSp["Valence_mean"] - FED_EmojiSp["val"]
) + np.abs(FED_EmojiSp["Arousal_mean"] - FED_EmojiSp["aro"])

# 找到difference的top-5
print("Top 5 FED-EmojiSp pairs with Greatest difference:")
top5_difference = FED_EmojiSp.sort_values(by="difference", ascending=False)[:5]
for index, row in top5_difference.iterrows():
    print(row["emoji"], end="")

print()
# 找到difference的bottom-5
print("Bottom 5 FED-EmojiSp pairs with Least difference:")
bottom5_difference = FED_EmojiSp.sort_values(by="difference", ascending=True)[:5]
for index, row in bottom5_difference.iterrows():
    print(row["emoji"], end="")

FED_EmojiSp = FED_EmojiSp[
    [
        "index",
        "emoji",
        "difference",
        "Valence_mean",
        "Arousal_mean",
        "val",
        "aro",
    ]
]
FED_EmojiSp.sort_values(by="difference", ascending=False, inplace=True)

print("\n")


#################################################### Emoji-Dis ###########################################
FED_EmojiDis = pd.merge(FED, Emoji_Dis, left_on="emoji", right_on="emoji", how="inner")

print("-" * 50)
print("FED_EmojiDis comparison")
print("Total number of EmojiDis-related FED:", len(FED_EmojiDis))


# 将EmojiDis的情绪分数线性变换到[1,7]之间
emo_list = ["happiness", "anger", "disgust", "sadness", "fear"]
for emo in emo_list:
    FED_EmojiDis[emo] = (FED_EmojiDis[emo] - 1) / 4 * 6 + 1


pairs = [
    ("Enjoyment_mean", "happiness"),
    ("Anger_mean", "anger"),
    ("Disgust_mean", "disgust"),
    ("Sadness_mean", "sadness"),
    ("Fear_mean", "fear"),
]
print("Correlation between Emoji-Dis and FED:")
for pair in pairs:
    corr, pvalue = spearmanr(
        FED_EmojiDis[pair[0]], FED_EmojiDis[pair[1]], nan_policy="omit"
    )
    print(f"{pair[0]} and {pair[1]} Corr:{corr:.3f}, p-value: {pvalue:.3f}")

# 计算距离
FED_EmojiDis["difference"] = np.sum(
    [np.abs(FED_EmojiDis[pair[0]] - FED_EmojiDis[pair[1]]) for pair in pairs],
    axis=0,
)

# 找到difference的top-5
print("Top 5 FED-EmojiDis pairs with Greatest difference:")
top5_difference = FED_EmojiDis.sort_values(by="difference", ascending=False)[:5]
for index, row in top5_difference.iterrows():
    print(row["emoji"], end="")

print()
# 找到difference的bottom-5
print("Bottom 5 FED-EmojiDis pairs with Least difference:")
bottom5_difference = FED_EmojiDis.sort_values(by="difference", ascending=True)[:5]
for index, row in bottom5_difference.iterrows():
    print(row["emoji"], end="")


FED_EmojiDis = FED_EmojiDis[
    [
        "index",
        "emoji",
        "difference",
        "Enjoyment_mean",
        "Anger_mean",
        "Disgust_mean",
        "Sadness_mean",
        "Fear_mean",
        "happiness",
        "anger",
        "disgust",
        "sadness",
        "fear",
    ]
]

FED_EmojiDis.sort_values(by="difference", ascending=False, inplace=True)

print("\n")

############################################# 存储对别结果 ###############################

# 存到一个excel中
with pd.ExcelWriter("cross_culture_exploration_emotional_dimensions.xlsx") as writer:
    FED_LEED2018.to_excel(writer, sheet_name="FED_LEED2018", index=False)
    FED_Scheffler2024.to_excel(writer, sheet_name="FED_Scheffler2024", index=False)
    FED_Kimura2017.to_excel(writer, sheet_name="FED_Kimura2017", index=False)
    FED_MLE2022.to_excel(writer, sheet_name="FED_MLE2022", index=False)
    FED_EmojiSp.to_excel(writer, sheet_name="FED_EmojiSp", index=False)
    FED_EmojiDis.to_excel(writer, sheet_name="FED_EmojiDis",index=False)


## subjective ambiguity (SA) vs. Clairy


FED = pd.read_excel("FED.xlsx")

PREVIOUS_DATASET_DIR = "./previous_dataset"
LEED2018 = pd.read_excel(os.path.join(PREVIOUS_DATASET_DIR, "LEED2018.xlsx"))
Scheffler2024 = pd.read_excel(os.path.join(PREVIOUS_DATASET_DIR, "Scheffler2024.xlsx"))
Emoji_Sp = pd.read_excel("./previous_dataset/Emoji-Sp.xlsx")

################################# LEED2018 ##########################################
FED["Unicode_meaning"] = FED["Unicode_meaning"].str.lower()
LEED2018["Intended Meaning"] = LEED2018["Intended Meaning"].str.lower()
# 只保留iOS系统
LEED2018 = LEED2018[LEED2018["System"] == "iOS"]

# 去掉FED["Unicode_meaning"]末尾的'\n'
FED["Unicode_meaning"] = FED["Unicode_meaning"].str.rstrip("\n")

FED_LEED2018 = pd.merge(
    FED, LEED2018, left_on="Unicode_meaning", right_on="Intended Meaning", how="inner"
)

# 计算相关系数
emotion_clarity_corr, emotion_clarity_pvalue = spearmanr(
    FED_LEED2018["Emotion_SA"], FED_LEED2018["Clarity_M"], nan_policy="omit"
)
meaning_clarity_corr, meaning_clarity_pvalue = spearmanr(
    FED_LEED2018["Meaning_SA"], FED_LEED2018["Clarity_M"], nan_policy="omit"
)

print("-" * 50)
print("FED-LEED2018 comparison")
print(
    "emotion-oriented emojis count:",
    len(FED_LEED2018[FED_LEED2018["category"].isin(["emotion-oriented", "overlap"])]),
)
print(
    "meaning-oriented emojis count:",
    len(FED_LEED2018[FED_LEED2018["category"].isin(["meaning-oriented", "overlap"])]),
)
print(
    f"Emotion Clarity Corr:{emotion_clarity_corr:.3f}, p-value: {emotion_clarity_pvalue:.3f}"
)
print(
    f"Meaning Clarity Corr:{meaning_clarity_corr:.3f}, p-value: {meaning_clarity_pvalue:.3f}"
)

# 计算距离
FED_LEED2018["Emotion_SA_clarity_difference"] = np.abs(
    FED_LEED2018["Emotion_SA"] - (8 - FED_LEED2018["Clarity_M"])
)
FED_LEED2018["Meaning_SA_clarity_difference"] = np.abs(
    FED_LEED2018["Meaning_SA"] - (8 - FED_LEED2018["Clarity_M"])
)

# 找到difference的top-5
print("Top 5 FED-LEED2018 pairs with Greatest difference for emotion-oriented emojis:")
top5_difference = FED_LEED2018.sort_values(
    by="Emotion_SA_clarity_difference", ascending=False
)[:5]
for index, row in top5_difference.iterrows():
    print(row["emoji"], end="")

print()
# 找到difference的bottom-5
print("Bottom 5 FED-LEED2018 pairs with Least difference for emotion-oriented emojis:")
bottom5_difference = FED_LEED2018.sort_values(
    by="Emotion_SA_clarity_difference", ascending=True
)[:5]
for index, row in bottom5_difference.iterrows():
    print(row["emoji"], end="")

print()
# 找到difference的top-5
print("Top 5 FED-LEED2018 pairs with Greatest difference for meaning-oriented emojis:")
top5_difference = FED_LEED2018.sort_values(
    by="Meaning_SA_clarity_difference", ascending=False
)[:5]
for index, row in top5_difference.iterrows():
    print(row["emoji"], end="")

print()
# 找到difference的bottom-5
print("Bottom 5 FED-LEED2018 pairs with Least difference for meaning-oriented emojis:")
bottom5_difference = FED_LEED2018.sort_values(
    by="Meaning_SA_clarity_difference", ascending=True
)[:5]
for index, row in bottom5_difference.iterrows():
    print(row["emoji"], end="")

FED_LEED2018 = FED_LEED2018[
    [
        "index",
        "emoji",
        "Emotion_SA_clarity_difference",
        "Emotion_SA",
        "Meaning_SA_clarity_difference",
        "Meaning_SA",
        "Clarity_M",
    ]
]

print("\n")


####################################### Scheffler2024 ###############################################
FED_Scheffler2024 = pd.merge(
    FED, Scheffler2024, left_on="emoji", right_on="unicode_char", how="inner"
)

# 将valence_rating_mean和arousal_rating_mean线性变换到[1,7]之间
FED_Scheffler2024["clarity_rating_mean"] = (
    FED_Scheffler2024["clarity_rating_mean"] / 100 * 6 + 1
)

# 计算相关系数
emotion_clarity_corr, emotion_clarity_pvalue = spearmanr(
    FED_Scheffler2024["Emotion_SA"], FED_Scheffler2024["clarity_rating_mean"], nan_policy="omit"
)
meaning_clarity_corr, meaning_clarity_pvalue = spearmanr(
    FED_Scheffler2024["Meaning_SA"], FED_Scheffler2024["clarity_rating_mean"], nan_policy="omit"
)

print("-" * 50)
print("FED-Scheffler2024 comparison")
print(
    "emotion-oriented emojis count:",
    len(FED_Scheffler2024[FED_Scheffler2024["category"].isin(["emotion-oriented", "overlap"])]),
)
print(
    "meaning-oriented emojis count:",
    len(FED_Scheffler2024[FED_Scheffler2024["category"].isin(["meaning-oriented", "overlap"])]),
)
print(
    f"Emotion Clarity Corr:{emotion_clarity_corr:.3f}, p-value: {emotion_clarity_pvalue:.4f}"
)
print(
    f"Meaning Clarity Corr:{meaning_clarity_corr:.3f}, p-value: {meaning_clarity_pvalue:.4f}"
)

# 计算距离
FED_Scheffler2024["Emotion_SA_clarity_difference"] = np.abs(
    FED_Scheffler2024["Emotion_SA"] - (8 - FED_Scheffler2024["clarity_rating_mean"])
)
FED_Scheffler2024["Meaning_SA_clarity_difference"] = np.abs(
    FED_Scheffler2024["Meaning_SA"] - (8 - FED_Scheffler2024["clarity_rating_mean"])
)

# 找到difference的top-5
print("Top 5 FED-Scheffler2024 pairs with Greatest difference for emotion-oriented emojis:")
top5_difference = FED_Scheffler2024.sort_values(
    by="Emotion_SA_clarity_difference", ascending=False
)[:5]
for index, row in top5_difference.iterrows():
    print(row["emoji"], end="")

print()
# 找到difference的bottom-5
print("Bottom 5 FED-Scheffler2024 pairs with Least difference for emotion-oriented emojis:")
bottom5_difference = FED_Scheffler2024.sort_values(
    by="Emotion_SA_clarity_difference", ascending=True
)[:5]
for index, row in bottom5_difference.iterrows():
    print(row["emoji"], end="")

print()
# 找到difference的top-5
print("Top 5 FED-Scheffler2024 pairs with Greatest difference for meaning-oriented emojis:")
top5_difference = FED_Scheffler2024.sort_values(
    by="Meaning_SA_clarity_difference", ascending=False
)[:5]
for index, row in top5_difference.iterrows():
    print(row["emoji"], end="")

print()
# 找到difference的bottom-5
print("Bottom 5 FED-Scheffler2024 pairs with Least difference for meaning-oriented emojis:")
bottom5_difference = FED_Scheffler2024.sort_values(
    by="Meaning_SA_clarity_difference", ascending=True
)[:5]
for index, row in bottom5_difference.iterrows():
    print(row["emoji"], end="")

FED_Scheffler2024 = FED_Scheffler2024[
    [
        "index",
        "emoji",
        "Emotion_SA_clarity_difference",
        "Emotion_SA",
        "Meaning_SA_clarity_difference",
        "Meaning_SA",
        "clarity_rating_mean",
    ]
]



####################################### Emoji-Sp ###############################################
FED_EmojiSp = pd.merge(
    FED, Emoji_Sp, left_on="emoji", right_on="emoji", how="inner"
)

# 计算相关系数
emotion_clarity_corr, emotion_clarity_pvalue = spearmanr(
    FED_EmojiSp["Emotion_SA"], FED_EmojiSp["clar"], nan_policy="omit"
)
meaning_clarity_corr, meaning_clarity_pvalue = spearmanr(
    FED_EmojiSp["Meaning_SA"], FED_EmojiSp["clar"], nan_policy="omit"
)

print("-" * 50)
print("FED-EmojiSp comparison")
print(
    "emotion-oriented emojis count:",
    len(FED_EmojiSp[FED_EmojiSp["category"].isin(["emotion-oriented", "overlap"])]),
)
print(
    "meaning-oriented emojis count:",
    len(FED_EmojiSp[FED_EmojiSp["category"].isin(["meaning-oriented", "overlap"])]),
)
print(
    f"Emotion Clarity Corr:{emotion_clarity_corr:.3f}, p-value: {emotion_clarity_pvalue:.4f}"
)
print(
    f"Meaning Clarity Corr:{meaning_clarity_corr:.3f}, p-value: {meaning_clarity_pvalue:.4f}"
)

# 计算距离
FED_EmojiSp["Emotion_SA_clarity_difference"] = np.abs(
    FED_EmojiSp["Emotion_SA"] - (8 - FED_EmojiSp["clar"])
)
FED_EmojiSp["Meaning_SA_clarity_difference"] = np.abs(
    FED_EmojiSp["Meaning_SA"] - (8 - FED_EmojiSp["clar"])
)

# 找到difference的top-5
print("Top 5 FED-EmojiSp pairs with Greatest difference for emotion-oriented emojis:")
top5_difference = FED_EmojiSp.sort_values(
    by="Emotion_SA_clarity_difference", ascending=False
)[:5]
for index, row in top5_difference.iterrows():
    print(row["emoji"], end="")

print()
# 找到difference的bottom-5
print("Bottom 5 FED-EmojiSp pairs with Least difference for emotion-oriented emojis:")
bottom5_difference = FED_EmojiSp.sort_values(
    by="Emotion_SA_clarity_difference", ascending=True
)[:5]
for index, row in bottom5_difference.iterrows():
    print(row["emoji"], end="")

print()
# 找到difference的top-5
print("Top 5 FED-EmojiSp pairs with Greatest difference for meaning-oriented emojis:")
top5_difference = FED_EmojiSp.sort_values(
    by="Meaning_SA_clarity_difference", ascending=False
)[:5]
for index, row in top5_difference.iterrows():
    print(row["emoji"], end="")

print()
# 找到difference的bottom-5
print("Bottom 5 FED-EmojiSp pairs with Least difference for meaning-oriented emojis:")
bottom5_difference = FED_EmojiSp.sort_values(
    by="Meaning_SA_clarity_difference", ascending=True
)[:5]
for index, row in bottom5_difference.iterrows():
    print(row["emoji"], end="")

FED_EmojiSp = FED_EmojiSp[
    [
        "index",
        "emoji",
        "Emotion_SA_clarity_difference",
        "Emotion_SA",
        "Meaning_SA_clarity_difference",
        "Meaning_SA",
        "clar",
    ]
]


# 存到一个excel中
with pd.ExcelWriter("cross_culture_exploration_clarity_dimensions.xlsx") as writer:
    FED_LEED2018.to_excel(writer, sheet_name="FED_LEED2018", index=False)
    FED_Scheffler2024.to_excel(writer, sheet_name="FED_Scheffler2024", index=False)
    FED_EmojiSp.to_excel(writer, sheet_name="FED_EmojiSp", index=False)