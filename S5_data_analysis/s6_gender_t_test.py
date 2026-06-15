import pandas as pd
import numpy as np
import os
import json
import pickle as pkl
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler
import pingouin as pg

scaler = MinMaxScaler()


def generate_gender_table(emoji_seperate_dir):
    q_size = 20
    INTERVAL_PATH = "./interval.json"
    info = json.load(open(INTERVAL_PATH))

    FED_path = "./FED.xlsx"

    material_path = (
        "./dataset_for_experiment_with_supplementary_descriptions_by_participants.xlsx"
    )

    FED_df = pd.read_excel(FED_path)

    material_df = pd.read_excel(material_path)
    material_df["emotion_added"].astype(str)
    material_df["meaning_added"].astype(str)

    emoji_vectors_counts_dir = "./emoji_vectors_counts.pkl"
    if os.path.exists(emoji_vectors_counts_dir):
        with open(emoji_vectors_counts_dir, "rb") as f:
            emoji_vectors_counts = pkl.load(f)
    else:
        print("Initialize the emoji_vectors_counts dict")
        emoji_vectors_counts = dict()

    for index, row in tqdm(FED_df.iterrows(), total=len(FED_df)):
        emoji_index = row["index"]

        # print(f"Processing {emoji_index}: {row['emoji']}")

        if emoji_index not in emoji_vectors_counts.keys():
            emoji_vectors_counts[emoji_index] = {
                "Emotion_vectors": None,
                "Emotion_counts": None,
                "Average_emotion_vectors": None,
                "Meaning_vectors": None,
                "Meaning_counts": None,
                "Average_meaning_vectors": None,
            }

        # Calculate the mean and std of each emotional dimension
        df_emoji_rating = pd.read_excel(
            os.path.join(emoji_seperate_dir, f"{emoji_index}.xlsx"), sheet_name="Rating"
        )
        # format the float number with 2 decimal places
        for dim in [
            "Valence",
            "Arousal",
            "Enjoyment",
            "Surprise",
            "Anger",
            "Disgust",
            "Sadness",
            "Fear",
        ]:
            FED_df.loc[index, f"{dim}_mean"] = df_emoji_rating[dim].mean()
            FED_df.loc[index, f"{dim}_std"] = df_emoji_rating[dim].std()

        questionaire_number = (int(emoji_index[1:]) - 1) // q_size + 1
        emoji_info = info[str(questionaire_number)][emoji_index]

        # calculate the statistic for Emotion Agreement
        if emoji_info["Emotion_interval"] is not None:
            df_emoji_emotion = pd.read_excel(
                os.path.join(emoji_seperate_dir, f"{emoji_index}.xlsx"),
                sheet_name="Emotion",
            )
            FED_df.loc[index, "Emotion_SA"] = df_emoji_emotion[
                "Emotion_subjective_ambiguity"
            ].mean()

        # calculate the statistic for Meaning Agreement
        if emoji_info["Meaning_interval"] is not None:
            df_emoji_meaning = pd.read_excel(
                os.path.join(emoji_seperate_dir, f"{emoji_index}.xlsx"),
                sheet_name="Meaning",
            )
            FED_df.loc[index, "Meaning_SA"] = df_emoji_meaning[
                "Meaning_subjective_ambiguity"
            ].mean()

    # save the results
    FED_df = FED_df[
        [
            "index",
            "emoji",
            "Valence_mean",
            "Arousal_mean",
            "Enjoyment_mean",
            "Surprise_mean",
            "Anger_mean",
            "Disgust_mean",
            "Sadness_mean",
            "Fear_mean",
            "Emotion_SA",
            "Meaning_SA",
        ]
    ]

    return FED_df


def main():

    male_dir = "./gender_comparison/seperate_data_of_each_emoji_raw_male"

    male_table = generate_gender_table(male_dir)

    female_dir = "./gender_comparison/seperate_data_of_each_emoji_raw_female"

    female_table = generate_gender_table(female_dir)

    FED_path = "./FED.xlsx"

    whole_table = pd.read_excel(FED_path)

    # t-test across all the quantified dimensions: Valence, Arousal, Enjoyment, Surprise, Anger, Disgust, Sadness, Fear, Emotion_SA, Meaning_SA

    result_dict = dict()

    for dim in [
        "Valence_mean",
        "Arousal_mean",
        "Enjoyment_mean",
        "Surprise_mean",
        "Anger_mean",
        "Disgust_mean",
        "Sadness_mean",
        "Fear_mean",
        "Emotion_SA",
        "Meaning_SA",
    ]:
        t_test_result = pg.ttest(
            male_table[dim], female_table[dim], paired=True, alternative="two-sided"
        )
        print(f"t-test for {dim}: {t_test_result}")

        result_dict[dim] = (
            whole_table[dim].mean(),
            whole_table[dim].std(),
            male_table[dim].mean(),
            male_table[dim].std(),
            female_table[dim].mean(),
            female_table[dim].std(),
            t_test_result["T"].iloc[0],
            t_test_result["p_val"].iloc[0],
        )


    result_df = pd.DataFrame(
        result_dict,
        index=[
            "Mean",
            "Std",
            "Male_Mean",
            "Male_Std",
            "Female_Mean",
            "Female_Std",
            "T",
            "p_val",
        ],
    )

    result_df = result_df.T

    result_df.to_excel("./gender_comparison_t_test_result.xlsx")



if __name__ == "__main__":
    main()
