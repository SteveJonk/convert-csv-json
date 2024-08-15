import csv
import json
import os


def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value

filename = 'translations.csv'  # replace with your filename
output_directory = 'new'

# Open the CSV
with open(filename, 'r', encoding='ISO-8859-1') as f:
    reader = csv.reader(f)

    # Get the entire data of the file
    rows = list(reader)

    # For each column after the first
    for j in range(1, len(rows[0])):
        # Use the first row of the column as the filename
        output_filename = f'{rows[0][j]}.json'
        
        data = {}
        
        # Create a new JSON file for this column
        with open(os.path.join(output_directory, output_filename), 'w') as jsonf:
            for i in range(1, len(rows)):
                key_parts = rows[i][0].split('.')
                nested_set(data, key_parts, rows[i][j])

            # Write data to this JSON file
            jsonf.write(json.dumps(data, indent=4))