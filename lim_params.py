import os 
import json
from openai import OpenAI
#1.读取API KEY
api_key=os.getenv("SILICONFLOW_API_KEY")
if not api_key:
    raise ValueError("")
#2.创建客户端
client=OpenAI(api_key=api_key,base_url="https://api.siliconflow.cn/v1")
#3.向AI提问题
question="什么是计算机网络？请介绍它的基本作用。"
#4.调用大模型
response=client.chat.completions.create(
    model="Qwen/Qwen3-8B",
    messages=[
        {
            "role":"system",
            "content": """
            你是一名计算机网络老师。
            请根据用户问题回答。
            你必须只返回合法的JSON，不要添加Markdown 代码块。
            JSON必须包含以下字段：
            question:字符串，用户的问题 
            answer:字符串，问题的详细回答 
            key_points:知识点列表 
            code_example:相关代码示例，没有代码时填写空字符串
            """
        },
        {
            "role":"user",
            "content":question
        }
    ],temperature=0.2,max_tokens=500 ##temperature取值0~1，越趋近0回答稳定固定严谨，越趋向1回答脑洞大开
)                    ## max_token控制回答长度，限制最多输出500个token
#5.获取AI返回内容
answer=response.choices[0].message.content
print("====================AI原始回答======================")
print(answer)
#6.将JSON字符串转化为python字典
try:
    data=json.loads(answer)
    print("\n==============提取结构化数据================")
    print("回答：",data["question"])
    print("回答：",data["answer"])
    print("\n知识点：")
    for point in data["key_points"]:
        print("-",point)
    print("\n代码示例：")
    print(data["code_example"])
except json.JSONDecodeError:
    print("\nJSON解析失败，请检查 AI 返回的内容")
except KeyError as e:
    print("\n返回结果缺少字段",e)