const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');


// Example with specific allowed origins:
const allowedOrigins = ['http://localhost:5173'];
// const corsOptions = {
//     origin: (origin, callback) => {
//         if (allowedOrigins.indexOf(origin) !== -1) {
//             callback(null, true);
//         } else {
//             callback(new Error('Not allowed by CORS'));
//         }
//     }
// };

const app = express();

app.use(cors())
app.use(bodyParser.json({ limit: '500mb' })); // Parse JSON request bodies


app.post('/', (req, res) => {

    const animData = req.body.data; // Access the parsed JSON data
    const animName = req.body.name;

    // console.log('Received animation data:', animData);
    // save animData to a local file

    fs.writeFileSync(path.join('data', animName + '.json'), JSON.stringify(animData, null, 2));

    res.json({
        message: `Saved animation data to ${animName}.json`
    });
});



app.listen(2020, () => {
    console.log('server is listening on port 2020');
});