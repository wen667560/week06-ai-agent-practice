
# Python 大模型 API 与 Agent 实践

## 1. 项目介绍

本项目是一个基于 Python 的大模型应用开发学习项目。

通过调用硅基流动 API 和 Qwen3-8B 模型，学习大模型 API 调用、多轮对话、结构化输出、Function Calling、多工具调用和 Agent 工作流。

## 2. 技术栈

- Python 3.12
- OpenAI Python SDK
- SiliconFlow API
- Qwen3-8B
- VS Code
- Git
- GitHub

## 3. 项目文件说明

| 文件名 | 功能 |
|---|---|
| llm_api.py | 大模型 API 基础调用 |
| llm_chat.py | 多轮对话与上下文管理 |
| llm_params.py | 模型参数控制与 JSON 输出 |
| llm_tools.py | Function Calling |
| llm_multi_tools.py | 多工具调用 |
| llm_agent_workflow.py | Agent 多步工作流 |
| ai_assistant.py | AI 数学与文本助手综合项目 |

## 4. 环境要求

- Windows
- Python 3.12
- OpenAI Python SDK
- 可用的 SiliconFlow API Key

## 5. 安装依赖

```bash
pip install openai
```

## 6. 配置 API Key

在 Windows 环境变量中配置：

SILICONFLOW_API_KEY

不要将真实 API Key 上传到 GitHub。

## 7. 运行项目

进入项目目录：

```powershell
cd D:\Python_Practice\week06
```

运行综合项目：

```powershell
python ai_assistant.py
```

## 8. 学习成果

1. 掌握 Python 调用大模型 API。
2. 实现多轮对话。
3. 学习 Prompt 设计。
4. 使用 JSON 处理结构化数据。
5. 实现 Function Calling。
6. 实现多工具调用。
7. 理解 Agent 基础工作流。

## 9. 项目说明

本项目为个人学习实践项目，后续将持续完善。