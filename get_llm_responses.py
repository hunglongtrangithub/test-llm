from openai import OpenAI
import google.generativeai as genai
import os


def get_gpt4_response(system_prompt, user_prompt):
    client = OpenAI()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    response = client.chat.completions.create(model="gpt-4", messages=messages)
    message = response.choices[0].message.content
    return message


def get_gemini_response(system_prompt, user_prompt):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    messages = [
        # {"role": "system", "parts": [system_prompt]},
        {"role": "user", "parts": [system_prompt, user_prompt]},
    ]
    response = model.generate_content(messages)
    message = response.text
    return message


def get_llm_response(model_name, system_prompt, user_prompt):
    if model_name == "gpt-4":
        return get_gpt4_response(system_prompt, user_prompt)
    elif model_name == "gemini-pro":
        return get_gemini_response(system_prompt, user_prompt)
    base_url = "https://api.naga.ac/v1/"
    api_key = os.getenv("CHIMERA_GPT_KEY")
    client = OpenAI(base_url=base_url, api_key=api_key)
    messages = [
        {"role": "system", "content": system_prompt},
        # {"role": "user", "content": system_prompt + "\n" + user_prompt},
        {"role": "user", "content": user_prompt},
    ]
    response = client.chat.completions.create(model=model_name, messages=messages)
    message = response.choices[0].message.content
    return message


if __name__ == "__main__":
    # print("Available models:")
    # print("\n".join(fetch_chat_models()))
    # print()
    # "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."
    system_prompt = "You are an alien from outer space. You have come to Earth to learn about humans."
    user_prompt = "What is your name? What planet do you come from?"
    model_names = [
        "gpt-4",
        "gemini-pro",
        "gpt-3.5-turbo-0613",
        "llama-2-70b-chat",
        "llama-2-7b-chat",
        "code-llama-34b",
    ]
    for model_name in model_names:
        print(f"Model: {model_name}")
        response = get_llm_response(model_name, system_prompt, user_prompt)
        print(response)
        print()
