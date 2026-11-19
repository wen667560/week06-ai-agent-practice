
import os
import json
from openai import OpenAI

# 1. 连接 API
api_key = os.getenv("SILICONFLOW_API_KEY")

if not api_key:
    raise ValueError("没有读取到 API Key")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)

# 2. 定义计算工具
def calculate(a, b, operation):

    if operation == "add":
        return a + b

    elif operation == "subtract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":
        if b == 0:
            return "错误：不能除以零"
        return a / b

    return "不支持的运算"


# 3. 告诉 AI 工具的使用方式
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行两个数字的加减乘除运算",
            "parameters": {
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
                "required": ["a", "b", "operation"]
            }
        }
    }
]


# 4. 执行工具
def run_tool(name, arguments):

    if name == "calculate":
        return calculate(
            arguments["a"],
            arguments["b"],
            arguments["operation"]
        )

    return "未知工具"


# 5. 用户输入任务
question = input("请告诉 AI 你想完成什么任务：")

messages = [
    {
        "role": "system",
        "content": """
你是一个能够分步骤完成任务的数学助手。

规则：
1. 如果任务包含计算，必须使用计算工具。
2. 如果任务有多个计算步骤，必须按顺序执行。
3. 后一步需要使用前一步的计算结果。
4. 工具返回结果后，再决定下一步。
5. 最后向用户总结完整过程和答案。
"""
    },
    {
        "role": "user",
        "content": question
    }
]


# 6. Agent 工作循环
max_rounds = 6

for step in range(max_rounds):

    print(f"\n========== 第 {step + 1} 轮 ==========")

    response = client.chat.completions.create(
        model="Qwen/Qwen3-8B",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.1,
        max_tokens=1000
    )

    assistant_message = response.choices[0].message

    # AI 不再调用工具，说明任务可能完成
    if not assistant_message.tool_calls:

        print("\n===== 任务执行结束 =====")
        print(assistant_message.content)

        break

    # 保存 AI 的工具调用信息
    messages.append(
        assistant_message.model_dump(exclude_none=True)
    )

    # 执行 AI 请求的工具
    for tool_call in assistant_message.tool_calls:

        name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        print("AI 选择工具：", name)
        print("工具参数：", arguments)

        result = run_tool(name, arguments)

        print("工具执行结果：", result)

        # 把执行结果交给 AI
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(
                {"result": result},
                ensure_ascii=False
            )
        })

else:
    print("任务达到最大执行轮数，请检查任务是否完成。")