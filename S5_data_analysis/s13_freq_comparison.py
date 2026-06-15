import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


def compare_distribution(df, freq_col, emoji_col,title, xlabel,filename):

    df_FED = pd.read_excel("./FED.xlsx")

    # 计算重合数量

    emoji_FED = set(df_FED["emoji"])

    emoji_target = set(df[emoji_col])

    overlap_num = len(emoji_FED.intersection(emoji_target))

    print("重合数量：", overlap_num)

    df["Interval of emoji frequency in target database"] = pd.qcut(
        df[freq_col],
        q=4,
        labels=[r"75%-100%", r"50%-75%", r"25%-50%", r"0%-25%"],
        duplicates="drop",
    )

    print(df.head())

    # print(df_ferre["频率区间"].value_counts())

    # ---------------------- 统计集合A中单词在各区间的数量分布 ----------------------
    # 筛选出FED中的emoji
    df_overlap = df[df[emoji_col].isin(emoji_FED)]

    # 统计每个频率区间的单词数量
    interval_counts = df_overlap[
        "Interval of emoji frequency in target database"
    ].value_counts()

    print(interval_counts)

    # ---------------------- 4. 绘制柱状图展示分布 ----------------------

    # 创建柱状图
    plt.figure(figsize=(12, 6))
    bars = plt.bar(
        interval_counts.index, interval_counts.values, color="#1f77b4", alpha=0.8
    )

    # 添加数值标签（在柱子上方显示数量）
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.05,
            f"{int(height)}",
            ha="center",
            va="bottom",
        )

    # 设置图表标题和轴标签
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel("Number of emoji in FED", fontsize=12)
    # plt.xticks(rotation=45)  # 旋转x轴标签，避免重叠
    plt.grid(axis="y", linestyle="--", alpha=0.3)  # 添加y轴网格线
    plt.tight_layout()  # 调整布局，防止标签被截断
    plt.savefig(f"./images/{filename}.png", dpi=600)

    # 显示图表
    plt.show()

    # 打印统计结果（便于查看具体数值）
    print(interval_counts)


def main():
    df = pd.read_excel("./previous_dataset/Emoji-Sp.xlsx")
    freq_col = "freq"
    emoji_col = "emoji"
    title = "The number of Emoji from FED in each interval partitioned by the frequency in Emoji‑SP database"
    xlabel = "Interval of emoji frequency in Emoji‑SP database"
    file_name = "FED_vs_Emoji-SP_freq_distribution.png"
    compare_distribution(df, freq_col, emoji_col, title, xlabel,file_name)


    df = pd.read_excel("../corpus_freq_count/CCI2_freq.xlsx")
    freq_col = "total_count"
    emoji_col = "emoji"
    title = "The number of Emoji from FED in each interval partitioned by the frequency in CCI 2.0 database"
    xlabel = "Interval of emoji frequency in CCI 2.0 database"
    file_name = "FED_vs_CCI2_freq_distribution.png"
    compare_distribution(df, freq_col, emoji_col, title, xlabel,file_name)


    # df = pd.read_excel("./previous_dataset/Scheffler2024.xlsx")
    # freq_col = "Twitter_frequency"
    # emoji_col = "unicode_char"
    # title = "The number of Emoji from FED in each interval \npartitioned by the Twitter frequency in Scheffler&Nenchev(2024) database"
    # xlabel = "Interval of emoji Twitter frequency in Scheffler2024 database"
    # file_name = "FED_vs_Scheffler2024_Twitter_freq_distribution.png"
    # compare_distribution(df, freq_col, emoji_col, title, xlabel,file_name)

    # df = pd.read_excel("./previous_dataset/Scheffler2024.xlsx")
    # freq_col = "Twitter_frequency"
    # emoji_col = "unicode_char"
    # title = "The number of Emoji from FED in each interval \npartitioned by the WhatsApp frequency in Scheffler&Nenchev(2024) database"
    # xlabel = "Interval of emoji WhatsApp frequency in Scheffler2024 database"
    # file_name = "FED_vs_Scheffler2024_whatsapp_freq_distribution.png"
    # compare_distribution(df, freq_col, emoji_col, title, xlabel,file_name)


if __name__ == "__main__":
    main()
