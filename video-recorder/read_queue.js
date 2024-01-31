const fs = require('fs');
const path = require('path');

const queue_data = JSON.parse(fs.readFileSync(path.join('.', 'queue0.json'), 'utf8'));

console.log(queue_data.length)