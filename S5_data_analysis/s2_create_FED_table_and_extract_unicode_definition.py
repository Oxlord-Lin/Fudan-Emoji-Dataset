import pandas as pd

df = pd.read_excel("dataset_for_experiment_with_supplementary_descriptions_by_participants.xlsx")
# df = pd.read_excel("./FED.xlsx")

dict_emoji_meaning = {}

count = 0
with open("emoji_unicode.txt",'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        if '#' in line and ";" in line and 'E' in line:
            emoji_and_meaning = line.split('#')[-1]
            emoji_and_meaning = emoji_and_meaning.split(' ',maxsplit=3)
            try:
                emoji = emoji_and_meaning[1]
                meaning = emoji_and_meaning[-1]
                dict_emoji_meaning[emoji] = meaning
                count += 1
            except Exception:
                continue

# print(count)
# print(dict_emoji_meaning)

df['Unicode_meaning'] = df['emoji'].apply(lambda x: dict_emoji_meaning.get(x, ''))

df = df[['index','emoji','Unicode_meaning']]



df.to_excel("FED.xlsx", index=False)