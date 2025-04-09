import json5  # Using json5 instead of demjson
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

def clean_ts_to_json_str(ts_content):
    # Remove 'export default ' at the beginning if it's present
    ts_content = re.sub(r'^export\s+default\s+', '', ts_content.strip())

    # Debug output to file (full content, no truncation)
    debug_file = "debug_cleaned_output.txt"
    with open(debug_file, 'w', encoding='utf-8') as debug_f:
        debug_f.write(f"🔍 Cleaned content preview (before parsing):\n{ts_content}\n")

    return ts_content

def extract_json_from_ts(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_ts = f.read()

    cleaned = clean_ts_to_json_str(raw_ts)

    try:
        return json5.loads(cleaned)  # Use json5 to decode
    except ValueError as e:  # Catch the generic ValueError
        print(f"\n❌ Failed to parse {file_path}")
        print(f"🔍 Cleaned content preview (before parsing):\n{cleaned}\n")
        raise e

# Process each TS file
for locales_file in os.listdir(locales_folder):
    if not locales_file.endswith('.ts'):
        continue

    base_name = os.path.splitext(locales_file)[0]
    new_json_path = os.path.join(new_folder, base_name + '.json')
    locale_ts_path = os.path.join(locales_folder, locales_file)
    output_ts_path = os.path.join(output_folder, locales_file)

    if os.path.isfile(new_json_path):
        locales_data = extract_json_from_ts(locale_ts_path)

        with open(new_json_path, 'r', encoding='utf-8') as f:
            new_data = json5.load(f)  # Use json5 to load the new data

        combined = deep_merge(locales_data, new_data)

        with open(output_ts_path, 'w', encoding='utf-8') as f:
            f.write('export default ')
            json5.dump(combined, f, indent=2, ensure_ascii=False)  # Use json5 to dump the data
            f.write(';\n')
    else:
        shutil.copyfile(locale_ts_path, output_ts_path)

print('✅ Done. Merged TS files are in "output".')
