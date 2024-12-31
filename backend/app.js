require('dotenv').config();
const express = require('express');
const { spawn } = require('child_process');
const app = express();

const port = process.env.PORT || 3000;

app.use(express.json());

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});


function callPythonFunction(inputData) {
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python3', ['my_script.py', inputData]);

        let result = '';
        pythonProcess.stdout.on('data', (data) => {
            result += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`Error: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                reject(`Process exited with code ${code}`);
            } else {
                resolve(result.trim());
            }
        });
    });
}


app.post('/ask-agent', async (req, res) => {
    const question = req.body.question
    
    if (!question) {
        return res.status(400).json({ error: "Question is required" });
    }

    try {
        const result = await callPythonFunction(question);
        res.json({ success: true, result });
    } catch (error) {
        res.status(500).json({ success: false, error: error.toString() });
    }
});