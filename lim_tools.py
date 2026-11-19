

##AI决定调用-python执行-结果返回AI-AI组织回答，Tool Calling的核心流程
##tool_choice="auto"  让AI自行判断是否使用工具    tool_calls查看AI是否请求调用工具    
# json.loads()解析AI给出的工具参数     role="tool"将工具执行结果交还给AI
# 为何需要第二次调用大模型：让AI根据工具执行结果组织最终回答     



import os 
import json
from openai import OpenAI
#1.读取API KEY
api_key=os.getenv("SILICONFLOW_API_KEY")
if not api_key:
    raise ValueError("")
#2.创建客户端
client=OpenAI(api_key=api_key,base_url="https://api.siliconflow.cn/v1")
#3.创建一个python工具函数
def calculate(a,b,operation):
    """执行基础数学计算"""
    if operation=="add":
        return a+b
    elif operation=="subtract":
        return a-b
    elif operation=="multiply":
        return a*b
    elif operation=="divide":
        if b==0:  
            return "错误：除数不能为0"
        return a/b
    else:
        return "不支持的运算类型"

#4.告诉AI可以使用什么工具
tools=[
    {
        "type":"function",
        "function":{
            "name":"calculate",
            "description":"执行两个数字的加减乘除运算",
            "parameters":{
                "type":"object",
                "properties":{
                    "a":{
                        "type":"number",
                        "description":"第一个数字"
                    },
                    "b":{
                        "type":"number",
                        "description":"第二个数字"
                    },
                    "operation":{
                        "type":"string",
                        "enum":[
                            "add",
                            "subtract",
                            "multiply",
                            "divide"
                        ],
                        "description":"运算类型"
                    }
                },
                "required":["a","b","operation"]
            }
        }
    }
]

#5.接受用户问题
question=input("请输入计算问题：")
messages=[
    {
        "role":"system",
        "content":"你是一个计算助手。遇到加减乘除问题时，优先使用计算工具，不要自己猜测结果。"  
    },
    {
        "role":"user",
        "content":question
    }
]
#6.第一次请求：让AI判断是否调用工具
response=client.chat.completions.create(
    model="Qwen/Qwen3-8B",
    messages=messages,
    tools=tools,
    tool_choice="auto", #auto让AI自己决定，auto自动，none禁止调用工具，required强制调用
    temperature=0.1,
    max_tokens=500
)
assistant_message=response.choices[0].message
#7.判断AI是否要求调用工具
if assistant_message.tool_calls:
    print("\nAI决定调用工具")
    messages.append(
        assistant_message.model_dump(exclude_none=True)
    )
#8.python真正执行工具
for tool_call in assistant_message.tool_calls:
    function_name=tool_call.function.name
    arguments=json.loads(tool_call.function.arguments)
    print("调用的工具：",function_name)
    print("工具参数",arguments)
    if function_name=="calculate":
        result=calculate(arguments["a"],arguments["b"],arguments["operation"])
    else:
        result="不支持的工具"
    print("python执行结果：",result)
    #9.把工具执行结果交还给AI
    messages.append({
        "role":"tool",
        "tool_call_id":tool_call.id,
        "content":json.dumps(
                {"result":result},
                ensure_ascii=False
                )
    })
    #10.第二次请求：AI根据工具结果组织回答
    final_response=client.chat.completions.create(
        model="Qwen/Qwen3-8B",
        messages=messages,
        temperature=0.1,
        max_tokens=500
    )
    print("=================AI最终回答=====================")
    print(final_response.choices[0].message.content)
else:
    print("\n=========AI回答=============")
    print(assistant_message.content)