import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.pyplot as plt
import cv2 as cv
from typing import List, Tuple
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from scipy import stats
from scipy.stats import t as t_dist
from scipy.stats import gaussian_kde
from collections import Counter
import re
# from translate import Translator

# translator = Translator(from_lang="zh", to_lang="en")


# 设置中文字体
# plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
# plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号

# set environment variable for TF_ENABLE_ONEDNN_OPTS to be 0
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# from text2vec import SentenceModel
# model = SentenceModel()


def word2vec(words: List[str]):
    """return the embedding vector of each word in the List of words"""
    from text2vec import SentenceModel

    model = SentenceModel()
    vectors = model.encode(words)
    return vectors


def calculate_embedding_vector_variation(
    vectors: np.ndarray, counts: List[float], mode="original"
):
    """Calculate the variation of the emotiong or meaning embedding vectors."""

    def cos_similarity(v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    if mode == "original":
        weights = [count / sum(counts[1:]) for count in counts[1:]]
        baseline = vectors[0]
        cos_similarity = np.array(
            [cos_similarity(baseline, target) for target in vectors[1:]]
        )
        cos_distantce = 1 - cos_similarity
        embedding_variation = np.inner(weights, cos_distantce)
        return embedding_variation

    if mode == "modified":
        weights = [count / sum(counts) for count in counts]
        baseline = np.mean(vectors, axis=0)
        cos_similarity = np.array(
            [cos_similarity(baseline, target) for target in vectors]
        )
        cos_distantce = 1 - cos_similarity
        embedding_variation = np.inner(weights, cos_distantce)
        return embedding_variation


def calculate_entropy(choice_count: List[Tuple[str, int]]):
    count = np.array([item[1] for item in choice_count])
    prob = count / sum(count)
    entropy = -np.sum(prob * np.log2(prob))
    return entropy


def calculate_generalized_variation(design_matrix: np.ndarray, mode="det"):
    if design_matrix.shape[1] == 1:  # only one dimension
        # return the ordinary variance
        # omit the nan values
        design_matrix = np.asarray([x for x in design_matrix if not np.isnan(x)])
        return np.var(design_matrix)
    # cov = np.cov(design_matrix, rowvar=False)
    design_matrix_df = pd.DataFrame(design_matrix)
    cov = design_matrix_df.cov()
    if mode == "det":
        return np.linalg.det(cov)
    elif mode == "trace":
        return np.trace(cov)


def count_added_item(s: pd.Series):
    c = Counter(s)
    if "无" in c.keys():
        c.pop("无")
    c = sorted(c.items(), key=lambda x: x[1], reverse=True)
    # return the c as a string with the format "item1(count1)，item2(count2)"
    return "；".join([f"{item[0]}({item[1]})" for item in c])


def translate_terms(terms: str):
    """translate the terms to Chinese"""
    if not isinstance(terms, str):
        return ""
    terms_list = terms.split(";")
    candidates_list = [c.split("(")[0] for c in terms_list]
    for _ in range(2):
        en_candiates_list = [translator.translate(c) for c in candidates_list]
        # 去除末尾的标点符号，如果有的话
        en_candiates_list = [re.sub(r"[\.\!\?;]$", "", c) for c in en_candiates_list]
        # 检查是否列表中的所有元素都是英文字符或者空格或者连字符
        all_en = all(re.match("^[a-zA-Z\s-]+$", c) for c in en_candiates_list)
        if all_en:
            break
    all_en = all(re.match("^[a-zA-Z\s-]+$", c) for c in en_candiates_list)
    if not all_en:
        print(en_candiates_list)
    if all_en:
        # 将所有字母转换为小写
        en_candiates_list = [c.lower() for c in en_candiates_list]
        # 去除首尾的空格
        en_candiates_list = [c.strip() for c in en_candiates_list]

    scores = [float(c.split("(")[1].split(")")[0]) for c in terms_list]
    return ";".join(
        [
            f"{en_candiates_list[i]}({scores[i]:.2f})"
            for i in range(len(en_candiates_list))
        ]
    )

    # return translator.translate(terms)


def get_emoji_img(emoji_index):
    image = cv.imread(
        os.path.join("./emoji_image", f"{emoji_index}.png"), cv.IMREAD_UNCHANGED
    )
    # 检查图像是否有alpha通道
    if image.shape[2] == 4:
        # 分离BGR和alpha通道
        bgr_image = image[:, :, :3]
        alpha_channel = image[:, :, 3]

        # 创建一个掩码，用于标识透明像素（alpha为0）
        mask = alpha_channel == 0

        # 将透明像素设置为白色
        bgr_image[mask] = [255, 255, 255]

        return cv.cvtColor(bgr_image, cv.COLOR_BGR2RGB)

    else:
        print(f"The image {emoji_index}.png has no alpha channel!")


def plot_valence_arousal_relationship(
    x_data,
    y_data,
    confidence_level=0.95,
    title="Arousal-Valence relashionship",
    output_dir="./images",
):
    # sort the data by x_data
    x_data = x_data.sort_values()
    # sor the data with the same order of x_data
    y_data = y_data.reindex(x_data.index)

    # fit the data with a quadratic function
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(x_data.values.reshape(-1, 1))
    model = LinearRegression()
    model.fit(X_poly, y_data)
    y_fit = model.predict(X_poly)

    # plot the data points
    plt.scatter(x_data, y_data, label="Data Points")

    # plot the fitted quadratic curve
    xx = np.linspace(x_data.min(), x_data.max(), 100)
    yy = model.predict(poly.fit_transform(xx.reshape(-1, 1)))
    plt.plot(xx, yy, label="Fitted Curve", color="blue")

    # calculate the confidence bands
    t_value = t_dist.ppf(1 - (1 - confidence_level) / 2, df=len(x_data) - 2)
    se = np.sqrt(np.sum((y_fit - y_data) ** 2) / (len(x_data) - 2))
    y_upper = yy + t_value * se
    y_lower = yy - t_value * se

    # plot the confidence bands
    plt.fill_between(xx, y_lower, y_upper, alpha=0.25, color="blue")

    # add labels and legend
    plt.xlabel("Valence")
    plt.ylabel("Arousal")
    plt.legend()
    plt.title(title)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{title}.png"))
    # plt.show()


def density_estimation(
    df: pd.DataFrame, title: str, labels: List[str], output_dir="./images", style=None
):
    # Estimate the density of each column using kernel density estimation
    # 使用Seaborn绘制KDE曲线
    plt.figure(figsize=(10, 8))

    # 对每一列进行KDE估计并绘制
    for index, column in enumerate(df.columns):
        data = df[column].dropna()
        kde = gaussian_kde(data, bw_method="scott")  # 使用Scott方法计算带宽
        x = np.linspace(data.min(), data.max(), 1000)  # 生成x轴数据
        y = kde(x)  # 计算KDE值
        if style is None:
            sns.lineplot(x=x, y=y, label=labels[index], linestyle="--", linewidth=2)
        else:
            line_style = style[index][0]
            line_color = style[index][1]
            sns.lineplot(
                x=x,
                y=y,
                label=labels[index],
                linestyle=line_style,
                color=line_color,
                linewidth=2,
            )

    # 添加标题和标签
    plt.title(title, fontdict={"fontsize": 22})
    plt.xlabel("Value")
    plt.ylabel("Density", fontdict={"fontsize": 18})
    plt.legend(prop={"size": 16})  # 显示图例
    plt.grid(True)  # 添加网格

    # 显示图形
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{title}.png"))
    # plt.show()


def plot_correlation_matrix(
    df, title="Correlation Matrix", labels=None, output_dir="./images"
):
    # calculate the correlation matrix of spearman correlation
    corr_matrix = df.corr("spearman")

    # extract the column names
    column_names = list(df.columns)

    # # mask the diagonal elements of the correlation matrix
    # mask = np.eye(corr_matrix.shape[0], dtype=bool)

    # plot the correlation matrix
    plt.figure(figsize=(10, 10))
    if labels:
        sns.heatmap(
            corr_matrix,
            annot=True,
            # mask=mask,
            cmap="Blues",
            xticklabels=labels,
            yticklabels=labels,
            square=True,
            cbar=False,
            annot_kws={"size": 28},  # 设置字体大小
        )
    else:
        sns.heatmap(
            corr_matrix,
            annot=True,
            # mask=mask,
            cmap="Blues",
            xticklabels=column_names,
            yticklabels=column_names,
            square=True,
            cbar=False,
            annot_kws={"size": 28},  # 设置字体大小
        )
    # heatmap不展示图例

    # 设置yticklabels字体大小
    plt.yticks(fontsize=16)
    plt.xticks(fontsize=16)

    # 旋转x轴标签
    plt.xticks(rotation=30)
    # 旋转y轴标签
    plt.yticks(rotation=-60)

    plt.title(title, fontdict={"fontsize": 28})
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{title}.png"))
    # plt.show()


def plot_emoji_2D(
    df: pd.DataFrame,
    title="Emoji ploted on Arousal-Valence 2D space",
    n_cluster=4,
    labels=["Valence", "Arousal"],
    outpu_dir="./images",
):
    df = df.dropna(inplace=False)
    # selecet the second and third columns of the dataframe
    df_2D = df.iloc[:, [1, 2]]
    # get the colum names of df_2D
    column_names = list(df_2D.columns)
    # plot the data points on the 2D space
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(1, 7)
    ax.set_ylim(1, 7)
    if n_cluster > 0:
        # normalize the data
        df_2D = (df_2D - df_2D.mean()) / df_2D.std()
        # cluster the data
        kmeans = KMeans(n_clusters=n_cluster, random_state=2024, n_init=10).fit(df_2D)
        df["cluster"] = kmeans.labels_
        # df.to_excel('emoji_cluster.xlsx')
        cmap = plt.cm.get_cmap("rainbow")
        norm = plt.Normalize(vmin=0, vmax=len(df["cluster"].unique()) - 1)
        colors = cmap(norm(df["cluster"].astype(int)))
        # plot the data points with different colors, use circle marker instead of point marker
        scatter = ax.scatter(
            df_2D[:, 0],
            df_2D[:, 1],
            s=800,
            edgecolor=colors,
            facecolor="none",
            linewidth=2,
            alpha=0.25,
        )

    # plot the emoji images on the same plot, on the top layer of the plot
    for i, row in df.iterrows():
        print(row["index"])
        emoji_img = get_emoji_img(row["index"])
        ax.imshow(
            emoji_img,
            extent=[
                row[column_names[0]] - 0.12,
                row[column_names[0]] + 0.12,
                row[column_names[1]] - 0.12,
                row[column_names[1]] + 0.12,
            ],
            alpha=1,
        )

    plt.title(title, fontdict={"fontsize": 22})
    plt.xlabel(labels[0], fontdict={"fontsize": 18})
    plt.ylabel(labels[1], fontdict={"fontsize": 18})
    plt.tight_layout()
    plt.savefig(os.path.join(outpu_dir, f"{title}.png"))
    plt.show()


def rescale(data: np.array, min_val=1, max_val=7):
    min_data = np.min(data)
    max_data = np.max(data)
    return (max_val - min_val) * (data - min_data) / (max_data - min_data) + min_val


def PCA_and_plot(
    df: pd.DataFrame,
    title="PCA of Ekman's Emotions",
    n_cluster=4,
    labels=["PCA1", "PCA2"],
    output_dir="./images",
):
    """Reduce the dimensionality of the Ekman' emotion using PCA and plot the result"""
    df = df.copy(deep=True)
    # drop the rows with missing values of Enjoyment_mean
    df.dropna(subset=["Enjoyment_mean"], inplace=True)
    df_Ekman = df[
        [
            "Enjoyment_mean",
            "Surprise_mean",
            "Anger_mean",
            "Disgust_mean",
            "Sadness_mean",
            "Fear_mean",
        ]
    ]
    scaler = StandardScaler()
    df_Ekman_scaled = scaler.fit_transform(df_Ekman)
    pca = PCA(n_components=6)
    pca.fit(df_Ekman_scaled)
    # plot the scree plot to check the number of principal components
    eigenvalues = pca.explained_variance_
    plt.figure(figsize=(10, 10))
    plt.plot(np.arange(1, len(eigenvalues) + 1), eigenvalues, marker="o", linewidth=2)
    # plt.xlabel("主成分个数", fontsize=18)
    plt.xlabel("Number of Principal Components", fontsize=18)
    # plt.ylabel("归一化协方差矩阵特征值", fontsize=18)
    plt.ylabel("Normalized Eigenvalues of the Covariance Matrix", fontsize=18)
    # plt.title("6种基本情绪的PCA碎石图", size=24)
    plt.title("PCA Scree Plot", size=22)
    plt.axhline(y=1, color="r", linestyle="--", linewidth=2)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"Scree Plot.png"))
    plt.show()

    # plot the emoji based on the first two principal components
    principal_components = pca.transform(df_Ekman_scaled)
    # scale the PCA result to [1, 7]
    df["PCA1"] = rescale(principal_components[:, 0])
    df["PCA1"] = 8 - df["PCA1"]
    df["PCA2"] = rescale(principal_components[:, 1])

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0.5, 7.5)
    ax.set_ylim(0.5, 7.5)
    if n_cluster > 0:
        # cluster the data
        kmeans = KMeans(n_clusters=n_cluster, random_state=2024, n_init=10).fit(
            df[["PCA1", "PCA2"]]
        )
        df["cluster"] = kmeans.labels_
        df.to_excel("emoji_cluster_by_PCA.xlsx")
        cmap = plt.cm.get_cmap("rainbow")
        norm = plt.Normalize(vmin=0, vmax=len(df["cluster"].unique()) - 1)
        colors = cmap(norm(df["cluster"].astype(int)))
        # plot the data points with different colors, use circle marker instead of point marker
        scatter = ax.scatter(
            df["PCA1"],
            df["PCA2"],
            s=800,
            edgecolor=colors,
            facecolor="none",
            linewidth=2,
            alpha=0.25,
        )

    # plot the emoji images on the same plot, on the top layer of the plot
    for i, row in df.iterrows():
        emoji_img = get_emoji_img(row["index"])
        ax.imshow(
            emoji_img,
            extent=[
                row["PCA1"] - 0.12,
                row["PCA1"] + 0.12,
                row["PCA2"] - 0.12,
                row["PCA2"] + 0.12,
            ],
            alpha=1,
        )

    # 计算第一主成分和第二主成分对方差的贡献度
    pca1_var_ratio = pca.explained_variance_ratio_[0]
    pca2_var_ratio = pca.explained_variance_ratio_[1]

    plt.title(title, fontdict={"fontsize": 22})
    plt.xlabel(labels[0] + f" ({pca1_var_ratio*100 :.0f}%)", fontdict={"fontsize": 18})
    plt.ylabel(labels[1] + f" ({pca2_var_ratio*100 :.0f}%)", fontdict={"fontsize": 18})
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{title}.png"))
    plt.show()

    return principal_components


def tsne_and_plot(
    df: pd.DataFrame,
    vectors: np.array,
    title="t-SNE of Emotion vectors",
    n_cluster=4,
    labels=["t-SNE1", "t-SNE2"],
    output_dir="./images",
):
    """Given a 2-dim numpy array, each row represents a vector,
    use t-SNE to reduce the dimensionality and plot the result on a 2D space
    and the df is used to get acces to the emoji images."""
    df = df.copy(deep=True)
    # nomalize each row of the vectors
    vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
    # calculate the cosine similarity matrix
    similarity_matrix = np.dot(vectors, vectors.T)
    distance_matrix = 1 - similarity_matrix
    # use t-SNE to reduce the dimensionality
    tsne = TSNE(n_components=2, random_state=2024)
    vectors_2d = tsne.fit_transform(distance_matrix)

    # plot the emoji based on the t-sne result
    # scale the t-SNE result to [1, 7]
    df["t-SNE1"] = rescale(vectors_2d[:, 0])
    df["t-SNE2"] = rescale(vectors_2d[:, 1])

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0.5, 7.5)
    ax.set_ylim(0.5, 7.5)
    if n_cluster > 0:
        # cluster the data
        kmeans = KMeans(n_clusters=n_cluster, random_state=2024, n_init=10).fit(
            df[["t-SNE1", "t-SNE2"]]
        )
        df["cluster"] = kmeans.labels_
        df.to_excel("emoji_cluster_by_tsne.xlsx")
        cmap = plt.cm.get_cmap("rainbow")
        norm = plt.Normalize(vmin=0, vmax=len(df["cluster"].unique()) - 1)
        colors = cmap(norm(df["cluster"].astype(int)))
        # plot the data points with different colors, use circle marker instead of point marker
        scatter = ax.scatter(
            df["t-SNE1"],
            df["t-SNE2"],
            s=800,
            edgecolor=colors,
            facecolor="none",
            linewidth=2,
            alpha=0.25,
        )

    # plot the emoji images on the same plot, on the top layer of the plot
    for i, row in df.iterrows():
        emoji_img = get_emoji_img(row["index"])
        ax.imshow(
            emoji_img,
            extent=[
                row["t-SNE1"] - 0.12,
                row["t-SNE1"] + 0.12,
                row["t-SNE2"] - 0.12,
                row["t-SNE2"] + 0.12,
            ],
            alpha=1,
        )

    plt.title(title, fontdict={"fontsize": 22})
    plt.xlabel(labels[0], fontdict={"fontsize": 18})
    plt.ylabel(labels[1], fontdict={"fontsize": 18})
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{title}.png"))
    plt.show()


def spearman_correlation_table(df, output_file=None):
    """
    计算DataFrame中所有字段间的Spearman相关系数，并生成格式化表格。
    表格对角线及上方留白，下方显示相关系数和显著性标记。

    参数:
    df (pd.DataFrame): 输入的DataFrame，需包含数值型字段
    output_file (str, optional): Excel输出文件路径，若为None则不保存

    返回:
    pd.DataFrame: 格式化后的相关系数表格
    """
    # 计算Spearman相关系数和p值
    corr_matrix, p_matrix = stats.spearmanr(df, nan_policy="omit")

    # 创建相关系数和p值的DataFrame
    corr_df = pd.DataFrame(corr_matrix, index=df.columns, columns=df.columns)
    p_df = pd.DataFrame(p_matrix, index=df.columns, columns=df.columns)
    print(corr_df)
    print(p_df)

    # 创建空的结果DataFrame
    result = pd.DataFrame("", index=df.columns, columns=df.columns)

    # 填充对角线下方的相关系数和显著性标记
    for i in range(len(df.columns)):
        for j in range(i):
            corr = corr_matrix[i, j]
            p_value = p_matrix[i, j]

            # 根据p值添加显著性标记
            if p_value < 0.001:
                sig_marker = "***"
            elif p_value < 0.01:
                sig_marker = "**"
            elif p_value < 0.05:
                sig_marker = "*"
            else:
                sig_marker = ""

            # 格式化相关系数并添加显著性标记
            result.iloc[i, j] = f"{corr:.3f}{sig_marker}"

    # 保存到Excel文件(如果指定了输出路径)
    if output_file:
        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            result.to_excel(writer, sheet_name="Spearman Correlation")
            print(f"相关系数表格已保存至 {output_file}")

    return result


def plot_spearman_heatmap(
    data: pd.DataFrame,
    title="Spearman Correlation Matrix",
    figsize=(12, 10),
    annot=True,
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    show_significance=True,
    square=True,
    cbar_kws=None,
    annot_kws=None,
    save_path=None,
    column_names=None,
):
    """
    绘制Spearman相关性矩阵的热力图（只显示对角线以下部分）

    参数:
    data (pd.DataFrame): 输入数据，每行是一个样本，每列是一个特征
    title (str): 热力图标题
    figsize (tuple): 图像大小
    annot (bool): 是否在热力图上标注相关系数值
    cmap (str): 颜色映射名称
    vmin (float): 颜色映射的最小值
    vmax (float): 颜色映射的最大值
    show_significance (bool): 是否标记显著相关的单元格
    square (bool): 是否使热力图单元格为正方形
    cbar_kws (dict): 颜色条的额外参数
    annot_kws (dict): 标注文本的额外参数
    save_path (str): 图像保存路径，为None则不保存
    column_names (list): 可选，用户指定的列名列表，长度应与data的列数相同

    返回:
    fig, ax:  matplotlib的图像和轴对象
    corr_matrix: Spearman相关系数矩阵
    p_matrix: 对应的p值矩阵
    """
    # 计算Spearman相关系数和p值
    corr_matrix, p_matrix = stats.spearmanr(data, nan_policy="omit")

    # 创建下三角掩码（只显示对角线以下部分）
    # mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    mask = np.eye(len(data.columns), dtype=bool)

    # 确定使用的列名（用户指定或数据自带）
    if column_names is not None:
        if len(column_names) != data.shape[1]:
            raise ValueError("column_names的长度必须与data的列数相同")
        cols = column_names
    else:
        cols = data.columns

    # 转换为DataFrame并设置列名和索引
    corr_matrix = pd.DataFrame(corr_matrix, columns=cols, index=cols)
    p_matrix = pd.DataFrame(p_matrix, columns=cols, index=cols)

    # 设置默认参数
    if cbar_kws is None:
        cbar_kws = {"shrink": 0.75, "label": "Spearman Correlation"}
    if annot_kws is None:
        annot_kws = {"size": 18,"color":"black"}

    # 创建图形
    plt.figure(figsize=figsize)
    ax = plt.gca()

    # 绘制热力图（只显示下三角部分）
    heatmap = sns.heatmap(
        corr_matrix,
        annot=annot,
        fmt=".3f",
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        square=square,
        mask=mask,
        cbar_kws=cbar_kws,
        annot_kws=annot_kws,
        ax=ax,
    )

    # 设置行列标签字体大小
    ax.tick_params(axis="both", which="major", labelsize=16)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=30)

    # 如果需要标记显著性，将星号放在相关系数下方
    if show_significance and annot:  # 只有在显示相关系数时才添加星号
        # 获取热力图的单元格坐标
        for i in range(len(corr_matrix.columns)):
            for j in range(len(corr_matrix.columns)):
                if i != j:
                    p_value = p_matrix.iloc[i, j]
                    # 根据p值添加显著性标记
                    if p_value < 0.001:
                        sig_marker = "***"
                    elif p_value < 0.01:
                        sig_marker = "**"
                    elif p_value < 0.05:
                        sig_marker = "*"
                    else:
                        sig_marker = ""
                    # 调整y坐标使星号位于相关系数下方
                    ax.text(
                        j + 0.5,
                        i + 0.75,
                        sig_marker,
                        ha="center",
                        va="center",
                        color="black",
                        fontsize=14,
                        fontweight="bold",
                    )

    # 加入显著性星号说明
    significance_text = "* p < .05, ** p < .01, *** p < .001"
    plt.figtext(0.5, -0.01, significance_text,
    ha="center", fontsize=12,
    bbox=dict(facecolor='none', edgecolor='none', pad=40.0))
    
    # 设置标题和布局
    plt.title(title, fontsize=20, pad=20)
    plt.tight_layout()

    # 保存图像
    # save_path = f"./images/{title}.png"
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        
    plt.show()

    # return plt.gcf(), ax, corr_matrix, p_matrix
