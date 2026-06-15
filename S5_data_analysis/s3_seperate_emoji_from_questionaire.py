import pandas as pd
import json
import os
import numpy as np


def find_interval(
    df_path="./dataset_for_experiment_with_supplementary_descriptions_by_participants.xlsx",
):
    """return the interval of each emoji"""
    if os.path.exists("interval.json"):
        with open("interval.json") as file:
            interval = json.load(file)
        return interval

    count = 0
    q_size = 20  # 每份问卷包含的Emoji
    interval = dict()
    questionaire_dict = None
    number = 0

    df = pd.read_excel(df_path)

    for index, row in df.iterrows():
        if count % q_size == 0:
            if questionaire_dict:
                interval[number] = questionaire_dict
            number = count // q_size + 1
            col_index = 0  # new questionaire, reset the col_index
            questionaire_dict = dict()  # the dict of this questionaire

        emoji_index = row["index"]
        emoji = row["emoji"]
        emotion_selected = row["emotion_selected"]
        meaning_selected = row["meaning_selected"]

        emoji_dict = dict()
        emoji_dict["Emoji"] = emoji
        emoji_dict["Rating_interval"] = (col_index, col_index + 8)

        # 八个维度评分
        if count % q_size in {6, 18}:  # 客观测谎题
            col_index += 8 + 1
        else:
            col_index += 8

        # emotion
        if not pd.isna(emotion_selected):
            emo_len = len(emotion_selected.split("、"))
            emoji_dict["Emotion_interval"] = (
                col_index,
                col_index + emo_len + 2,
            )  # +2 一道模糊量表，一道主观补充题
            col_index += emo_len + 2
            emoji_dict["Emotion_selected"] = emotion_selected.split("、")
        else:
            emoji_dict["Emotion_interval"] = None

        # meaning
        if not pd.isna(meaning_selected):
            meaning_len = len(meaning_selected.split("、"))
            emoji_dict["Meaning_interval"] = (
                col_index,
                col_index + meaning_len + 2,
            )  # +2 一道模糊量表，一道主观补充题
            col_index += meaning_len + 2
            emoji_dict["Meaning_selected"] = meaning_selected.split("、")
        else:
            emoji_dict["Meaning_interval"] = None

        if count % q_size == 12:  # 主观测谎题
            col_index += 1

        questionaire_dict[emoji_index] = emoji_dict

        count += 1

    interval[str(number)] = questionaire_dict

    with open("interval.json", "w") as file:
        json.dump(interval, file, indent=4)

    print(count)

    with open("interval.json") as file:
        interval = json.load(file)

    return interval


def main():
    interval = find_interval()

    input_dir = "./raw_questionaire_data"
    output_dir = "./seperate_data_of_each_emoji_raw"

    input_dir = "./gender_comparison/raw_questionaire_data_male"
    output_dir = "./gender_comparison/seperate_data_of_each_emoji_raw_male"


    input_dir = "./gender_comparison/raw_questionaire_data_female"
    output_dir = "./gender_comparison/seperate_data_of_each_emoji_raw_female"


    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    for table_index in range(1, 18 + 1):
        table_interval = interval[str(table_index)]
        table_path = os.path.join(input_dir, f"{table_index}.xlsx")
        if not os.path.exists(table_path):
            continue
        raw_table = pd.read_excel(table_path)
        # Drop the first 11 columns
        raw_table = raw_table.iloc[:, 11:]
        for emoji_index, emoji_dict in table_interval.items():
            with pd.ExcelWriter(
                os.path.join(output_dir, f"{emoji_index}.xlsx"), engine="openpyxl"
            ) as writer:
                # Select the columns of this emoji
                df_rating = raw_table.iloc[
                    :,
                    emoji_dict["Rating_interval"][0] : emoji_dict["Rating_interval"][1],
                ]
                df_rating.columns = [
                    "Valence",
                    "Arousal",
                    "Enjoyment",
                    "Surprise",
                    "Anger",
                    "Disgust",
                    "Sadness",
                    "Fear",
                ]

                df_rating.to_excel(writer, sheet_name="Rating", index=False)
                if emoji_dict["Emotion_interval"]:
                    df_emotion = raw_table.iloc[
                        :,
                        emoji_dict["Emotion_interval"][0] : emoji_dict[
                            "Emotion_interval"
                        ][1],
                    ]
                    df_emotion.columns = emoji_dict["Emotion_selected"] + [
                        "Emotion_subjective_ambiguity",
                        "被试补充情绪",
                    ]
                    df_emotion.to_excel(writer, sheet_name="Emotion", index=False)
                if emoji_dict["Meaning_interval"]:
                    df_meaning = raw_table.iloc[
                        :,
                        emoji_dict["Meaning_interval"][0] : emoji_dict[
                            "Meaning_interval"
                        ][1],
                    ]
                    df_meaning.columns = emoji_dict["Meaning_selected"] + [
                        "Meaning_subjective_ambiguity",
                        "被试补充含义",
                    ]
                    df_meaning.to_excel(writer, sheet_name="Meaning", index=False)


if __name__ == "__main__":
    main()
