import pandas as pd
import numpy as np
import pickle as pkl
import os

from utils import tsne_and_plot


def main():
    IMAGE_OUTPUT_DIR = "./images/"

    # read the data
    df = pd.read_excel("./FED.xlsx")
    
    emoji_vectors_counts_dir = "./emoji_vectors_counts.pkl"
    if os.path.exists(emoji_vectors_counts_dir):
        with open(emoji_vectors_counts_dir, "rb") as f:
            emoji_vectors_counts = pkl.load(f)
    else:
        raise FileNotFoundError

    # t-sne
    # select all the rows where Emotion_agreement is not missing
    emotion_vectors = []
    df_emo = df[df["Emotion_agreement"].notna()]
    for index, row in df_emo.iterrows():
        average_vector = emoji_vectors_counts[row["index"]]["Average_emotion_vectors"]
        emotion_vectors.append(average_vector)
    emotion_vectors = np.array(emotion_vectors)
    tsne_and_plot(
        df_emo,
        emotion_vectors,
        # title="情绪嵌入向量的t-SNE降维结果",
        title="t-SNE of Emotion Embeddings",
        n_cluster=0,
    )

    # emotion_features = df_emo[
    #     [
    #         "Valence_mean",
    #         "Arousal_mean",
    #         "Enjoyment_mean",
    #         "Surprise_mean",
    #         "Anger_mean",
    #         "Disgust_mean",
    #         "Sadness_mean",
    #         "Fear_mean",
    #     ]
    # ]
    # emotion_features = emotion_features.to_numpy()
    # tsne_and_plot(
    #     df_emo, emotion_features, title="t-SNE of Emotional Features", n_cluster=3
    # )

    # select all the rows where Meaning_agreement is not missing
    meaning_vectors = []
    df_mean = df[df['Meaning_agreement'].notna()]
    for index, row in df_mean.iterrows():
        average_vector = emoji_vectors_counts[row["index"]]["Average_meaning_vectors"]
        meaning_vectors.append(average_vector)
    meaning_vectors = np.array(meaning_vectors)
    tsne_and_plot(
        df_mean,
        meaning_vectors,
        # title="含义嵌入向量的t-SNE降维结果",
        title="t-SNE of Meaning Embeddings",
        n_cluster=0,
    )
    
if __name__ == "__main__":
    main()