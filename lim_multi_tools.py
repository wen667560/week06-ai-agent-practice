
##用户提出问题->AI判断需要那个工具->Python 执行工具->执行结果返回AI


import os
import json
from openai import OpenAI

# 1. 连接硅基流动 API
api_key = os.getenv("SILICONFLOW_API_KEY")

if not api_key:
    raise ValueError("没有读取到硅基流动 API Key")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)

# 2. 工具一：数学计算
def calculate(a, b, operation):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return "错误：除数不能为零"
        return a / b
    else:
        return "不支持的运算类型"


# 3. 工具二：统计文字长度
def count_text_length(text):
    return len(text)


# 4. 告诉 AI：现在有哪些工具可以使用
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算两个数字的加减乘除",
            "parameters": {    ##parameters参数规则
                "type": "object",
                "properties": {  
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                    "operation": {
                        "type": "string",
                        "enum": [
                            "add",
                            "subtract",
                            "multiply",
                            "divide"
                        ]
                    }
                },
                "required": ["a", "b", "operation"]   ##required这些参数必须传
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_text_length",
            "description": "统计用户提供的文字有多少个字符",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "需要统计的文字"
                    }
                },
                "required": ["text"]
            }
        }
    }
]


# 5. Python 根据 AI 的选择执行对应工具
def run_tool(function_name, arguments):

    if function_name == "calculate":
        return calculate(
            arguments["a"],
            arguments["b"],
            arguments["operation"]
        )

    elif function_name == "count_text_length":
        return count_text_length(arguments["text"])

    else:
        return "不支持的工具"


# 6. 接收用户的问题
question = input("请输入你的问题：")

messages = [
    {
        "role": "system",
        "content": (
            "你是一个智能助手。"
            "如果问题涉及数学计算，使用 calculate 工具。"
            "如果问题涉及统计文字字符数量，使用 count_text_length 工具。"
            "必须根据工具返回的结果回答，不要编造结果。"
        )
    },
    {
        "role": "user",
        "content": question
    }
]


# 7. 开始 Agent 工具调用流程
for round_number in range(5):

    response = client.chat.completions.create(
        model="Qwen/Qwen3-8B",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.1,
        max_tokens=800
    )

    assistant_message = response.choices[0].message

    # 如果 AI 不需要工具，就直接回答
    if not assistant_message.tool_calls:
        print("\n===== AI 最终回答 =====")
        print(assistant_message.content)
        break

    # 保存 AI 的工具调用信息
    messages.append(
        assistant_message.model_dump(exclude_none=True)
    )

    # 逐个执行 AI 请求的工具
    for tool_call in assistant_message.tool_calls:

        function_name = tool_call.function.name
        arguments = json.loads(
            tool_call.function.arguments
        )

        print("\nAI 决定调用工具：", function_name)
        print("工具参数：", arguments)

        result = run_tool(function_name, arguments)

        print("Python 执行结果：", result)

        # 把工具结果交还给 AI
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(
                {"result": result},
                ensure_ascii=False
            )
        })

else:
    print("\n工具调用轮数达到上限，请重新提问。")