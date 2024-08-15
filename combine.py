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

# Get the list of JSON files in the 'new' folder
new_files = os.listdir(new_folder)

# Iterate over the files in the 'new' folder
for new_file in new_files:
    # Get the corresponding file path in the 'locales' folder
    locales_file = os.path.join(locales_folder, new_file)
    
    # Check if the file exists in the 'locales' folder
    if os.path.isfile(locales_file):
        # Open the JSON files
        with open(os.path.join(new_folder, new_file)) as new_json, open(locales_file) as locales_json:
            # Load the JSON data
            new_data = json.load(new_json)
            locales_data = json.load(locales_json)
        
        # Combine the JSON data
        combined_data = {**new_data, **locales_data}
        
        # Save the combined data to the 'output' folder
        output_file = os.path.join(output_folder, new_file)
        with open(output_file, 'w') as output_json:
            json.dump(combined_data, output_json, indent=4)
    
    # If the file doesn't exist in the 'locales' folder, copy it from the 'new' folder to the 'output' folder
    else:
        shutil.copyfile(os.path.join(new_folder, new_file), os.path.join(output_folder, new_file))

print('JSON files combined and outputted to the "output" folder.')