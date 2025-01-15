import openai
from openai import OpenAI
import google.generativeai as genai
import json
import os
from helper import save_json_file, load_json_file


def get_vicuna_response(model_name, system_prompt, user_prompt):
    if model_name not in [
        "vicuna-7b-v1.5",
        "vicuna-13b-v1.5",
        "vicuna-7b-v1.5-16k",
        "vicuna-13b-v1.5-16k",
        "vicuna-33b-v1.3",
    ]:
        raise ValueError(f"Model {model_name} not supported.")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.base_url = "http://localhost:8000/v1/"
    messages = [
        {"role": "user", "content": system_prompt + "\n" + user_prompt},
    ]
    response = openai.chat.completions.create(model=model_name, messages=messages)
    message = response.choices[0].message.content
    return message


def get_gpt_response(model_name, system_prompt, user_prompt):
    if model_name not in ["gpt-4", "gpt-3.5-turbo-0613"]:
        raise ValueError(f"Model {model_name} not supported.")
    client = OpenAI()
    messages = [
        {"role": "user", "content": system_prompt + "\n" + user_prompt},
    ]
    response = client.chat.completions.create(model="gpt-4", messages=messages)
    message = response.choices[0].message.content
    return message


def get_gemini_response(system_prompt, user_prompt):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    messages = [
        {"role": "user", "parts": [system_prompt, user_prompt]},
    ]
    response = model.generate_content(messages)
    message = response.text
    return message


def get_llm_response(model_name, system_prompt, user_prompt):
    if model_name in ["gpt-4", "gpt-3.5-turbo-0613"]:
        return get_gpt_response(model_name, system_prompt, user_prompt)
    elif model_name == "gemini-pro":
        return get_gemini_response(system_prompt, user_prompt)
    elif model_name in [
        "vicuna-7b-v1.5",
        "vicuna-13b-v1.5",
        "vicuna-7b-v1.5-16k",
        "vicuna-13b-v1.5-16k",
        "vicuna-33b-v1.3",
    ]:
        return get_vicuna_response(model_name, system_prompt, user_prompt)
    base_url = "https://api.naga.ac/v1/"
    api_key = os.getenv("CHIMERA_GPT_KEY")
    client = OpenAI(base_url=base_url, api_key=api_key)
    messages = [
        {"role": "user", "content": system_prompt + "\n" + user_prompt},
    ]
    response = client.chat.completions.create(model=model_name, messages=messages)
    message = response.choices[0].message.content
    return message


def load_local_llm_responses(patient_name, document_name):
    # Construct the file path for the local responses
    file_path = f"llm_responses/{patient_name}/{document_name}.json"

    # Load the local responses from a JSON file
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            responses = json.load(file)
        return responses
    else:
        raise FileNotFoundError(f"Response file {file_path} not found.")


def collect_llm_responses(
    model_name: str,
    system_prompt: str,
    user_prompt_template: str,
    patient_name: str,
    document_name: str,
    questions: dict[str, str],
) -> dict[str, str]:
    try:
        document = open(f"input/{patient_name}/{document_name}.txt", "r").read()
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Document {document_name} for patient {patient_name} not found"
        ) from e
    try:
        responses = load_json_file(f"llm_responses/{patient_name}/{document_name}.json")
    except FileNotFoundError:
        responses = {}
    print(f"Collecting responses of {model_name} for {document_name}")
    model_responses = {}
    for question_type, question in questions.items():
        print("Question type: ", question_type)
        user_prompt = user_prompt_template.format(question=question, document=document)
        response = get_llm_response(model_name, system_prompt, user_prompt)
        print("Response: ", response)
        model_responses[question_type] = response
    responses[model_name] = model_responses
    save_json_file(f"llm_responses/{patient_name}/{document_name}.json", responses)
    return model_responses


if __name__ == "__main__":
    system_prompt = "Your task is to analyze the provided medical document and answer the following question accurately. Only answer with relevant information from the document and present your answer in the specified format. Pay close attention to the format requirements for the question to ensure your response align with the expected structure. Your goal is to provide a clear, concise, and correctly formatted answer based on the content of the document. Avoid extraneous details to ensure your answer is clear, concise, and correctly formatted, directly reflecting the document's content."
    document = open("input/fake_patient1/fake_patient1_doc1_RAD.txt", "r").read()
    question = "What is the principal date of the medical document as noted in the text, formatted as 'Month DD, YYYY at HH:MM'?" 
    user_prompt = f"{question}\n{document}"
    model_names = [
        # "gpt-4",
        "gemini-pro",
        # "gpt-3.5-turbo-0613",
        # "llama-2-70b-chat",
        # "llama-2-7b-chat",
        # "llama-2-13b-chat",
    ]
    for model_name in model_names:
        print(f"Model: {model_name}")
        response = get_llm_response(model_name, system_prompt, user_prompt)
        print(response)
        print()
