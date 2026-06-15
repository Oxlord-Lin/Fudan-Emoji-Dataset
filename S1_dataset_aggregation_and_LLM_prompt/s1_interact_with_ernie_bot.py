import json
import pandas as pd
import requests
import json

file_name = "MLE_union_KK_union_weibo.xlsx"


def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
        
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=WWvdZSefpDkQ7zaMZdYWmsUH&client_secret=4PaG74rzfmXcY8HOkSKSLF1yDz2CtVoG"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")




def ask_Q(INPUT):
        
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed?access_token=" + get_access_token()
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": """
                请你以一个经常使用emoji进行沟通聊天的网友的身份，回答一些你关于emoji的认知情况的问题。接下来，我会向你提供多个emoji。你需要完成下述任务：

                1. 根据你目前所学到的包含该emoji的文本，思考这个emoji表达哪些常见的情绪，具有哪些常见的含义。。

                2. 给出3个例句，这3个例句都必须且只能包含我给定的emoji。每个例句中，我给定的emoji出现次数只能为1次。3个例句中的emoji的用法和情感要尽可能不同，要展现出这个emoji的常见情绪和常见含义。emoji在可以出现在例句的包括开头、中间和结尾。这些例句需要做到情感生动丰富。

                在之后的问答中，你都需要严格按照下面的格式进行回答，请注意，所有给出的例句都必须在开头和结尾处使用“##”进行分界：

                你接下来的回答需要遵循这样的格式：
                ""
                emoji：
                例句一：##例句##
                例句二：##例句##
                例句三：##例句##
                ""
                """
            },
            {
                "role": "assistant",
                "content": "好的，我将会以一个经常使用emoji进行沟通聊天的网友的身份，回答你的问题。请你给出emoji"
            },
            {
                "role": "user",
                "content": "🤍"
            },
            {
                "role": "assistant",
                "content": """
                emoji：🤍
                例句一：##每次看到你，我的心里都充满了这份纯净的爱🤍##
                例句二：##谢谢你一直以来的陪伴和支持，我对你的感激之情🤍无法用言语表达##
                例句三：##🤍在这个特别的日子里，我想对你说，你是我生命中最美好的存在。##
                """
            },
            {
                "role": "user",
                "content": "🤧"
            },
            {
                "role": "assistant",
                "content": """
                emoji：🤧
                例句一：##今天天气太冷了，我鼻子都冻红了，还一直流鼻涕🤧##
                例句二：##🤧一不小心在众人面前摔倒了，真是尴尬得要命，真希望地上有个洞能钻进去。##
                例句三：##听了他的故事，我感动得几乎要哭🤧出来，真是太感人了！##
                """
            },
            {
                "role": "user",
                "content": INPUT
            },
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.json().get("result")
    print(result)
    return  result

def get_examples(emoji):
    return ask_Q(emoji)

# with open("prompt.txt",'r')  as f:
#     regulation = f.read()

# def send_regulation():
#     return ask_Q(regulation)

df = pd.read_excel(file_name)

df['raw'] = df['raw'].astype(str)

def main():

    # send_regulation()

    for index, row in df.iterrows():
        
        if row['label'] != -1:
            continue

        emoji = row["emoji"]
        print("\n查询第{index}个emoji：{emoji}".format(index=index,emoji=emoji))

        df.at[index,"raw"] = get_examples(emoji)

    df.to_excel(file_name,index=False)

if __name__ == "__main__":
    main()