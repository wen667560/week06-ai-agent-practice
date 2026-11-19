import os
from openai import OpenAI
api_key=os.getenv("SILICONFLOW_API_KEY")
if not api_key:
    raise ValueError("没有读取到API Key")
client=OpenAI(api_key=api_key,base_url="https://api.siliconflow.cn/v1")
messages=[
    {
        "role":"system",
        "content":"你是一名耐心的网络工程专业老师，擅长解释计算机网络、数据库和python，请用中文回答。"
    }
]
print("================AI网络工程助手===============")
print("可以连续提问，输入 exit 或 退出 结束进程")

#### [system,user1,assistant1,user2,assistant2,...] user是用户说的话 assistant是AI说的话



while True:
    question=input("\n你：")
    if question.lower()=='exit' or question=="退出":
        print("AI:再见，欢迎下次使用！")
        break
    if not question.split():
        print("请输入有效信息")
        continue
    messages.append(
        {
            "role":"user",
            "content":question
        }
    )
    try:
        response=client.chat.completions.create(
            model="Qwen/Qwen3-8B",
            messages=messages
        )
        answer=response .choices[0].message.content
        print("\nAI:",answer)
        messages.append(
            {
                "role":"assistant", ##assisatant的作用是展现AI的回答
                "content":answer
            }
        )
    except Exception as e:
        print("请求出现错误",e)
        messages.pop()   ##失败了就无效，要删除