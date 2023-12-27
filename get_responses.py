from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def get_gpt4_response(system_prompt, user_prompt):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    # "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."
    system_prompt = "次のは、AIアシスタントとの会話です。このアシスタントは、親切で、クリエイティブで、優しいです。"
    user_prompt = "お名前はなんでしょうか?"
    print(get_gpt4_response(system_prompt, user_prompt))
