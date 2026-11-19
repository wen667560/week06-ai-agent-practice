import os ##用来读取电脑里的环境变量
from openai import OpenAI ##导入OpenAI库

# 第一步：读取硅基流动 API Key
api_key = os.getenv("SILICONFLOW_API_KEY") ##os.getnv("名字")：去电脑环境变量里去找叫 的值

if not api_key: ##未读取到密钥（空的）
    raise ValueError("没有读取到硅基流动 API Key")

# 第二步：连接硅基流动平台
client = OpenAI(   ##client=OpenAI():创建一个连接AI平台的客户端对象
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1" ##默认是连OPENAI官网，但是我的模型是在硅基流动平台
)

print("===============AI Python 助手==================")
question=input("请输入你的问题：")
#####对于同一个问题由于sysytem设定不一样，AI的回答风格也不同，这就是大模型AI中非常重要的Prompt提示词基础
# 第三步：调用 Qwen3-8B 模型
response = client.chat.completions.create(
    model="Qwen/Qwen3-8B",##指定模型
    messages=[
        {
            ##"role": "user",##role角色，告诉大模型是谁在说话，是用户说的
            ##"content": "你好，请用简单的语言介绍一下 Python，并举一个简单的例子。"##发给AI的提问内容
            "role":"system", ##system,设定AI身份、行为准则
            "content":"你是一名耐心的Python编程老师，请用中文回答。"
        },
        {
            "role": "user",
            ##"content":"什么是python变量？请举一个简单的例子。"
            "content":question
        }
    ]
)

# 第四步：输出 AI 的回答
print("===== AI 的回答 =====")
print(response.choices[0].message.content)
##response：AI返回给你的全部数据（文字，模型名、token消耗等）
##.choices[0]:取返回结果里第一条回答
##.message.content:提取AI回答的文字内容