import csv
import json

filename = 'translations.csv'  # replace with your filename

# Open the CSV
with open(filename, 'r', encoding='ISO-8859-1') as f:
    reader = csv.reader(f)
    
    # Get the entire data of the file
    rows = list(reader)
    
    # For each column after the first
    for j in range(1, len(rows[0])):
        # Create a new JSON file for this column
        with open(f'output{j}.json', 'w') as jsonf:
            # Write data to this JSON file
            jsonf.write(json.dumps({rows[i][0]: rows[i][j] for i in range(len(rows))}, indent=4))