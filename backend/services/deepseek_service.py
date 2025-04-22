# deepseek_api.py

import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# 加载 .env 文件中的环境变量
load_dotenv(find_dotenv())

DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_KEY:
    raise ValueError("please set in .env for DEEPSEEK_API_KEY")

class DeepSeekChatBot:
    def __init__(self, system_prompt: str = "You are a helpful assistant."):
        self.client = OpenAI(
            api_key=DEEPSEEK_KEY,
            base_url="https://api.deepseek.com"
        )
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]

    def send_message(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            stream=False
        )

        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def reset(self, system_prompt: str = "You are a helpful assistant."):
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]
