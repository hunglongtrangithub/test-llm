from get_answer_keys import load_answer_keys
from get_llm_responses import collect_llm_responses
from get_evaluation_results import get_evaluation_results
from natsort import os_sorted
import json
import os

# SYSTEM_PROMPT = "Your task is to analyze the provided medical document and answer the following questions accurately. For each question, only answer with relevant information from the document and present your answers in the specified format. Pay close attention to the format requirements for each question to ensure your responses align with the expected structure. Your goal is to provide clear, concise, and correctly formatted answers based on the content of the document."
# SYSTEM_PROMPT = "Your task is to analyze the provided medical document and answer the following question accurately. Only answer with relevant information from the document and present your answer in the specified format. Pay close attention to the format requirements for the question to ensure your response align with the expected structure. Your goal is to provide a clear, concise, and correctly formatted answer based on the content of the document."
# SYSTEM_PROMPT = "Analyze the medical document and succinctly answer the question provided. Your response must directly use information from the document and adhere strictly to the specified answer format. Focus on brevity and precision. Avoid extraneous details to ensure your answer is clear, concise, and correctly formatted, directly reflecting the document's content."
SYSTEM_PROMPT = "Your task is to analyze the provided medical document and answer the following question accurately. Only answer with relevant information from the document and present your answer in the specified format. Pay close attention to the format requirements for the question to ensure your response align with the expected structure. Your goal is to provide a clear, concise, and correctly formatted answer based on the content of the document. Avoid extraneous details to ensure your answer is clear, concise, and correctly formatted, directly reflecting the document's content."
USER_PROMPT_TEMPLATE = "{question}\n{document}"
MODEL_LIST = [
    "gpt-4",
    "gemini-pro",
    "gpt-3.5-turbo-0613",
    "llama-2-70b-chat",
    "llama-2-13b-chat",
    "llama-2-7b-chat",
]


def get_patient_to_document_names(
    path: str = "input", patient_name: str = None, document_name: str = None
) -> dict[str, list[str]]:
    # The path must contain only subdirectories as patients and only .txt files in each subdirectory as documents
    patient_document_names = {}
    if patient_name is not None:
        # Get the document names for the patient
        patient_document_names[patient_name] = []
        txt_files = os_sorted(
            [
                filename
                for filename in os.listdir(f"{path}/{patient_name}")
                if filename.endswith(".txt")
            ]
        )
        for filename in txt_files:
            doc_name = os.path.splitext(filename)[0]
            if document_name is not None:
                if doc_name == document_name:
                    patient_document_names[patient_name].append(doc_name)
                    return patient_document_names
            else:
                patient_document_names[patient_name].append(doc_name)
        return patient_document_names
    else:
        patient_names = os_sorted(
            [
                dir_name
                for dir_name in os.listdir(path)
                if os.path.isdir(os.path.join(path, dir_name))
            ]
        )
        for patient_name in patient_names:
            patient_document_names[patient_name] = []
            txt_files = os_sorted(
                [
                    filename
                    for filename in os.listdir(f"{path}/{patient_name}")
                    if filename.endswith(".txt")
                ]
            )
            for filename in txt_files:
                doc_name = os.path.splitext(filename)[0]
                patient_document_names[patient_name].append(doc_name)
    return patient_document_names


def load_questions():
    return json.load(open("questions.json", "r"))


def main():
    # This functions loads the questions, answer keys, and collect LLM responses, and then evaluates the responses
    # Load the questions
    questions = load_questions()
    print("Loaded questions from questions.json")
    # Load the answer keys
    answer_keys = load_answer_keys(patient_name="fake_patient1", document_name=None)
    print("Loaded answer keys from answer_keys")
    # Get patient to document names
    patient_to_document_names = get_patient_to_document_names(
        patient_name="fake_patient1", document_name=None
    )
    print("Loaded patient to document names")
    # Collect LLM responses and evaluation
    evaluations = {}
    for patient_name, document_names in patient_to_document_names.items():
        evaluations[patient_name] = {}
        for document_name in document_names:
            evaluations[patient_name][document_name] = {}
            for model_name in MODEL_LIST:
                llm_respones = collect_llm_responses(
                    model_name,
                    SYSTEM_PROMPT,
                    USER_PROMPT_TEMPLATE,
                    patient_name,
                    document_name,
                    questions,
                )
                evals = get_evaluation_results(
                    llm_respones, answer_keys[patient_name][document_name]
                )
                evaluations[patient_name][document_name][model_name] = evals
    # Save the evaluations
    json.dump(evaluations, open("evaluation_results.json", "w"), indent=4)
    print("Evaluation results saved to evaluation_results.json")


if __name__ == "__main__":
    main()
