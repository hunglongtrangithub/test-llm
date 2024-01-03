from openai import OpenAI
import google.generativeai as genai
import os
from helper import save_json_file, load_json_file


def get_gpt4_response(system_prompt, user_prompt):
    client = OpenAI()
    messages = [
        # {"role": "user", "content": system_prompt},
        {"role": "user", "content": system_prompt + "\n" + user_prompt},
    ]
    # messages = [
    #     {"role": "system", "content": system_prompt},
    #     {"role": "user", "content": user_prompt},
    # ]
    # print(messages)
    response = client.chat.completions.create(model="gpt-4", messages=messages)
    message = response.choices[0].message.content
    print(message)
    return message


def get_gemini_response(system_prompt, user_prompt):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    messages = [
        # {"role": "system", "parts": [system_prompt]},
        {"role": "user", "parts": [system_prompt, user_prompt]},
    ]
    # print(messages)
    response = model.generate_content(messages)
    message = response.text
    print(message)
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
    print(message)
    return message


def collect_llm_responses(
    model_name: str,
    system_prompt: str,
    make_user_prompt: callable,
    patient_name: str,
    document_name: str,
    questions: dict[str, str],
) -> dict[str, str]:
    # Check if the document exists
    try:
        document = open(f"input/{patient_name}/{document_name}.txt", "r").read()
    except FileNotFoundError as e:
        # Raise an error
        raise FileNotFoundError(
            f"Document {document_name} for patient {patient_name} not found"
        ) from e
    # Check if the responses have already been collected
    try:
        responses = load_json_file(f"llm_responses/{patient_name}/{document_name}.json")
    except FileNotFoundError:
        # Initialize the dictionary
        responses = {}
    print(f"Collecting responses of {model_name} for {document_name}")
    model_responses = {}
    for question_type, question in questions.items():
        # Construct the user prompt
        user_prompt = make_user_prompt(question, document)
        # Get the response
        response = get_llm_response(model_name, system_prompt, user_prompt)
        # Add the response to the dictionary
        model_responses[question_type] = response
    # Save the responses
    responses[model_name] = model_responses
    save_json_file(f"llm_responses/{patient_name}/{document_name}.json", responses)
    # Return the model responses
    return model_responses


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
