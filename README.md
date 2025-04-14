# CSV to TS/JSON file for i18n
This is a script to convert a CSV file with translations into a TypeScript or JSON file for i18n. It uses Python and Node.js to do the conversion.

## Some requirements:
- Install python3
- Make sure to save your csv as utf-8 encoded (or you'll get errors)
- Run `pnpm install`
- Make sure you have these three folders in the root of the repo:
   - `locales`
   - `output`
   - `translations`

## Notes:
- The node `convert` script doesn't work yet. Python does.
- Sorry that this is a combination of python and node, I didn't have time to convert everything to node.

## To run this, simply do the following:
1. There are two options:
   1. Replace the contents of translations.csv with your own translations (make sure it's utf-8 encoded and that the first row is the keys)
   2. change the filename const in the `convert.py` file to your own csv file
2. Run the following command: `python3 convert.py`
3. Copy all current locales from the repo to the `locales` folder
4. Here too, two options:
   1. When merging to a TS file, Run the following command: `npm run combine`
   2. When merging to a new json file, run the following command: `python3 combine.py`
5. The new locales will be in the `output` folder
6. Copy the contents of the `output` folder to the `locales` folder in the repo
