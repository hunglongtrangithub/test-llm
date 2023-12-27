import json
import os


def load_json_file(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def save_json_file(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def get_note(data, document_name):
    for n in data["patient"]["notes"]:
        if n["name"] == document_name:
            return n


def generate_answer_keys(data, note):
    print(f"Generating answer keys for {note}")
    # Generate the answer keys with the following format:
    answer_keys = {}
    answer_keys["name"] = data["patient"]["name"]
    answer_keys["type"] = note["type"]
    answer_keys["date"] = note["date"]
    answer_keys["episode"] = note["episode"]
    answer_keys["sections"] = ", ".join([s["type"] for s in note["sections"]])
    answer_keys["classUri-mentions"] = ", ".join(
        [m["classUri"] for m in note["mentions"]]
    )
    answer_keys["classUri-begins-ends"] = ", ".join(
        [f"{m['begin']}:{m['end']}" for m in note["mentions"]]
    )
    answer_keys["attributes"] = ", ".join(
        [f"{m['classUri']}: {a}" for m in note["mentions"] for a in m if m[a] is True]
    )
    return answer_keys


def get_answer_keys(patient_name, document_name):
    # Check if the answer keys have already been generated
    try:
        return load_json_file(f"answer_keys/{patient_name}/{document_name}.json")
    except FileNotFoundError:
        pass
    # Load the JSON file
    data = load_json_file(f"output/JSON/{patient_name}/{patient_name}.json")
    # Get the note according to the document name
    note = get_note(data, document_name)
    # Generate the answer keys
    answer_keys = generate_answer_keys(data, note)
    # Save the answer keys
    save_json_file(f"answer_keys/{patient_name}/{document_name}.json", answer_keys)

    return answer_keys


def load_answer_keys(patient_name, document_name=None):
    if document_name is None:
        answer_keys = {}
        for file in os.listdir(f"input/{patient_name}"):
            document, extension = os.path.splitext(file)
            # Skip non-text files
            if extension != ".txt":
                continue
            answer_keys[document] = get_answer_keys(patient_name, document)
        return answer_keys
    else:
        return get_answer_keys(patient_name, document_name)


if __name__ == "__main__":
    # Test the get_answer_keys function
    patient_name = "fake_patient2"
    document_name = "fake_patient1_doc1_RAD"
    answer_keys = load_answer_keys(patient_name)
