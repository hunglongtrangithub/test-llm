from get_answer_keys import load_answer_keys
from get_llm_responses import collect_llm_responses
from get_evaluation_results import get_evaluation_results
import json
import os

# SYSTEM_PROMPT = "Your task is to analyze the provided medical document and answer the following questions accurately. For each question, only answer with relevant information from the document and present your answers in the specified format. Pay close attention to the format requirements for each question to ensure your responses align with the expected structure. Your goal is to provide clear, concise, and correctly formatted answers based on the content of the document."
SYSTEM_PROMPT = "Your task is to analyze the provided medical document and answer the following question accurately. Only answer with relevant information from the document and present your answer in the specified format. Pay close attention to the format requirements for the question to ensure your response align with the expected structure. Your goal is to provide a clear, concise, and correctly formatted answer based on the content of the document."
USER_PROMPT_TEMPLATE = "{question}\n{document}"
MODEL_LIST = [
    "gpt-4",
    "gemini-pro",
    # "gpt-3.5-turbo-0613",
    # "llama-2-70b-chat",
    # "llama-2-7b-chat",
    # "code-llama-34b",
]


def get_patient_to_document_names(
    path: str = "input", patient_name: str = None
) -> dict[str, list[str]]:
    # The path must contain only subdirectories as patients and only .txt files in each subdirectory as documents
    patient_document_names = {}
    if patient_name is not None:
        # Get the document names for the patient
        patient_document_names[patient_name] = []
        for filename in os.listdir(f"{path}/{patient_name}"):
            if filename.endswith(".txt"):
                document_name = os.path.splitext(filename)[0]
                patient_document_names[patient_name].append(document_name)
        return patient_document_names
    for dirpath, _, filenames in os.walk(path):
        if dirpath == path:
            continue
        patient_name = os.path.basename(dirpath)
        txt_files = [filename for filename in filenames if filename.endswith(".txt")]
        patient_document_names[patient_name] = txt_files
    return patient_document_names


def load_questions():
    return json.load(open("questions.json", "r"))


def make_user_prompt(question, document):
    # Construct the user prompt
    user_prompt = USER_PROMPT_TEMPLATE.format(question=question, document=document)
    return user_prompt


def main():
    # This functions loads the questions, answer keys, and collect LLM responses, and then evaluates the responses
    # Load the questions
    questions = load_questions()
    print("Loaded questions from questions.json")
    # Load the answer keys
    answer_keys = load_answer_keys(patient_name="fake_patient1")
    print("Loaded answer keys from answer_keys.json")
    # Get patient to document names
    patient_to_document_names = get_patient_to_document_names(
        patient_name="fake_patient1"
    )
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
                    make_user_prompt,
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
