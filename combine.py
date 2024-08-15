import json
import os
import shutil

# Specify the paths of the 'new' and 'locales' folders
new_folder = 'new'
locales_folder = 'locales'
output_folder = 'output'

# Create the 'output' folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to deeply merge two dictionaries
def deep_merge(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1:
            if isinstance(value, dict) and isinstance(dict1[key], dict):
                # If both values are dictionaries, merge them recursively
                dict1[key] = deep_merge(dict1[key], value)
            else:
                # Otherwise, overwrite with the value from dict2
                dict1[key] = value
        else:
            dict1[key] = value
    return dict1

# Get the list of JSON files in the 'locales' folder
locales_files = os.listdir(locales_folder)

# Iterate over the files in the 'locales' folder
for locales_file in locales_files:
    # Get the corresponding file path in the 'new' folder
    new_file = os.path.join(new_folder, locales_file)
    
    # Check if the file exists in the 'new' folder
    if os.path.isfile(new_file):
        # Open the JSON files
        with open(os.path.join(locales_folder, locales_file), 'r', encoding='utf-8') as locales_json, open(new_file, 'r', encoding='utf-8') as new_json:
            # Load the JSON data
            locales_data = json.load(locales_json)
            new_data = json.load(new_json)
        
        # Deeply merge the JSON data
        combined_data = deep_merge(locales_data, new_data)
        
        # Save the combined data to the 'output' folder
        output_file = os.path.join(output_folder, locales_file)
        with open(output_file, 'w', encoding='utf-8') as output_json:
            # Set indent to 2 spaces and add a newline after the JSON data
            json.dump(combined_data, output_json, indent=2, ensure_ascii=False)
            output_json.write('\n')  # Add a newline at the end
    
    # If the file doesn't exist in the 'new' folder, copy it from the 'locales' folder to the 'output' folder
    else:
        shutil.copyfile(os.path.join(locales_folder, locales_file), os.path.join(output_folder, locales_file))

print('JSON files combined and outputted to the "output" folder.')
