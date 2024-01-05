import os
from helper import load_json_file, save_json_file, translate_principal_date


def get_note(data, document_name):
    for n in data["patient"]["notes"]:
        if n["name"] == document_name:
            return n


# TODO: make the attributes extensible and configurable
def generate_answer_keys(data, note):
    # data: the whole JSON file, note: the note to generate the answer keys for
    # Generate the answer keys with the following format:
    answer_keys = {}
    answer_keys["name"] = " ".join(
        [part.capitalize() for part in data["patient"]["name"].split("_")]
    )
    answer_keys["type"] = note["type"]
    answer_keys["date"] = translate_principal_date(note["date"])
    answer_keys["episode"] = note["episode"]
    answer_keys["sections"] = ", ".join([s["type"] for s in note["sections"]])
    answer_keys["classUri-mentions"] = ", ".join(
        set([f"{m['classUri']}" for m in note["mentions"]])
    )
    answer_keys["attributes"] = ", ".join(
        [
            f"{m['classUri']}: " + ", ".join([a for a in m if m[a] is True])
            for m in note["mentions"]
        ]
    )
    return answer_keys


def get_answer_keys(patient_name, document_name):
    data = load_json_file(f"output/JSON/{patient_name}/{patient_name}.json")
    note = get_note(data, document_name)
    print(f"Generating answer keys for {document_name}")
    answer_keys = generate_answer_keys(data, note)
    save_json_file(f"answer_keys/{patient_name}/{document_name}.json", answer_keys)

    return answer_keys


# TODO: consider removing document_name from the function parameters
def load_answer_keys(
    patient_name: str = None, document_name: str = None
) -> dict[str, dict[str, dict]]:
    if patient_name is None:
        # Load the answer keys for all patients
        answer_keys = {}
        for d in os.listdir("input"):
            if not os.path.isdir(os.path.join("input", d)):
                continue
            patient = d
            answer_keys.update(load_answer_keys(patient_name=patient))
        return answer_keys
    if document_name is None:
        # Load the answer keys for a single patient (all documents)
        answer_keys = {}
        answer_keys[patient_name] = {}
        for file in os.listdir(f"input/{patient_name}"):
            document, extension = os.path.splitext(file)
            if extension != ".txt":
                continue
            answer_keys[patient_name][document] = get_answer_keys(
                patient_name, document
            )
        return answer_keys
    else:
        # Load the answer keys for a single document
        answer_keys = {}
        answer_keys[patient_name] = {}
        answer_keys[patient_name][document_name] = get_answer_keys(
            patient_name, document_name
        )
        return answer_keys


if __name__ == "__main__":
    import json

    # Test the get_answer_keys function
    answer_keys = load_answer_keys(
        patient_name="fake_patient1",
        document_name="fake_patient1_doc1_RAD",
    )
    print(json.dumps(answer_keys, indent=4))
