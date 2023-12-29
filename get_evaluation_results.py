from transformers import pipeline


def evaluate(response: str, answer: str, model_name: str = "roberta-large-mnli"):
    # Load a pre-trained NLI model from Hugging Face
    nli_model = pipeline("text-classification", model=model_name)
    # Use the NLI model to predict the relationship
    result = nli_model(f"{answer} {response}")
    label, score = result[0]["label"], result[0]["score"]
    return label, score


def get_evaluation_results(
    responses: dict[str, str], answer_keys: dict[str, str]
) -> dict[str, dict[str, str]]:
    # This function is for comparing the responses with the answer keys for a single document
    if responses.keys() != answer_keys.keys():
        raise ValueError("The keys of the responses and answer keys must match.")
    evaluation_results = {}
    for question_type in responses.keys():
        label, score = evaluate(responses[question_type], answer_keys[question_type])
        evaluation_results[question_type] = {"label": label, "score": score}
    return evaluation_results
