import pandas as pd
import os

from utils import (
    plot_emoji_2D,
    spearman_correlation_table,
    PCA_and_plot,
    plot_spearman_heatmap,
)


def main():

    df = pd.read_excel("./FED.xlsx")

    df_index_VA = df[["index", "Valence_mean", "Arousal_mean"]].copy(deep=True)

    # plot_emoji_2D(
    #     df_index_VA,
    #     # title="Emoji在唤醒度-愉悦度二维平面上的分布情况",
    #     title="Emoji Distribution by Valence and Arousal",
    #     n_cluster=0,
    #     # labels=["愉悦度", "唤醒度"],
    #     labels=["Valence", "Arousal"],
    # )

    df_VA_Ekman = df[
        [
            "Valence_mean",
            "Arousal_mean",
            "Enjoyment_mean",
            "Surprise_mean",
            "Anger_mean",
            "Disgust_mean",
            "Sadness_mean",
            "Fear_mean",
        ]
    ]

    # spearman_correlation_table(df_VA_Ekman,"VA_Ekman_spearman_corr.xlsx")
    plot_spearman_heatmap(
        data=df_VA_Ekman,
        title="Spearman correlation coefficients between valence, arousal\nand Ekman’s basic six emotions for emotion-oriented emojis",
        save_path="./images/spearman_heatmap_VA_Ekman.png",
        column_names=[
            "Valence",
            "Arousal",
            "Enjoyment",
            "Surprise",
            "Anger",
            "Disgust",
            "Sadness",
            "Fear",
        ],
    )

    # raise NotImplementedError

    # PCA_and_plot(
    #     df,
    #     # title="6种情绪的PCA降维结果",
    #     title="PCA of Ekman's Six Basic Emotions",
    #     n_cluster=0,
    #     # labels=["第一主成分", "第二主成分"],
    #     labels = ["PC1", "PC2"],
    # )

    df_emo_amb = df[
        [
            "Emotion_SA",
            "Emotion_original_SV",
            "Emotion_modified_SV",
            "Emotion_entropy",
            "Emotion_GV",
        ]
    ]

    plot_spearman_heatmap(
        data=df_emo_amb,
        title="Spearman correlation coefficients between uncertainty metrics\nfor emotion-oriented emojis",
        save_path="./images/spearman_heatmap_emo_amb.png",
        column_names=["SA", "Original SV", "Modified SV", "Entropy", "GV"],
    )

    df_meaning_amb = df[
        [
            "Meaning_SA",
            "Meaning_original_SV",
            "Meaning_modified_SV",
            "Meaning_entropy",
            "Meaning_GV",
        ]
    ]

    plot_spearman_heatmap(
        data=df_meaning_amb,
        title="Spearman correlation coefficients between uncertainty metrics\nfor meaning-oriented emojis",
        save_path="./images/spearman_heatmap_meaning_amb.png",
        column_names=["SA", "Original SV", "Modified SV", "Entropy", "GV"],
    )

    # spearman_correlation_table(df_emo_amb,"emo_amb_spearman_corr.xlsx")
    # spearman_correlation_table(df_meaning_amb,"meaning_amb_spearman_corr.xlsx")


if __name__ == "__main__":
    main()
