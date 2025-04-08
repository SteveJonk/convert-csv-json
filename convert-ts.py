import json
import os
import shutil
import re

new_folder = 'new'
locales_folder = 'locales'
output_folder = 'output'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def deep_merge(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1 and isinstance(value, dict) and isinstance(dict1[key], dict):
            dict1[key] = deep_merge(dict1[key], value)
        else:
            dict1[key] = value
    return dict1

# Helper to strip `export default` from TS file
def extract_json_from_ts(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Remove export default and trailing semicolon
        match = re.search(r'export\s+default\s+(.+);?$', content, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse TypeScript file: {file_path}")
        json_str = match.group(1).strip()
        return json.loads(json_str)

# Iterate through files in locales
for locales_file in os.listdir(locales_folder):
    if not locales_file.endswith('.ts'):
        continue

    name = os.path.splitext(locales_file)[0]
    new_file = os.path.join(new_folder, name + '.json')
    locale_ts_path = os.path.join(locales_folder, locales_file)

    if os.path.isfile(new_file):
        # Load TS locale data
        locales_data = extract_json_from_ts(locale_ts_path)

        # Load JSON new data
        with open(new_file, 'r', encoding='utf-8') as new_json:
            new_data = json.load(new_json)

        # Merge
        combined_data = deep_merge(locales_data, new_data)

        # Write TS output
        output_file = os.path.join(output_folder, locales_file)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('export default ')
            json.dump(combined_data, f, indent=2, ensure_ascii=False)
            f.write(';\n')
    else:
        # No new file, just copy the original TS file
        shutil.copyfile(locale_ts_path, os.path.join(output_folder, locales_file))

print('TS files combined and outputted to the "output" folder.')
