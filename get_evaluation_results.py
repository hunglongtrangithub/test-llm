from transformers import pipeline
from pylcs import lcs
import unicodedata


def normalize_string(s: str) -> str:
    # Convert to lowercase
    s = s.lower()

    # Normalize whitespace
    s = " ".join(s.split())

    # Normalize Unicode characters
    s = unicodedata.normalize("NFKC", s)
    return s


# Load the NLI model
nli_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


def evaluate_by_nli(response: str, answer: str) -> tuple[str, float]:
    if not response:
        return "empty", 0.0
    candidate_labels = ["entailment", "contradiction", "neutral"]
    hypothesis_template = f'This text is {{}} to "{answer}".'
    result = nli_model(
        response,
        candidate_labels=candidate_labels,
        hypothesis_template=hypothesis_template,
    )
    label, score = max(zip(result["labels"], result["scores"]), key=lambda x: x[1])
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
