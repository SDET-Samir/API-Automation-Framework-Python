import json
import os


def load_test_data(key):
    file_path = os.path.join(os.path.dirname(
        __file__), '..', 'data', 'employees.json')

    file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f" Master Samir, the file was not found here: {file_path}")

    with open(file_path, 'r', encoding="utf8") as file:
        data = json.load(file)

    return data.get(key)
