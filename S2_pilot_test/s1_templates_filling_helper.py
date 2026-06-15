import pandas as pd

with open("./introduction.txt",'r', encoding="utf-8") as f:
    introduction = f.read()

with open("./template.txt",'r', encoding="utf-8") as f:
    template = f.read()


df = pd.read_excel("../aggregation_of_dataset_and_interation_with_Ernie_bot/MLE_union_KK_union_weibo.xlsx")

liar_check_1_template = "请直接选择{k}"

liar_check_2_template = "4.请直接填写“有”"

count = 0
number = 1

for _, row in df.iterrows():  
    label = row['label']
    if label == 0:
        continue
    if count % 30 == 0 and number != 12:
        number = count // 30 + 1
        file_name = "./Questionaire/templates_filled_number_{number}.txt".format(number=number)
        with open(file_name,"w", encoding="utf-8") as f:
            f.write(introduction.format(number=number))
    
    emoji = row["emoji"]
    ex1 = row["ex1"]
    ex2 = row["ex2"]
    ex3 = row["ex3"] 
    if count % 30 == 15: # 量表题的测谎项出现在第16题
        question_group = template.format(emoji=emoji,ex1=ex1,ex2=ex2,ex3=ex3,
                                    liar_check_1=liar_check_1_template.format(k=number%6+1), liar_check_2='\n')
    elif count % 30 == 22: # 主观题的测谎项出现在第23题
        question_group = template.format(emoji=emoji,ex1=ex1,ex2=ex2,ex3=ex3,
                                    liar_check_1='\n',liar_check_2=liar_check_2_template)
    else:
        question_group = template.format(emoji=emoji,ex1=ex1,ex2=ex2,ex3=ex3,
                                    liar_check_1='\n',liar_check_2='\n')
        
    with open(file_name,"a", encoding="utf-8") as f:
        f.write(question_group)

    count += 1
        
print(count)