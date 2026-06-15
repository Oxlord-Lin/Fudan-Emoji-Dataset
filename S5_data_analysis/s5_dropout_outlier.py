import os
import pandas as pd
import numpy as np
import pandas as pd


def drop_out_outlier(x, mean, std, threshold=3):
    if x < mean - threshold * std or x > mean + threshold * std:
        return np.nan
    else:
        return x


emotions = [
    "Valence",
    "Arousal",
    "Enjoyment",
    "Surprise",
    "Anger",
    "Disgust",
    "Sadness",
    "Fear",
]


drop_out_count = dict.fromkeys(
    emotions
    + ["emotion_term", "meaning_term"]
    + ["Emotion_subjective_ambiguity", "Meaning_subjective_ambiguity"],
    0,
)

drop_out_min_ratio = dict.fromkeys(
    emotions
    + ["emotion_term", "meaning_term"]
    + ["Emotion_subjective_ambiguity", "Meaning_subjective_ambiguity"],
    1.0,
)

drop_out_max_ratio = dict.fromkeys(
    emotions
    + ["emotion_term", "meaning_term"]
    + ["Emotion_subjective_ambiguity", "Meaning_subjective_ambiguity"],
    0.0,
)


total_sample_count = 0

total_emotion_term_count = 0
total_meaning_term_count = 0

for file in os.listdir("./seperate_data_of_each_emoji_raw"):
    # process the "Rating" sheet
    dfs = pd.read_excel(f"./seperate_data_of_each_emoji_raw/{file}", sheet_name=None)
    df_rating = dfs["Rating"]
    total_sample_count += len(df_rating)
    for emotion in df_rating.columns:
        # for values in this emotion column, drop the values out of 3 sd
        mean = df_rating[emotion].mean()
        std = df_rating[emotion].std()
        df_rating[emotion] = df_rating[emotion].apply(
            drop_out_outlier, args=(mean, std)
        )
        drop_out_count[emotion] += df_rating[emotion].isna().sum()

        drop_out_ratio = df_rating[emotion].isna().sum() / len(df_rating)
        if drop_out_ratio > drop_out_max_ratio[emotion]:
            drop_out_max_ratio[emotion] = drop_out_ratio
        if drop_out_ratio < drop_out_min_ratio[emotion]:
            drop_out_min_ratio[emotion] = drop_out_ratio

    # process the "Emotion" sheet if it this sheet exists
    if "Emotion" in dfs:

        df_emotion = dfs["Emotion"]
        # the columns are : emotion_term(several columns) + Emotion_subjective_ambiguity
        # find the index of Emotion_subjective_ambiguity and the range of emotion_term columns
        Emotion_subjective_ambiguity_index = df_emotion.columns.get_loc(
            "Emotion_subjective_ambiguity"
        )

        # print(Emotion_subjective_ambiguity_index)

        Emotion_term_drop_count_for_this_emoji = 0
        total_emotion_term_count += len(df_emotion) * Emotion_subjective_ambiguity_index
        for index in range(Emotion_subjective_ambiguity_index):
            col = df_emotion.columns[index]
            mean = df_emotion[col].mean()
            std = df_emotion[col].std()
            df_emotion[col] = df_emotion[col].apply(drop_out_outlier, args=(mean, std))
            Emotion_term_drop_count_for_this_emoji += df_emotion[col].isna().sum()
        drop_out_count["emotion_term"] += Emotion_term_drop_count_for_this_emoji
        drop_out_ratio = Emotion_term_drop_count_for_this_emoji / (
            len(df_emotion) * Emotion_subjective_ambiguity_index
        )
        if drop_out_ratio > drop_out_max_ratio["emotion_term"]:
            drop_out_max_ratio["emotion_term"] = drop_out_ratio
        if drop_out_ratio < drop_out_min_ratio["emotion_term"]:
            drop_out_min_ratio["emotion_term"] = drop_out_ratio

        # process Emotion_subjective_ambiguity_index column
        mean = df_emotion["Emotion_subjective_ambiguity"].mean()
        std = df_emotion["Emotion_subjective_ambiguity"].std()
        df_emotion["Emotion_subjective_ambiguity"] = df_emotion[
            "Emotion_subjective_ambiguity"
        ].apply(drop_out_outlier, args=(mean, std))
        drop_out_count["Emotion_subjective_ambiguity"] += (
            df_emotion["Emotion_subjective_ambiguity"].isna().sum()
        )
        drop_out_ratio = df_emotion["Emotion_subjective_ambiguity"].isna().sum() / len(
            df_emotion
        )
        if drop_out_ratio > drop_out_max_ratio["Emotion_subjective_ambiguity"]:
            drop_out_max_ratio["Emotion_subjective_ambiguity"] = drop_out_ratio
        if drop_out_ratio < drop_out_min_ratio["Emotion_subjective_ambiguity"]:
            drop_out_min_ratio["Emotion_subjective_ambiguity"] = drop_out_ratio

    # process the "Meaning" sheet if it this sheet exists
    if "Meaning" in dfs:

        df_meaning = dfs["Meaning"]
        # the columns are : meaning_term(several columns) + Meaning_subjective_ambiguity
        # find the index of Meaning_subjective_ambiguity and the range of meaning_term columns
        Meaning_subjective_ambiguity_index = df_meaning.columns.get_loc(
            "Meaning_subjective_ambiguity"
        )
        # print(Meaning_subjective_ambiguity_index)

        Meaning_term_drop_count_for_this_emoji = 0
        total_meaning_term_count += len(df_meaning) * Meaning_subjective_ambiguity_index
        for index in range(Meaning_subjective_ambiguity_index):
            col = df_meaning.columns[index]
            mean = df_meaning[col].mean()
            std = df_meaning[col].std()
            df_meaning[col] = df_meaning[col].apply(drop_out_outlier, args=(mean, std))
            Meaning_term_drop_count_for_this_emoji += df_meaning[col].isna().sum()
        drop_out_count["meaning_term"] += Meaning_term_drop_count_for_this_emoji
        drop_out_ratio = Meaning_term_drop_count_for_this_emoji / (
            len(df_meaning) * Meaning_subjective_ambiguity_index
        )
        if drop_out_ratio > drop_out_max_ratio["meaning_term"]:
            drop_out_max_ratio["meaning_term"] = drop_out_ratio
        if drop_out_ratio < drop_out_min_ratio["meaning_term"]:
            drop_out_min_ratio["meaning_term"] = drop_out_ratio

        # process Meaning_subjective_ambiguity_index column
        mean = df_meaning["Meaning_subjective_ambiguity"].mean()
        std = df_meaning["Meaning_subjective_ambiguity"].std()
        df_meaning["Meaning_subjective_ambiguity"] = df_meaning[
            "Meaning_subjective_ambiguity"
        ].apply(drop_out_outlier, args=(mean, std))
        drop_out_count["Meaning_subjective_ambiguity"] += (
            df_meaning["Meaning_subjective_ambiguity"].isna().sum()
        )
        drop_out_ratio = df_meaning["Meaning_subjective_ambiguity"].isna().sum() / len(
            df_meaning
        )
        if drop_out_ratio > drop_out_max_ratio["Meaning_subjective_ambiguity"]:
            drop_out_max_ratio["Meaning_subjective_ambiguity"] = drop_out_ratio
        if drop_out_ratio < drop_out_min_ratio["Meaning_subjective_ambiguity"]:
            drop_out_min_ratio["Meaning_subjective_ambiguity"] = drop_out_ratio

    print(f"{file} processed")
    # save the processed data into one excel file
    with pd.ExcelWriter(f"./seperate_data_of_each_emoji/{file}") as writer:
        df_rating.to_excel(writer, sheet_name="Rating", index=False)
        if "Emotion" in dfs:
            df_emotion.to_excel(writer, sheet_name="Emotion", index=False)
        if "Meaning" in dfs:
            df_meaning.to_excel(writer, sheet_name="Meaning", index=False)

    # break

# print("drop_out_min_raio:")
# for k, v in drop_out_min_ratio.items():
#     print(f"{k}: {v}")

print()
print("drop_out_max_raio:")
for k, v in drop_out_max_ratio.items():
    print(f"{k}: {v}")
print()
print("average drop_out ratio")
for emotion in emotions:
    print(f"{emotion}: {drop_out_count[emotion]/total_sample_count}")

print(f"emotion_term: {drop_out_count['emotion_term']/total_emotion_term_count}")
print(f"meaning_term: {drop_out_count['meaning_term']/total_meaning_term_count}")
print(
    f"Emotion_subjective_ambiguity: {drop_out_count['Emotion_subjective_ambiguity']/total_sample_count}"
)
print(
    f"Meaning_subjective_ambiguity: {drop_out_count['Meaning_subjective_ambiguity']/total_sample_count}"
)
