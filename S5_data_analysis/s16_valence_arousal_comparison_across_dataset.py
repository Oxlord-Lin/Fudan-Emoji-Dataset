import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from scipy import stats
from scipy.stats import spearmanr
from utils import get_emoji_img
import matplotlib.pyplot as plt


def compare(df, colx, coly, xlabel, ylabel, title, output_name):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(1, 7)
    ax.set_ylim(1, 7)
    # plot the emoji images on the same plot, on the top layer of the plot
    for i, row in df.iterrows():
        if pd.isna(row[coly]):
            continue
        # print(row["index"])
        emoji_img = get_emoji_img(row["index"])
        ax.imshow(
            emoji_img,
            extent=[
                row[colx] - 0.12,
                row[colx] + 0.12,
                row[coly] - 0.12,
                row[coly] + 0.12,
            ],
            alpha=1,
        )
    corr, _ = spearmanr(df[[colx, coly]].dropna(), nan_policy="omit")
    title = f"{title}\nSpearman correlation = {corr:.3f}; Overlapped emojis = {len(df[df[coly].notna()])}"
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(f"./images/{output_name}.png", dpi=600)
    plt.show()


FED = pd.read_excel("FED.xlsx")

PREVIOUS_DATASET_DIR = "./previous_dataset"
LEED2018 = pd.read_excel(os.path.join(PREVIOUS_DATASET_DIR, "LEED2018.xlsx"))
Scheffler2024 = pd.read_excel(os.path.join(PREVIOUS_DATASET_DIR, "Scheffler2024.xlsx"))
Emoji_Sp = pd.read_excel("./previous_dataset/Emoji-Sp.xlsx")


FED["Unicode_meaning"] = FED["Unicode_meaning"].str.lower()
LEED2018["Intended Meaning"] = LEED2018["Intended Meaning"].str.lower()
# 只保留iOS系统
LEED2018 = LEED2018[LEED2018["System"] == "iOS"]

# 去掉FED["Unicode_meaning"]末尾的'\n'
FED["Unicode_meaning"] = FED["Unicode_meaning"].str.rstrip("\n")

FED["LEED_valence_mean"] = FED["Unicode_meaning"].map(
    LEED2018.set_index("Intended Meaning")["Valence_M"]
)
FED["LEED_arousal_mean"] = FED["Unicode_meaning"].map(
    LEED2018.set_index("Intended Meaning")["Arousal_M"]
)

compare(
    FED,
    "Valence_mean",
    "LEED_valence_mean",
    "FED valence",
    "LEED valence",
    "Valence comparison between FED and LEED",
    "Valence_comparison_between_FED_and_LEED",
)

compare(
    FED,
    "Arousal_mean",
    "LEED_arousal_mean",
    "FED arousal",
    "LEED arousal",
    "Arousal comparison between FED and LEED",
    "Arousal_comparison_between_FED_and_LEED",
)


FED["Scheffler_valence_mean"] = FED["emoji"].map(
    Scheffler2024.set_index("unicode_char")["valence_rating_mean"]
)
FED["Scheffler_arousal_mean"] = FED["emoji"].map(
    Scheffler2024.set_index("unicode_char")["arousal_rating_mean"]
)

FED["Scheffler_valence_mean"] = FED["Scheffler_valence_mean"] / 100 * 6 + 1
FED["Scheffler_arousal_mean"] = FED["Scheffler_arousal_mean"] / 100 * 6 + 1

compare(
    FED,
    "Valence_mean",
    "Scheffler_valence_mean",
    "FED valence",
    "Scheffler valence",
    "Valence comparison between FED and Scheffler&Nenchev (2024)",
    "Valence_comparison_between_FED_and_Scheffler_and_Nenchev (2024)",
)

compare(
    FED,
    "Arousal_mean",
    "Scheffler_arousal_mean",
    "FED arousal",
    "Scheffler arousal",
    "Arousal comparison between FED and Scheffler",
    "Arousal_comparison_between_FED_and_Scheffler",
)

FED["Emoji-Sp_valence_mean"] = FED["emoji"].map(Emoji_Sp.set_index("emoji")["val"])
FED["Emoji-Sp_arousal_mean"] = FED["emoji"].map(Emoji_Sp.set_index("emoji")["aro"])

FED["Emoji-Sp_valence_mean"] = (FED["Emoji-Sp_valence_mean"] - 1) / 8 * 6 + 1
FED["Emoji-Sp_arousal_mean"] = (FED["Emoji-Sp_arousal_mean"] - 1) / 8 * 6 + 1

compare(
    FED,
    "Valence_mean",
    "Emoji-Sp_valence_mean",
    "FED valence",
    "Emoji-Sp valence",
    "Valence comparison between FED and Emoji-SP",
    "Valence_comparison_between_FED_and_Emoji-SP",
)

compare(
    FED,
    "Arousal_mean",
    "Emoji-Sp_arousal_mean",
    "FED arousal",
    "Emoji-Sp arousal",
    "Arousal comparison between FED and Emoji-SP",
    "Arousal_comparison_between_FED_and_Emoji-SP",
)
