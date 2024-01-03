from transformers import pipeline
from pylcs import lcs
import re
import unicodedata


def normalize_string(s: str) -> str:
    # Convert to lowercase
    s = s.lower()

    # Normalize whitespace
    s = " ".join(s.split())

    # Normalize Unicode characters
    s = unicodedata.normalize("NFKC", s)
    return s


MODEL_NAME = "roberta-large-mnli"
# Load a pre-trained NLI model from Hugging Face
NLI_MODEL = pipeline("text-classification", model=MODEL_NAME)


def evaluate_by_nli(response: str, answer: str) -> tuple[str, float]:
    # Use the NLI model to predict the relationship
    result = NLI_MODEL(f"{answer} {response}")
    label, score = result[0]["label"], result[0]["score"]
    return label, score


def evaluate_by_lcs(response: str, answer: str) -> tuple[str, float]:
    # Use the LCS algorithm to predict the relationship
    score = lcs(response, answer) / len(answer)
    return score


def get_evaluation_results(
    responses: dict[str, str], answer_keys: dict[str, str]
) -> dict[str, dict[str, str]]:
    # This function is for comparing the responses with the answer keys for a single document
    if responses.keys() != answer_keys.keys():
        raise ValueError("The keys of the responses and answer keys must match.")
    evaluation_results = {}
    for question_type in responses.keys():
        # normalized_responses = normalize_string(responses[question_type])
        # normalized_answer_keys = normalize_string(answer_keys[question_type])
        label, nli_score = evaluate_by_nli(
            responses[question_type], answer_keys[question_type]
        )
        lcs_score = evaluate_by_lcs(
            responses[question_type], answer_keys[question_type]
        )
        evaluation_results[question_type] = {
            "nli_label": label,
            "nli_score": nli_score,
            "lcs_score": lcs_score,
        }
    return evaluation_results
