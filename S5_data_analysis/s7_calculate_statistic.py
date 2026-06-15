import pandas as pd
import numpy as np
import os
import json
import pickle as pkl
from tqdm import tqdm
from utils import (
    count_added_item,
    calculate_generalized_variation,
    word2vec,
    calculate_embedding_vector_variation,
    calculate_entropy,
)
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

def main():
    q_size = 20
    INTERVAL_PATH = "./interval.json"
    info = json.load(open(INTERVAL_PATH))

    FED_path = "./FED.xlsx"
    material_path = "./正式实验材料+被试补充情绪与含义.xlsx"

    FED_df = pd.read_excel(FED_path)

    material_df = pd.read_excel(material_path)
    material_df["emotion_added"].astype(str)
    material_df["meaning_added"].astype(str)

    emoji_seperate_dir = "./seperate_data_of_each_emoji"

    emoji_vectors_counts_dir = "./emoji_vectors_counts.pkl"
    if os.path.exists(emoji_vectors_counts_dir):
        with open(emoji_vectors_counts_dir, "rb") as f:
            emoji_vectors_counts = pkl.load(f)
    else:
        print("Initialize the emoji_vectors_counts dict")
        emoji_vectors_counts = dict()

    for index, row in tqdm(FED_df.iterrows(), total=len(FED_df)):
        emoji_index = row["index"]
        if not os.path.exists(os.path.join(emoji_seperate_dir, f"{emoji_index}.xlsx")):
            print(
                f"Emoji {emoji_index} not found in seperate_data_of_each_emoji folder"
            )
            continue

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

        # calculate the generalized variation of emotional ratings
        # first transeform the emotional ratings into a design matrix
        # emotion_ratings = df_emoji_rating.to_numpy()
        # FED_df.loc[index, "G_var_of_emotion_rating"] = calculate_generalized_variation(
        #     emotion_ratings[:, 2:], mode="det"
        # )  # The design matrix may be singular, so that we use trace version of Generalized variation
        # # TODO: Compare retain/drop the valence and arousal columns from the design matrix

        questionaire_number = (int(emoji_index[1:]) - 1) // q_size + 1
        emoji_info = info[str(questionaire_number)][emoji_index]

        # assign the category
        if emoji_info["Emotion_interval"] is not None and emoji_info["Meaning_interval"] is not None:
            FED_df.loc[index, "category"] = "overlap"
        elif emoji_info["Emotion_interval"] is not None:
            FED_df.loc[index, "category"] = "emotion-oriented"
        elif emoji_info["Meaning_interval"] is not None:
            FED_df.loc[index, "category"] = "meaning-oriented"

        
        # calculate the statistic for Emotion Agreement
        if emoji_info["Emotion_interval"] is not None:
            df_emoji_emotion = pd.read_excel(
                os.path.join(emoji_seperate_dir, f"{emoji_index}.xlsx"),
                sheet_name="Emotion",
            )
            FED_df.loc[index, "Emotion_SA"] = df_emoji_emotion[
                "Emotion_subjective_ambiguity"
            ].mean()
            FED_df.loc[index, "Emotion_SA_std"] = df_emoji_emotion[
                "Emotion_subjective_ambiguity"
            ].std()
            emotion_agreement = df_emoji_emotion.iloc[:, :-2]

            # if emotion_agreement has more than one column, calculate the generalized variation
            FED_df.loc[index, "Emotion_GV"] = calculate_generalized_variation(
                emotion_agreement.to_numpy(), mode="det"
            )
            emotion_choice = emoji_info["Emotion_selected"]

            # calculate the mean of each emotion choice
            choice_count = []
            for emo in emotion_choice:
                choice_count.append((emo, df_emoji_emotion[emo].mean()))
            choice_count = sorted(choice_count, key=lambda x: x[1], reverse=True)

            # write the choice_count dict into FED_df in the ascending order of value
            FED_df.loc[index, "Candidate_emotion"] = ";".join(
                [f"{emo}({avg:.2f})" for emo, avg in choice_count]
            )

            if emoji_vectors_counts[emoji_index]["Emotion_vectors"] is None:
                print("processing emotion vectors of ", emoji_index)
                emoji_vectors_counts[emoji_index]["Emotion_vectors"] = word2vec(
                    [emo for emo, avg in choice_count]
                )
            emoji_vectors_counts[emoji_index]["Emotion_counts"] = [
                avg for emo, avg in choice_count
            ]
            emoji_vectors_counts[emoji_index]["Average_emotion_vectors"] = np.average(
                emoji_vectors_counts[emoji_index]["Emotion_vectors"],
                axis=0,
                weights=emoji_vectors_counts[emoji_index]["Emotion_counts"],
            )

            vec = emoji_vectors_counts[emoji_index]["Average_emotion_vectors"].tolist()
            formatted_str = f"[{','.join(map(str, vec))}]"

            FED_df.loc[index, "Emotion_embedding"] = formatted_str

            # add the additional emotion provided by participants
            emotion_added = df_emoji_emotion["被试补充情绪"]
            emotion_added.astype(str)
            material_df.loc[index, "emotion_added"] = count_added_item(emotion_added)

            if len(emotion_choice) > 1:
                # calculate the entropy of the emotion
                FED_df.loc[index, "Emotion_entropy"] = calculate_entropy(choice_count)

                # calculate the variation of the emotion embedding vectors
                FED_df.loc[index, "Emotion_original_SV"] = (
                    calculate_embedding_vector_variation(
                        emoji_vectors_counts[emoji_index]["Emotion_vectors"],
                        emoji_vectors_counts[emoji_index]["Emotion_counts"],
                        mode="original",
                    )
                )
                FED_df.loc[index, "Emotion_modified_SV"] = (
                    calculate_embedding_vector_variation(
                        emoji_vectors_counts[emoji_index]["Emotion_vectors"],
                        emoji_vectors_counts[emoji_index]["Emotion_counts"],
                        mode="modified",
                    )
                )

        # calculate the statistic for Meaning Agreement
        if emoji_info["Meaning_interval"] is not None:
            df_emoji_meaning = pd.read_excel(
                os.path.join(emoji_seperate_dir, f"{emoji_index}.xlsx"),
                sheet_name="Meaning",
            )
            FED_df.loc[index, "Meaning_SA"] = df_emoji_meaning[
                "Meaning_subjective_ambiguity"
            ].mean()
            FED_df.loc[index, "Meaning_SA_std"] = df_emoji_meaning[
                "Meaning_subjective_ambiguity"
            ].std()
            meaning_agreement = df_emoji_meaning.iloc[:, :-2]
            FED_df.loc[index, "Meaning_GV"] = calculate_generalized_variation(
                meaning_agreement.to_numpy(), mode="det"
            )
            meaning_choice = emoji_info["Meaning_selected"]

            # calculate the mean of each meaning choice
            choice_count = []
            for mean in meaning_choice:
                choice_count.append((mean, df_emoji_meaning[mean].mean()))
            choice_count = sorted(choice_count, key=lambda x: x[1], reverse=True)
            FED_df.loc[index, "Candidate_meaning"] = ";".join(
                [f"{mean}({avg:.2f})" for mean, avg in choice_count]
            )

            if emoji_vectors_counts[emoji_index]["Meaning_vectors"] is None:
                print("processing meaning vectors of ", emoji_index)
                emoji_vectors_counts[emoji_index]["Meaning_vectors"] = word2vec(
                    [mean for mean, avg in choice_count]
                )
            emoji_vectors_counts[emoji_index]["Meaning_counts"] = [
                avg for mean, avg in choice_count
            ]
            emoji_vectors_counts[emoji_index]["Average_meaning_vectors"] = np.average(
                emoji_vectors_counts[emoji_index]["Meaning_vectors"],
                axis=0,
                weights=emoji_vectors_counts[emoji_index]["Meaning_counts"],
            )

            vec = emoji_vectors_counts[emoji_index]["Average_meaning_vectors"].tolist()
            formatted_str = f"[{','.join(map(str, vec))}]"

            FED_df.loc[index, "Meaning_embedding"] = formatted_str

            # add the additional meaning provided by participants
            meanning_added = df_emoji_meaning["被试补充含义"]
            meanning_added.astype(str)
            material_df.loc[index, "meaning_added"] = count_added_item(meanning_added)

            if len(meaning_choice) > 1:
                # calculate the entropy of the meaning
                FED_df.loc[index, "Meaning_entropy"] = calculate_entropy(choice_count)

                # calculate the variation of the meaning embedding vectors
                FED_df.loc[index, "Meaning_original_SV"] = (
                    calculate_embedding_vector_variation(
                        emoji_vectors_counts[emoji_index]["Meaning_vectors"],
                        emoji_vectors_counts[emoji_index]["Meaning_counts"],
                        mode="original",
                    )
                )
                FED_df.loc[index, "Meaning_modified_SV"] = (
                    calculate_embedding_vector_variation(
                        emoji_vectors_counts[emoji_index]["Meaning_vectors"],
                        emoji_vectors_counts[emoji_index]["Meaning_counts"],
                        mode="modified",
                    )
                )

    FED_df["Emotion_entropy"] = scaler.fit_transform(
        FED_df["Emotion_entropy"].values.reshape(-1, 1)
    ).flatten()
    FED_df["Meaning_entropy"] = scaler.fit_transform(
        FED_df["Meaning_entropy"].values.reshape(-1, 1)
    ).flatten()
    
    FED_df["Emotion_GV"] = scaler.fit_transform(
        FED_df["Emotion_GV"].values.reshape(-1, 1)
    ).flatten()
    FED_df["Meaning_GV"] = scaler.fit_transform(
        FED_df["Meaning_GV"].values.reshape(-1, 1)
    ).flatten()



    # save the results
    FED_df = FED_df[
        [
            "index",
            "emoji",
            "Unicode_meaning",
            "category",
            "Valence_mean",
            "Valence_std",
            "Arousal_mean",
            "Arousal_std",
            "Enjoyment_mean",
            "Enjoyment_std",
            "Surprise_mean",
            "Surprise_std",
            "Anger_mean",
            "Anger_std",
            "Disgust_mean",
            "Disgust_std",
            "Sadness_mean",
            "Sadness_std",
            "Fear_mean",
            "Fear_std",
            "Candidate_emotion",
            "Emotion_embedding",
            "Emotion_SA",
            "Emotion_SA_std",
            "Emotion_original_SV",
            "Emotion_modified_SV",
            "Emotion_entropy",
            "Emotion_GV",
            "Candidate_meaning",
            "Meaning_embedding",
            "Meaning_SA",
            "Meaning_SA_std",
            "Meaning_original_SV",
            "Meaning_modified_SV",
            "Meaning_entropy",
            "Meaning_GV",
        ]
    ]
    FED_df.to_excel("FED.xlsx", index=False)
    material_df.to_excel("正式实验材料+被试补充情绪与含义.xlsx", index=False)
    with open(emoji_vectors_counts_dir, "wb") as f:
        pkl.dump(emoji_vectors_counts, f)


if __name__ == "__main__":
    main()
