from transformers import pipeline
import json
import pylcs

SYSTEM_PROMPT = "Your task is to analyze the provided medical document and answer the following questions accurately. For each question, extract only the relevant information from the document and present your answers in the specified format. Pay close attention to the format requirements for each question to ensure your responses align with the expected structure. Your goal is to provide clear, concise, and correctly formatted answers based on the content of the document."


def evaluate(response, answer, model_name="roberta-large-mnli"):
    # Load a pre-trained NLI model from Hugging Face
    nli_model = pipeline("text-classification", model=model_name)
    # Use the NLI model to predict the relationship
    result = nli_model(f"{answer} [SEP] {response}")
    label, score = result[0]["label"], result[0]["score"]
    return label, score


def compare_responses_with_keys(responses, answer_keys):
    if len(responses) != len(answer_keys):
        raise ValueError("The length of responses and answer keys must be the same")

    results = []
    for response, key in zip(responses, answer_keys):
        # Calculate the length of the longest common substring
        lcs_length = pylcs.lcs(response, key)
        results.append({"response": response, "key": key, "lcs_length": lcs_length})

    return results


def main():
    # Get the questions and answer keys from the JSON file
    pass
