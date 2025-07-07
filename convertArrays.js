const fs = require('fs');
const path = require('path');

/**
 * Checks if an object has consecutive numeric keys starting from 0
 * @param {Object} obj - The object to check
 * @returns {boolean} - True if the object should be converted to an array
 */
function shouldConvertToArray(obj) {
    if (typeof obj !== 'object' || obj === null || Array.isArray(obj)) {
        return false;
    }

    const keys = Object.keys(obj);
    if (keys.length === 0) {
        return false;
    }

    // Check if all keys are numeric strings
    const numericKeys = keys.filter(key => /^\d+$/.test(key));
    if (numericKeys.length !== keys.length) {
        return false;
    }

    // Convert to numbers and sort
    const sortedNumbers = numericKeys.map(Number).sort((a, b) => a - b);

    // Check if they start from 0 and are consecutive
    for (let i = 0; i < sortedNumbers.length; i++) {
        if (sortedNumbers[i] !== i) {
            return false;
        }
    }

    return true;
}

/**
 * Recursively converts numeric keys to arrays
 * @param {any} obj - The object to process
 * @returns {any} - The processed object/array
 */
function convertNumericKeysToArrays(obj) {
    if (typeof obj !== 'object' || obj === null) {
        return obj;
    }

    if (Array.isArray(obj)) {
        return obj.map(item => convertNumericKeysToArrays(item));
    }

    // Check if this object should be converted to an array
    if (shouldConvertToArray(obj)) {
        const keys = Object.keys(obj).map(Number).sort((a, b) => a - b);
        const array = keys.map(key => convertNumericKeysToArrays(obj[key.toString()]));
        return array;
    }

    // Otherwise, recursively process object properties
    const result = {};
    for (const [key, value] of Object.entries(obj)) {
        result[key] = convertNumericKeysToArrays(value);
    }

    return result;
}

/**
 * Processes a single JSON file
 * @param {string} filePath - Path to the JSON file
 */
function processJsonFile(filePath) {
    try {
        console.log(`Processing: ${filePath}`);

        // Read the file
        const fileContent = fs.readFileSync(filePath, 'utf8');
        const jsonData = JSON.parse(fileContent);

        // Convert numeric keys to arrays
        const convertedData = convertNumericKeysToArrays(jsonData);

        // Write back to file with proper formatting
        fs.writeFileSync(filePath, JSON.stringify(convertedData, null, 2), 'utf8');

        console.log(`✅ Successfully processed: ${filePath}`);
    } catch (error) {
        console.error(`❌ Error processing ${filePath}:`, error.message);
    }
}

/**
 * Recursively finds all JSON files in a directory
 * @param {string} dir - Directory path
 * @returns {string[]} - Array of JSON file paths
 */
function findJsonFiles(dir) {
    let jsonFiles = [];

    try {
        const files = fs.readdirSync(dir);

        for (const file of files) {
            const fullPath = path.join(dir, file);
            const stat = fs.statSync(fullPath);

            if (stat.isDirectory()) {
                jsonFiles = jsonFiles.concat(findJsonFiles(fullPath));
            } else if (path.extname(file).toLowerCase() === '.json') {
                jsonFiles.push(fullPath);
            }
        }
    } catch (error) {
        console.error(`Error reading directory ${dir}:`, error.message);
    }

    return jsonFiles;
}

/**
 * Main function
 */
function main() {
    const newFolderPath = path.join(__dirname, 'new');

    // Check if the 'new' folder exists
    if (!fs.existsSync(newFolderPath)) {
        console.error(`❌ The 'new' folder does not exist at: ${newFolderPath}`);
        process.exit(1);
    }

    // Find all JSON files
    const jsonFiles = findJsonFiles(newFolderPath);

    if (jsonFiles.length === 0) {
        console.log('No JSON files found in the new folder.');
        return;
    }

    console.log(`Found ${jsonFiles.length} JSON file(s) to process:`);
    jsonFiles.forEach(file => console.log(`  - ${file}`));
    console.log('');

    // Process each JSON file
    jsonFiles.forEach(processJsonFile);

    console.log(`\n🎉 Conversion complete! Processed ${jsonFiles.length} file(s).`);
}

// Run the script
if (require.main === module) {
    main();
}
