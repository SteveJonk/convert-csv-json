const fs = require('fs');
const csv = require('csv-parser');

const FILE_NAME = 'translations.csv';

function setNestedKey(obj, path, value) {
  const keys = path?.split('.');
  const lastKey = keys?.pop();
  const lastObj = keys?.reduce((obj, key) => (obj[key] = obj[key] || {}), obj);
  lastObj[lastKey] = value;
}

fs.createReadStream(FILE_NAME)
  .pipe(csv())
  .on('headers', (headers) => {
    headers.slice(1).forEach((header) => {
      fs.writeFileSync(`${header}.json`, '{}');
    });
  })
  .on('data', (row) => {
    Object.keys(row)
      .slice(1)
      .forEach((column) => {
        const data = JSON.parse(fs.readFileSync(`${column}.json`));
        setNestedKey(data, row['key'], row[column]);
        fs.writeFileSync(`${column}.json`, JSON.stringify(data, null, 4));
      });
  });
