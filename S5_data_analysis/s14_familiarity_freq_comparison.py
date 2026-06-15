import pandas as pd
import matplotlib.pyplot as plt
from utils import get_emoji_img, rescale
from scipy import stats
import seaborn as sns


def familiarity_freq_comparison(
    df_target, target_freq_col, xlabel, ylabel, title, ranking=True
):

    df = pd.read_excel("./FED.xlsx")

    # df_add = pd.read_excel("./additional_experiment_familarity_score_raw_result.xlsx")
    # df["familiarity_score"] = df["emoji"].map(df_add.set_index("emoji")["平均分"])
    # df.to_excel("./FED.xlsx", index=False)

    df["target_freq"] = df["emoji"].map(df_target.set_index("emoji")[target_freq_col])

    if ranking:
        # df["familiarity_score"] = df["familiarity_score"].rank()
        df["target_freq"] = df["target_freq"].rank()

    df["familiarity_score"] = rescale(df["familiarity_score"])
    df["target_freq"] = rescale(df["target_freq"])

    # calculate spearman correlation
    corr_matrix, p_matrix = stats.spearmanr(
        df[["familiarity_score", "target_freq"]].dropna(), nan_policy="omit"
    )
    print(corr_matrix, p_matrix)
    corr_df = pd.DataFrame(
        corr_matrix,
        index=["familiarity_score", "target_freq"],
        columns=["familiarity_score", "target_freq"],
    )
    spearman_corr = corr_df.iloc[0, 1]

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(1 - 0.5, 7 + 0.5)
    ax.set_ylim(1 - 0.5, 7 + 0.5)
    # plot the emoji images on the same plot, on the top layer of the plot
    for i, row in df.iterrows():
        if pd.isna(row["target_freq"]):
            continue
        print(row["index"])
        emoji_img = get_emoji_img(row["index"])
        ax.imshow(
            emoji_img,
            extent=[
                row["familiarity_score"] - 0.12,
                row["familiarity_score"] + 0.12,
                row["target_freq"] - 0.12,
                row["target_freq"] + 0.12,
            ],
            alpha=1,
        )
    full_title = f"{title}\nSpearman correlation = {spearman_corr:.3f}; Overlapped emojis = {len(df[df["target_freq"].notna()])}"
    plt.title(full_title, fontdict={"fontsize": 20})
    plt.xlabel(xlabel, fontdict={"fontsize": 18})
    plt.ylabel(ylabel, fontdict={"fontsize": 18})
    plt.tight_layout()
    plt.savefig(f"./images/{title}.png", dpi=600)
    plt.show()


# df_ferre = pd.read_excel("./previous_dataset/Emoji-Sp.xlsx")
# target_freq_col = "freq"
# xlabel = "Familiarity score in FED"
# ylabel = "Frequency in Emoji-SP"
# title = "Familiarity score in FED against frequency in Emoji-SP"
# familiarity_freq_comparison(df_ferre, target_freq_col, xlabel, ylabel, title, False)

# df_CCI2 = pd.read_excel("../corpus_freq_count/CCI2_freq.xlsx")
# target_freq_col = "total_count"
# xlabel = "Familiarity score in FED"
# ylabel = "Frequency ranking in CCI 2.0"
# title = "Familiarity score in FED against frequency in CCI 2.0"
# familiarity_freq_comparison(df_CCI2, target_freq_col, xlabel, ylabel, title, True)


##################################################################################################

# df = pd.read_excel("./FED.xlsx")
# df_CCI2 = pd.read_excel("../corpus_freq_count/CCI2_freq.xlsx")
# df["total_count_in_CCI2.0"] = df["emoji"].map(df_CCI2.set_index("emoji")["total_count"])
# df.to_excel("./FED.xlsx", index=False)

##################################################################################################


def freq_freq_comparison(
    df_x,
    df_x_emoji_col,
    df_x_freq_col,
    df_y,
    df_y_emoji_col,
    df_y_freq_col,
    xlabel,
    ylabel,
    title,
    ranking=True,
):

    df_x["y_freq"] = df_x[df_x_emoji_col].map(
        df_y.set_index(df_y_emoji_col)[df_y_freq_col]
    )

    df_x["x_freq"] = df_x[df_x_freq_col]

    # if x_freq or y_freq is nan, drop the row
    df_x = df_x[["x_freq", "y_freq"]]
    df_x = df_x.dropna()

    if ranking:
        df_x["x_freq"] = df_x["x_freq"].rank()
        df_x["y_freq"] = df_x["y_freq"].rank()

    df_x["x_freq"] = rescale(df_x["x_freq"])
    df_x["y_freq"] = rescale(df_x["y_freq"])

    # calculate spearman correlation
    corr_matrix, p_matrix = stats.spearmanr(
        df_x[["x_freq", "y_freq"]].dropna(), nan_policy="omit"
    )
    print(corr_matrix, p_matrix)

    spearman_corr = corr_matrix

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(1 - 0.5, 7 + 0.5)
    ax.set_ylim(1 - 0.5, 7 + 0.5)

    sns.scatterplot(x=df_x["x_freq"], y=df_x["y_freq"])

    full_title = f"{title}\nSpearman correlation = {spearman_corr:.3f}; Overlapped emojis = {len(df_x)}"
    plt.title(full_title, fontdict={"fontsize": 20})
    plt.xlabel(xlabel, fontdict={"fontsize": 18})
    plt.ylabel(ylabel, fontdict={"fontsize": 18})
    plt.tight_layout()
    plt.savefig(f"./images/{title}.png", dpi=600)
    plt.show()


df_x = pd.read_excel("../corpus_freq_count/CCI2_freq.xlsx")
df_x_emoji_col = "emoji"
df_x_freq_col = "total_count"
df_y = pd.read_excel("./previous_dataset/Emoji-Sp.xlsx")
df_y_emoji_col = "emoji"
df_y_freq_col = "freq"
xlabel = "Frequency ranking in CCI 2.0"
ylabel = "Frequency ranking in Emoji-SP"
title = "Frequency in CCI 2.0 against frequency in Emoji-SP"
ranking = True

freq_freq_comparison(
    df_x,
    df_x_emoji_col,
    df_x_freq_col,
    df_y,
    df_y_emoji_col,
    df_y_freq_col,
    xlabel,
    ylabel,
    title,
    ranking,
)


df_x = pd.read_excel("../corpus_freq_count/CCI2_freq.xlsx")
df_x_emoji_col = "emoji"
df_x_freq_col = "total_count"
df_y = pd.read_excel("./previous_dataset/Scheffler2024.xlsx")
df_y_emoji_col = "unicode_char"
df_y_freq_col = "Twitter_frequency"
xlabel = "Frequency ranking in CCI 2.0"
ylabel = "Frequency ranking in Twitter"
title = "Frequency in CCI 2.0 against frequency in Twitter"
ranking = True

freq_freq_comparison(
    df_x,
    df_x_emoji_col,
    df_x_freq_col,
    df_y,
    df_y_emoji_col,
    df_y_freq_col,
    xlabel,
    ylabel,
    title,
    ranking,
)


df_x = pd.read_excel("../corpus_freq_count/CCI2_freq.xlsx")
df_x_emoji_col = "emoji"
df_x_freq_col = "total_count"
df_y = pd.read_excel("./previous_dataset/Scheffler2024.xlsx")
df_y_emoji_col = "unicode_char"
df_y_freq_col = "WhatsApp_frequency"
xlabel = "Frequency ranking in CCI 2.0"
ylabel = "Frequency ranking in WhatsApp"
title = "Frequency in CCI 2.0 against frequency in WhatsApp"
ranking = True

freq_freq_comparison(
    df_x,
    df_x_emoji_col,
    df_x_freq_col,
    df_y,
    df_y_emoji_col,
    df_y_freq_col,
    xlabel,
    ylabel,
    title,
    ranking,
)


df_x = pd.read_excel("./previous_dataset/Emoji-Sp.xlsx")
df_x_emoji_col = "emoji"
df_x_freq_col = "freq"

df_y = pd.read_excel("./previous_dataset/Scheffler2024.xlsx")
df_y_emoji_col = "unicode_char"
df_y_freq_col = "Twitter_frequency"

xlabel = "Frequency ranking in Emoji-SP"
ylabel = "Frequency ranking in Twitter"
title = "Frequency in Emoji-SP against frequency in Twitter"
ranking = True

freq_freq_comparison(
    df_x,
    df_x_emoji_col,
    df_x_freq_col,
    df_y,
    df_y_emoji_col,
    df_y_freq_col,
    xlabel,
    ylabel,
    title,
    ranking,
)

df_x = pd.read_excel("./previous_dataset/Emoji-Sp.xlsx")
df_x_emoji_col = "emoji"
df_x_freq_col = "freq"

df_y = pd.read_excel("./previous_dataset/Scheffler2024.xlsx")
df_y_emoji_col = "unicode_char"
df_y_freq_col = "WhatsApp_frequency"

xlabel = "Frequency ranking in Emoji-SP"
ylabel = "Frequency ranking in WhatsApp"
title = "Frequency in Emoji-SP against frequency in WhatsApp"
ranking = True

freq_freq_comparison(
    df_x,
    df_x_emoji_col,
    df_x_freq_col,
    df_y,
    df_y_emoji_col,
    df_y_freq_col,
    xlabel,
    ylabel,
    title,
    ranking,
)


df_x = pd.read_excel("./previous_dataset/Scheffler2024.xlsx")
df_x_emoji_col = "unicode_char"
df_x_freq_col = "Twitter_frequency"

df_y = pd.read_excel("./previous_dataset/Scheffler2024.xlsx")
df_y_emoji_col = "unicode_char"
df_y_freq_col = "WhatsApp_frequency"

xlabel = "Frequency ranking in Twitter"
ylabel = "Frequency ranking in WhatsApp"
title = "Frequency in Twitter against frequency in WhatsApp"
ranking = True

freq_freq_comparison(
    df_x,
    df_x_emoji_col,
    df_x_freq_col,
    df_y,
    df_y_emoji_col,
    df_y_freq_col,
    xlabel,
    ylabel,
    title,
    ranking,
)
