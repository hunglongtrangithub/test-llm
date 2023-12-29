import requests
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
    import os

    for dirpath, dirnames, filenames in os.walk(start_dir):
        # print(f"Found directory: {dirpath}")
        # for dirname in dirnames:
        # print(f"Subdirectory: {dirname}")
        for filename in filenames:
            print(f"File: {filename}")


def print_keys_recursively(d, indent=0):
    for key, value in d.items():
        print(" " * indent + str(key))
        if isinstance(value, dict):
            print_keys_recursively(
                value, indent + 2
            )  # Increase indentation for nested dictionaries


if __name__ == "__main__":
    # print("Available models:")
    # print("\n".join(fetch_chat_models()))
    list_paths("input")
    # print(list(os.walk("input")))
