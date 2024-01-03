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
    # answer_keys["classUri-begins-ends"] = ", ".join(
    #     [f"{m['begin']}:{m['end']}" for m in note["mentions"]]
    # )
    answer_keys["attributes"] = ", ".join(
        [
            f"{m['classUri']}: " + ", ".join([a for a in m if m[a] is True])
            for m in note["mentions"]
        ]
    )
    return answer_keys


def get_answer_keys(patient_name, document_name):
    # Load the JSON file
    data = load_json_file(f"output/JSON/{patient_name}/{patient_name}.json")
    # Get the note according to the document name
    note = get_note(data, document_name)
    # Generate the answer keys
    print(f"Generating answer keys for {document_name}")
    answer_keys = generate_answer_keys(data, note)
    # Save the answer keys
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
            # Skip non-directories
            if not os.path.isdir(os.path.join("input", d)):
                continue
            patient = d
            # print(f"Loading answer keys for {patient}")
            answer_keys.update(load_answer_keys(patient_name=patient))
        return answer_keys
    if document_name is None:
        # Load the answer keys for a single patient (all documents)
        answer_keys = {}
        answer_keys[patient_name] = {}
        for file in os.listdir(f"input/{patient_name}"):
            document, extension = os.path.splitext(file)
            # Skip non-text files
            if extension != ".txt":
                continue
            # print(f"Loading answer keys for {document}")
            answer_keys[patient_name][document] = get_answer_keys(
                patient_name, document
            )
        return answer_keys
    else:
        # Load the answer keys for a single document
        # print(f"Loading answer keys for {document_name}")
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
    # # print all the keys of the dictionary for all levels
    # from helper import print_keys_recursively

    # print("Answer keys:")
    # print_keys_recursively(answer_keys)
