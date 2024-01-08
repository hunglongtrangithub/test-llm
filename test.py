from datetime import datetime
from get_llm_responses import collect_llm_responses, get_llm_response
from get_evaluation_results import get_evaluation_results, normalize_string
from get_answer_keys import get_answer_keys
from main import (
    load_questions,
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    get_patient_to_document_names,
)
from helper import translate_principal_date, merge_two_evluation_dicts
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
        USER_PROMPT_TEMPLATE,
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
        "question4": "The capital of France is Paris.",
    }
    responses = {
        "question1": "Paris is the capital of France.",
        "question2": "Python is a high-level, interpreted, general-purpose programming language.",
        "question3": "The principal date of the medical document is January 23, 2010 at 10:45.",
        "question4": "The capital of France is Paris." * 1000,
    }
    # Evaluate the responses
    evaluations = get_evaluation_results(responses, answer_keys)
    print(json.dumps(evaluations, indent=4))


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


def test_get_patient_to_document_names():
    patient_to_document_names = get_patient_to_document_names()
    print(json.dumps(patient_to_document_names, indent=4))


def test_get_llm_response():
    system_prompt = "You are an alien from outer space. You have come to Earth to learn about humans."
    user_prompt = "What is your name? What planet do you come from?"
    model_name = "vicuna-7b-v1.5-16k"
    response = get_llm_response(model_name, system_prompt, user_prompt)
    print(response)


def test_merge_two_evaluation_dicts():
    dict1 = {"level1": {"level2": {"key1": "value1", "key2": "value2"}}}
    dict2 = {"level1": {"level2": {"key3": "value3", "key2": "new_value2"}}}
    expected_result = {
        "level1": {"level2": {"key1": "value1", "key2": "new_value2", "key3": "value3"}}
    }
    result = merge_two_evluation_dicts(dict1, dict2)
    print(result)
    assert result == expected_result


if __name__ == "__main__":
    # test_collect_llm_responses()
    # test_get_evaluation_results()
    # test_get_answer_keys()
    # test_translate_principal_date()
    # test_normalize_string()
    # test_get_patient_to_document_names()
    # test_get_llm_response()
    test_merge_two_evaluation_dicts()
    pass
