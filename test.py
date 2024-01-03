from datetime import datetime
from get_llm_responses import collect_llm_responses
from get_evaluation_results import get_evaluation_results, normalize_string
from get_answer_keys import get_answer_keys
from main import load_questions, SYSTEM_PROMPT, make_user_prompt
from helper import translate_principal_date
import json


# Test the collect_llm_responses function
def test_collect_llm_responses():
    model_name = "gpt-4"
    patient_name = "fake_patient1"
    document_name = "fake_patient1_doc1_RAD"
    questions = load_questions()

    responses = collect_llm_responses(
        model_name,
        SYSTEM_PROMPT,
        make_user_prompt,
        patient_name,
        document_name,
        questions,
    )
    print(json.dumps(responses, indent=4))


def test_get_evaluation_results():
    answer_keys = {
        "question1": "The capital of France is Paris.",
        "question2": "Python is an interpreted, high-level, general-purpose programming language.",
        "question3": "medical document's principal date: January 23, 2010 at 10:45 AM",
    }
    responses = {
        "question1": "Paris is the capital of France.",
        "question2": "Python is a high-level, interpreted, general-purpose programming language.",
        "question3": "The principal date of the medical document is January 23, 2010 at 10:45.",
    }
    # Evaluate the responses
    evaluations = get_evaluation_results(responses, answer_keys)
    print(json.dumps(evaluations, indent=4))


def test_make_user_prompt():
    question = "What is the capital of France?"
    document = "The capital of France is Paris."
    print(make_user_prompt(question, document))


def test_get_answer_keys():
    patient_name = "fake_patient1"
    document_name = "fake_patient1_doc1_RAD"
    answer_keys = get_answer_keys(patient_name, document_name)
    print(json.dumps(answer_keys, indent=4))


def test_translate_principal_date():
    # Example usage
    principal_date = "201001231045"
    print(translate_principal_date(principal_date))


def test_normalize_string():
    # Example usage
    s = "The principal date of the medical document is January 23, 2010 at 10:45 AM."
    print(normalize_string(s))


if __name__ == "__main__":
    # test_collect_llm_responses()
    # test_get_evaluation_results()
    # test_make_user_prompt()
    # test_get_answer_keys()
    # test_translate_principal_date()
    test_normalize_string()
    pass
