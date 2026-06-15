import pandas as pd
import json
import os
import numpy as np
import pingouin as pg
from tqdm import tqdm


def find_interval(
    df_path="./dataset_for_experiment_with_supplementary_descriptions_by_participants.xlsx",
):
    """return the interval of each emoji"""
    if os.path.exists("interval.json"):
        with open("interval.json") as file:
            interval = json.load(file)
        return interval


def reshape_icc_sheet(df):

    # 重命名列便于操作
    df = df.rename(
        columns={
            df.columns[0]: "Questionnaire",
            df.columns[1]: "Dimension",
            df.columns[2]: "ICC",
            df.columns[3]: "CI95",
        }
    )

    # 格式化单元格： "ICC [CI95]"
    df["ICC_formatted"] = df.apply(
        lambda row: f"{row['ICC']:.3f} {row['CI95']}", axis=1
    )

    # 透视：行=Table_ID, 列=Emotion, 值=格式化后的字符串
    result = df.pivot(
        index="Questionnaire", columns="Dimension", values="ICC_formatted"
    ).reset_index()

    # 将mean, SD, min, max 加入结果表，作为最后四列

    # # 可选：按情绪名称排序列（按你需要的顺序）
    # emotion_order = [
    #     "Valence",
    #     "Arousal",
    #     "Enjoyment",
    #     "Surprise",
    #     "Anger",
    #     "Disgust",
    #     "Sadness",
    #     "Fear",
    # ]
    # result = result[
    #     ["Questionnaire"] + [e for e in emotion_order if e in result.columns]
    # ]

    return result


def compute_summary(df_raw):
    """输入原始长格式df，输出每个情绪的汇总统计"""
    summary = (
        df_raw.groupby("Dimension")["ICC"]
        .agg(
            [
                ("Min", "min"),
                ("Max", "max"),
                ("Mean", "mean"),
                ("SD", "std"),  # 样本标准差 (ddof=1)
            ]
        )
        .round(3)
    )

    # 对行重新排序
    emotion_order = [
        "Valence",
        "Arousal",
        "Enjoyment",
        "Surprise",
        "Anger",
        "Disgust",
        "Sadness",
        "Fear",
    ]


    return summary.reset_index()


def main():
    interval = find_interval()

    input_dir = "./raw_questionaire_data"

    ICC_Ck = dict()
    ICC_Ak = dict()

    for table_index in tqdm(range(1, 18 + 1)):
        table_interval = interval[str(table_index)]
        table_path = os.path.join(input_dir, f"{table_index}.xlsx")
        if not os.path.exists(table_path):
            continue
        raw_table = pd.read_excel(table_path)
        # Drop the first 11 columns
        raw_table = raw_table.iloc[:, 11:]

        emoji_rating_dict = dict()

        for emoji_index, emoji_dict in table_interval.items():

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

            emoji_rating_dict[emoji_index] = df_rating

        for emotion in [
            "Valence",
            "Arousal",
            "Enjoyment",
            "Surprise",
            "Anger",
            "Disgust",
            "Sadness",
            "Fear",
        ]:
            emotion_table = {
                emoji_index: emoji_rating_dict[emoji_index][emotion].to_list()
                for emoji_index, _ in table_interval.items()
            }
            emotion_table = pd.DataFrame(emotion_table)

            # 目前每行是一个被试，每列是一个emoji
            # 转换为宽格式：每行一个emoji，每列一个被试
            wide_data = emotion_table.T

            # print(wide_data)

            wide_data.index.name = "emoji_id"

            # 转为长格式（pingouin 要求）
            long_data = (
                wide_data.reset_index()
                .melt(id_vars="emoji_id", var_name="rater_id", value_name="score")
                .dropna()
            )  # 自动剔除缺失值

            # 3. 计算ICC
            icc_table = pg.intraclass_corr(
                data=long_data, targets="emoji_id", raters="rater_id", ratings="score"
            )

            # print(icc_table)

            # 提取Type=="ICC(A,k)" 这一行的ICC和CI95
            icc_table.set_index("Type", inplace=True)
            ICC_Ak[(table_index, emotion)] = (
                icc_table.loc["ICC(A,k)"]["ICC"],
                icc_table.loc["ICC(A,k)"]["CI95"],
            )

            # print(ICC_Ak)

            # 提取Type=="ICC(C,k)" 这一行的ICC和CI95
            ICC_Ck[(table_index, emotion)] = (
                icc_table.loc["ICC(C,k)"]["ICC"],
                icc_table.loc["ICC(C,k)"]["CI95"],
            )

            # print(ICC_Ck)


    df_Ak = pd.DataFrame(ICC_Ak, index=["ICC", "CI95"]).T.reset_index()
    df_Ak.columns = ["Questionnaire", "Dimension", "ICC", "CI95"]

    sig_count = len(df_Ak[df_Ak["ICC"] >= 0.75])
    print(sig_count / len(df_Ak))

    Ak_summary = compute_summary(df_Ak)

    df_Ak = reshape_icc_sheet(df_Ak)

    df_Ck = pd.DataFrame(ICC_Ck, index=["ICC", "CI95"]).T.reset_index()
    df_Ck.columns = ["Questionnaire", "Dimension", "ICC", "CI95"]

    sig_count = len(df_Ck[df_Ck["ICC"] >= 0.75])
    print(sig_count / len(df_Ck))

    Ck_summary = compute_summary(df_Ck)

    df_Ck = reshape_icc_sheet(df_Ck)

    output_path = "./ICC_result.xlsx"
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_Ak.to_excel(writer, sheet_name="ICC(A,k)", index=False)
        Ak_summary.to_excel(writer, sheet_name="Summary(A,k)", index=False)
        df_Ck.to_excel(writer, sheet_name="ICC(C,k)", index=False)
        Ck_summary.to_excel(writer, sheet_name="Summary(C,k)", index=False)


if __name__ == "__main__":
    main()
