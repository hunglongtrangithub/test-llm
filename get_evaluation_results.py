from transformers import pipeline


def evaluate(response, answer, model_name="roberta-large-mnli"):
    # Load a pre-trained NLI model from Hugging Face
    nli_model = pipeline("text-classification", model=model_name)
    # Use the NLI model to predict the relationship
    result = nli_model(f"{answer} {response}")
    label, score = result[0]["label"], result[0]["score"]
    return label, score


def compare_responses_with_keys(responses, answer_keys):
    # This function is for comparing the responses with the answer keys for a single document
    if len(responses) != len(answer_keys):
        raise ValueError("The length of responses and answer keys must be the same")

    results = []
    for response, key in zip(responses, answer_keys):
        label, score = evaluate(response, key)
        results.append(
            {"response": response, "key": key, "label": label, "score": score}
        )

    return results
