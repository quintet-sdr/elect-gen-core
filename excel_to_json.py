import pandas as pd
import json


def excel_to_json(excel_file_path, json_file_path):
    df = pd.read_excel(excel_file_path)
    json_data = df.to_json(orient="records")
    with open(json_file_path, 'w') as json_file:
        json_file.write(json_data)
    return json_file_path


def format_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
