from get_llm_responses import collect_llm_responses
from get_evaluation_results import get_evaluation_results
from main import load_questions, SYSTEM_PROMPT, make_user_prompt
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
        "question3": "The square root of 9 is 3.",
    }
    responses = {
        "question1": "Paris is the capital of France.",
        "question2": "Python is a high-level, interpreted, general-purpose programming language.",
        "question3": "3 is the square root of 9.",
    }
    # Evaluate the responses
    evaluations = get_evaluation_results(responses, answer_keys)
    print(json.dumps(evaluations, indent=4))


if __name__ == "__main__":
    test_collect_llm_responses()
    # test_get_evaluation_results()
