from get_answer_keys import load_answer_keys
from get_llm_responses import get_llm_response
from get_evaluation_results import compare_responses_with_keys
import json
import os

# SYSTEM_PROMPT = "Your task is to analyze the provided medical document and answer the following questions accurately. For each question, only answer with relevant information from the document and present your answers in the specified format. Pay close attention to the format requirements for each question to ensure your responses align with the expected structure. Your goal is to provide clear, concise, and correctly formatted answers based on the content of the document."
SYSTEM_PROMPT = "Your task is to analyze the provided medical document and answer the following question accurately. Only answer with relevant information from the document and present your answer in the specified format. Pay close attention to the format requirements for the question to ensure your response align with the expected structure. Your goal is to provide a clear, concise, and correctly formatted answer based on the content of the document."
MODEL_LIST = [
    "gpt-4",
    "gemini-pro",
    "gpt-3.5-turbo-0613",
    "llama-2-70b-chat",
    "llama-2-7b-chat",
    "code-llama-34b",
]


def get_patient_to_document_names(
    path: str = "input", patient_name: str = None
) -> list[tuple[str, str]]:
    # The path must contain only subdirectories as patients and only .txt files in each subdirectory as documents
    patient_document_names = []
    if patient_name is not None:
        # Get the document names for the patient
        for filename in os.listdir(f"{path}/{patient_name}"):
            if filename.endswith(".txt"):
                document_name = os.path.splitext(filename)[0]
                patient_document_names.append((patient_name, document_name))
        return patient_document_names
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(".txt"):
                patient_name = os.path.basename(dirpath)
                patient_document_names.append((patient_name, filename))
    return patient_document_names


def load_questions():
    return json.load(open("questions.json", "r"))


def make_user_prompt(question, document_name):
    # Find the index of the second underscore in the string
    second_underscore_index = document_name.find("_", document_name.find("_") + 1)
    # Get the patient name
    patient_name = document_name[:second_underscore_index]
    # Get the document
    try:
        document = open(f"input/{patient_name}/{document_name}", "r").read()
    except FileNotFoundError:
        print(f"File not found: {document_name}")
    # Construct the user prompt
    user_prompt = f"{question}\n{document}"
    return user_prompt


def collect_llm_responses(
    model_list: list[str],
    system_prompt: str,
    questions: dict[str, str],
    patient_to_document_names: list[tuple[str, str]],
) -> dict[str, dict[str, dict[str, str]]]:
    responses = {}
    # For each model, document, and question, get the response
    for model_name in model_list:
        responses[model_name] = {}
        for patient_name, document_name in patient_to_document_names:
            responses[model_name][document_name] = {}
            for question_type, question in questions.items():
                # Construct the user prompt
                user_prompt = make_user_prompt(question, patient_name, document_name)
                # Get the response
                response = get_llm_response(model_name, system_prompt, user_prompt)
                # Add the response to the dictionary
                responses[model_name][document_name][question_type] = response
    # Get the responses
    return responses


def main():
    # Load the questions
    questions = load_questions()
    # Load the answer keys
    answer_keys = load_answer_keys()
    # Get the patient to document names
    patient_to_document_names = get_patient_to_document_names()
    # Get the responses
    responses = collect_llm_responses(
        MODEL_LIST, SYSTEM_PROMPT, questions, patient_to_document_names
    )

    # Compare the responses with the answer keys
    results = {}
    for model_name, document_responses in responses.items():
        results[model_name] = {}
        for document_name, question_responses in document_responses.items():
            results[model_name][document_name] = {}
            for question_type, response in question_responses.items():
                print(
                    f"Model: {model_name}\nDocument: {document_name}\nQuestion type: {question_type}\nResponse: {response}\n"
                )
            # Save to results
            results[model_name][document_name] = compare_responses_with_keys(
                question_responses, answer_keys[document_name]
            )
    # Print the results
    print(json.dumps(results, indent=4))
    # Write the results to a file
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)


if __name__ == "__main__":
    # print(json.dumps(load_questions(), indent=4))
    # print(get_patient_to_document_names())
    # make_user_prompt("question1", "fake_patient1_doc1_RAD.txt")
    # assert len(get_patient_to_document_names()) == 59
    print(get_patient_to_document_names())
