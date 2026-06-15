import pandas as pd
import numpy as np
import pickle as pkl
import os

from sklearn.preprocessing import MinMaxScaler

from utils import density_estimation


def main():
    IMAGE_OUTPUT_DIR = "./images/"

    # read the data
    df = pd.read_excel("./FED.xlsx")
    print(f"total emojis count: {len(df)}")

    df_emotion = df[df["Candidate_emotion"].notna()]
    print(f"emotion emojis count: {len(df_emotion)}")

    df_meaning = df[df["Candidate_meaning"].notna()]
    print(f"meaning emojis count: {len(df_meaning)}")

    # calculate the mean and std of all numeric features of df, df_emotion and df_meaning
    # and save the results to a excel file

    # filter the numeric features
    numeric_features = []
    for col in df.columns:
        if "std" in col:
            continue
        if df[col].dtype == "float64" or df[col].dtype == "int64":
            numeric_features.append(col)

    # calculate the mean and std of all numeric features of df, df_emotion and df_meaning
    mean_std_dict = {}
    for col in numeric_features:
        mean_std_dict[col] = {}
        mean_std_dict[col]["all_M"] = df[col].mean()
        mean_std_dict[col]["all_SD"] = df[col].std()

        mean_std_dict[col]["emotion_M"] = df_emotion[col].mean()
        mean_std_dict[col]["emotion_SD"] = df_emotion[col].std()

        mean_std_dict[col]["meaning_M"] = df_meaning[col].mean()
        mean_std_dict[col]["meaning_SD"] = df_meaning[col].std()

    mean_std_df = pd.DataFrame(mean_std_dict).T
    mean_std_df.to_excel("./mean_std.xlsx")

    # raise NotImplementedError("The code is not complete yet.")

    # Density estimation

    df_emotion_VA = df_emotion[["Valence_mean", "Arousal_mean"]]

    density_estimation(
        df_emotion_VA,
        title="Valence and Arousal of emotion-oriented emojis",
        labels=["Valence", "Arousal"],
        output_dir=IMAGE_OUTPUT_DIR,
    )

    df_meaning_VA = df_meaning[["Valence_mean", "Arousal_mean"]]

    density_estimation(
        df_meaning_VA,
        title="Valence and Arousal of meaning-oriented emojis",
        labels=["Valence", "Arousal"],
        output_dir=IMAGE_OUTPUT_DIR,
    )

    df_emotion_emo_features = df_emotion[
        [
            "Enjoyment_mean",
            "Surprise_mean",
            "Anger_mean",
            "Disgust_mean",
            "Sadness_mean",
            "Fear_mean",
        ]
    ]

    density_estimation(
        df_emotion_emo_features,
        title="Ekman's 6 basic emotions of emotion-oriented emojis",
        labels=["Enjoyment", "Surprise", "Anger", "Disgust", "Sadness", "Fear"],
        output_dir=IMAGE_OUTPUT_DIR,
    )

    df_meaning_emo_features = df_meaning[
        [
            "Enjoyment_mean",
            "Surprise_mean",
            "Anger_mean",
            "Disgust_mean",
            "Sadness_mean",
            "Fear_mean",
        ]
    ]

    density_estimation(
        df_meaning_emo_features,
        title="Ekman's 6 basic emotions of meaning-oriented emojis",
        labels=["Enjoyment", "Surprise", "Anger", "Disgust", "Sadness", "Fear"],
        output_dir=IMAGE_OUTPUT_DIR,
    )

    df_emotion_uncertainty_features = df_emotion[
        [
            "Emotion_SA",
            "Emotion_original_SV",
            "Emotion_modified_SV",
            "Emotion_entropy",
            "Emotion_GV",
        ]
    ]

    df_emotion_uncertainty_features = MinMaxScaler().fit_transform(
        df_emotion_uncertainty_features
    )
    df_emotion_uncertainty_features = pd.DataFrame(df_emotion_uncertainty_features)

    density_estimation(
        df_emotion_uncertainty_features,
        title="Emotion uncertainty metircs of emotion-oriented emojis",
        labels=["SA", "Original SV", "Modified SV", "Entropy", "GV"],
        output_dir=IMAGE_OUTPUT_DIR,
    )

    df_meaning_uncertainty_features = df_meaning[
        [
            "Meaning_SA",
            "Meaning_original_SV",
            "Meaning_modified_SV",
            "Meaning_entropy",
            "Meaning_GV",
        ]
    ]

    df_meaning_uncertainty_features = MinMaxScaler().fit_transform(
        df_meaning_uncertainty_features
    )
    df_meaning_uncertainty_features = pd.DataFrame(df_meaning_uncertainty_features)

    density_estimation(
        df_meaning_uncertainty_features,
        title="Meaning uncertainty metircs of meaning-oriented emojis",
        labels=["SA", "Original SV", "Modified SV", "Entropy", "GV"],
        output_dir=IMAGE_OUTPUT_DIR,
    )


if __name__ == "__main__":
    main()
