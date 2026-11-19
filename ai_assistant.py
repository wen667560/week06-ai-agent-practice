
import os
import json
from openai import OpenAI

# ==========================
# 1. 连接大模型 API
# ==========================

api_key = os.getenv("SILICONFLOW_API_KEY")

if not api_key:
    raise ValueError("没有读取到硅基流动 API Key")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)

MODEL_NAME = "Qwen/Qwen3-8B"


# ==========================
# 2. 定义 Python 工具
# ==========================

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


def count_text_length(text):

    return len(text)


# ==========================
# 3. 向 AI 描述可用工具
# ==========================

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算两个数字的加减乘除",
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
    },
    {
        "type": "function",
        "function": {
            "name": "count_text_length",
            "description": "统计文字的字符数量，包含空格",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string"
                    }
                },
                "required": ["text"]
            }
        }
    }
]


# ==========================
# 4. Python 工具执行分发
# ==========================

def run_tool(name, arguments):

    if name == "calculate":

        return calculate(
            arguments["a"],
            arguments["b"],
            arguments["operation"]
        )

    elif name == "count_text_length":

        return count_text_length(
            arguments["text"]
        )

    else:

        return "未知工具"


# ==========================
# 5. 保存对话上下文
# ==========================

messages = [
    {
        "role": "system",
        "content": """
你是一个可靠的 AI 助手。

你可以回答普通问题，也可以使用工具。

规则：
1. 数学计算必须使用 calculate 工具。
2. 统计文字长度必须使用 count_text_length 工具。
3. 工具结果返回后，根据真实结果回答。
4. 保留前面的对话上下文。
5. 不要编造工具执行结果。
"""
    }
]


# ==========================
# 6. 主程序：持续对话
# ==========================

print("================================")
print("       AI 数学与文本助手")
print("================================")
print("可以计算、统计文字，也可以普通聊天。")
print("输入 exit 退出程序。")


while True:

    question = input("\n你：").strip()

    if question.lower() == "exit":

        print("AI：再见！")

        break

    if not question:

        print("请输入有效的问题。")

        continue

    messages.append({
        "role": "user",
        "content": question
    })

    try:

        # 最多进行 5 轮工具调用
        for step in range(5):

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.2,
                max_tokens=1000
            )

            assistant_message = response.choices[0].message

            # 不需要调用工具，直接回答
            if not assistant_message.tool_calls:

                answer = assistant_message.content or "暂时无法生成回答。"

                print("\nAI：", answer)

                messages.append({
                    "role": "assistant",
                    "content": answer
                })

                break

            # 保存 AI 的工具调用消息
            messages.append(
                assistant_message.model_dump(exclude_none=True)
            )

            # 执行工具
            for tool_call in assistant_message.tool_calls:

                function_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                print("\n[工具调用]", function_name)
                print("[工具参数]", arguments)

                result = run_tool(
                    function_name,
                    arguments
                )

                print("[工具结果]", result)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        {"result": result},
                        ensure_ascii=False
                    )
                })

        else:

            print("\nAI：工具调用达到最大轮数，请简化问题。")

    except Exception as e:

        print("\n程序发生错误：", e)

        # 删除本轮未完成的对话，避免错误上下文影响后续对话
        if messages and messages[-1]["role"] == "user":
            messages.pop()