# -*- coding: UTF-8 -*-
# @Author  ：Leezed
# @Date    ：2025/8/10 16:04

from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI


# 自定义工具：查询天气
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    if city.lower() == "beijing":
        return "The weather in Beijing is sunny with a high of 25°C."
    elif city.lower() == "shanghai":
        return "The weather in Shanghai is cloudy with a high of 22°C."
    else:
        return "Sorry, I don't have weather information for that location."


# 初始化LLM
llm = ChatOpenAI(
    base_url="https://api.deepseek.com",
    model="deepseek-chat"
)

# 初始化Agent
agent = create_react_agent(
    model=llm,
    tools=[get_weather],
    prompt="You are a helpful assistant"
)

# 用户输入
user_input = "What is the weather like in Beijing today?"

if __name__ == '__main__':
    # 运行Agent并逐步展示推理过程
    for step in agent.stream({"messages": [{"role": "user", "content": user_input}]}):
        print(step)
