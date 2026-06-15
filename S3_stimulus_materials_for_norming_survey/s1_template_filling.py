import pandas as pd

with open("./introduction.txt",'r', encoding='utf-8') as f:
    introduction = f.read()

with open("./rating_template.txt",'r', encoding='utf-8') as f:
    rating_template = f.read()

with open("./agreement_template.txt",'r', encoding='utf-8') as f:
    agreement_template = f.read()


df = pd.read_excel("./emoji_set_for_experiment.xlsx") 

liar_check_1_template = "请直接选择{k}"

liar_check_2_template = ["邯郸校区最高的建筑物是：",
                         "复旦大学的现任校长是：",
                         "复旦大学的第一任校长是：",
                         "在复旦现行绩点制度下每个本科生班级最多有多少A：",
                         "请默写复旦校训的前半句：",
                         "请默写复旦校训的后半句：",
                         "复旦的理科图书馆在毛主席像的哪一侧（西侧还是东侧）：",
                         "《共产党宣言》是哪位复旦校长翻译的："] 

count = 0
number = 1
q_size = 20 # 每份问卷包含的Emoji

for index, row in df.iterrows():  
    if count % q_size == 0:
        number = count // q_size + 1
        file_name = "./Questionaire/questionaire_{number}.txt".format(number=number)
        with open(file_name,"w", encoding='utf-8') as f:
            f.write(introduction.format(number=number))
    
    emoji = row["emoji"]
    emotion_selected = row['emotion_selected']
    meaning_selected = row['meaning_selected']
    
    # 八个维度评分
    if count % q_size in {6,18}: # 测谎项
        rating_part = rating_template.format(emoji=emoji) + liar_check_1_template.format(k=count%7+1) + '\n'
    else:
        rating_part = rating_template.format(emoji=emoji) + '\n'

    # emotion
    if pd.isna(emotion_selected):
        emotion_part = '\n'
    else:
        emotion_part = agreement_template.format(emoji=emoji,field="情绪",choice='\n'.join(emotion_selected.split('、')))

    # meaning
    if pd.isna(meaning_selected):
        meaning_part = '\n'
    else:
        meaning_part = agreement_template.format(emoji=emoji,field="含义",choice='\n'.join(meaning_selected.split('、')))

    if count % q_size == 12:
        meaning_part = meaning_part + liar_check_2_template[(number-1)%len(liar_check_2_template)] + '\n'

    with open(file_name,"a", encoding='utf-8') as f:
        f.write('\n'.join([rating_part,emotion_part,meaning_part]))
    count += 1

    if count % q_size == 0 or count == 359:
        with open(file_name,"a", encoding='utf-8') as f:
            f.write('\n本问卷到此结束，感谢您的作答！回答完成后请您及时告知主试，谢谢！[段落说明]\n\n1.作答过程中如果发现问卷存在问题，欢迎您留下宝贵的改进意见，帮助我们提升问卷质量。如无意见请填写“无”：')
        
print(count)