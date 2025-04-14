import fs from 'fs';
import path from 'path';
import { Project } from 'ts-morph';
import merge from 'lodash.merge';

// Helper to evaluate exported default object from TS file
function getDefaultExportObject(tsFilePath: string): any {
    const project = new Project();
    const sourceFile = project.addSourceFileAtPath(tsFilePath);

    const exportAssignment = sourceFile.getExportAssignmentOrThrow(expr => expr.isExportEquals() === false);
    const exportExpr = exportAssignment.getExpression();

    if (!exportExpr) {
        throw new Error(`No default export expression in ${tsFilePath}`);
    }

    const text = exportExpr.getText();

    // Make sure it's a plain object (starts with `{`)
    if (!text.trim().startsWith('{')) {
        throw new Error(`Default export in ${tsFilePath} is not a plain object literal`);
    }

    try {
        return eval(`(${text})`);
    } catch (e) {
        throw new Error(`Failed to evaluate object from ${tsFilePath}: ${e}`);
    }
}

// Merge and write one file
function mergeAndWrite(jsonPath: string, tsPath: string, outputPath: string) {
    console.log(`Merging ${path.basename(tsPath)}...`);

    const jsonObject = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
    const tsObject = getDefaultExportObject(tsPath);

    const merged = merge({}, tsObject, jsonObject);
    const output = `export default ${JSON.stringify(merged, null, 2)};\n`;
    fs.writeFileSync(outputPath, output, 'utf8');
    console.log(`✓ Written to ${outputPath}`);
}

// Process all matching files
function mergeAllLocales(jsonDir: string, tsDir: string, outputDir: string) {
    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

    const jsonFiles = fs.readdirSync(jsonDir).filter(f => f.endsWith('.json'));

    for (const jsonFile of jsonFiles) {
        const baseName = path.parse(jsonFile).name;
        const tsFile = `${baseName}.ts`;

        const jsonPath = path.join(jsonDir, jsonFile);
        const tsPath = path.join(tsDir, tsFile);
        const outputPath = path.join(outputDir, tsFile);

        if (!fs.existsSync(tsPath)) {
            console.warn(`! Skipped: ${tsFile} not found in ${tsDir}`);
            continue;
        }

        try {
            mergeAndWrite(jsonPath, tsPath, outputPath);
        } catch (err) {
            console.error(`Error processing ${tsFile}:`, err);
        }
    }
}

// Run with hardcoded folders
mergeAllLocales('new', 'locales', 'output');
