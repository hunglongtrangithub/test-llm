import requests
from datetime import datetime
import json
import os

CHIMERA_GPT_KEY = os.getenv("CHIMERA_GPT_KEY")


def fetch_chat_models():
    models = []
    headers = {
        "Authorization": f"Bearer {CHIMERA_GPT_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get("https://api.naga.ac/v1/models", headers=headers)
    if response.status_code == 200:
        ModelsData = response.json()
        models.extend(
            model["id"] for model in ModelsData.get("data") if "max_images" not in model
        )
    else:
        print(f"Failed to fetch chat models. Status code: {response.status_code}")

    return models


def list_paths(start_dir):
    for dirpath, dirnames, filenames in os.walk(start_dir):
        print(f"Found directory: {dirpath}")
        for dirname in dirnames:
            print(f"Subdirectory: {dirname}")
        for filename in filenames:
            print(f"File: {filename}")


def print_keys_recursively(d, indent=0):
    for key, value in d.items():
        print(" " * indent + str(key))
        if isinstance(value, dict):
            print_keys_recursively(
                value, indent + 2
            )  # Increase indentation for nested dictionaries


def load_json_file(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def save_json_file(file_path, data):
    dir_name = os.path.dirname(file_path)
    if dir_name:  # only create directories if dir_name is not empty
        os.makedirs(dir_name, exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def translate_principal_date(principal_date):
    dt = datetime.strptime(principal_date, "%Y%m%d%H%M")
    formatted_date = dt.strftime("%B %d, %Y at %I:%M %p")
    return formatted_date


def merge_two_evluation_dicts(dict1, dict2):
    for key in dict2:
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                merge_two_evluation_dicts(dict1[key], dict2[key])
            else:
                dict1[key] = dict2[key]
        else:
            dict1[key] = dict2[key]
    return dict1


if __name__ == "__main__":
    # print("Available models:")
    # print("\n".join(fetch_chat_models()))
    # list_paths("input")
    # print(list(os.walk("input")))
    pass
