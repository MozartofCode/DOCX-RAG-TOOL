
require('dotenv').config();
const express = require('express');
const { spawn } = require('child_process');
const app = express();

const port = process.env.PORT || 3001;
const axios = require('axios');

app.use(express.json());

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});


app.post('/ask-agent', (req, res) => {
    const question = req.body.question;

    if (!question) {
        return res.status(400).json({ error: "Question is required" });
    }

    const pythonProcess = spawn('python3', ['run_agent.py', question]);

    let output = '';
    pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        if (code === 0) {
            try {
                const response = JSON.parse(output);
                res.json(response);
            } catch (err) {
                console.error('Error parsing Python response:', err);
                res.status(500).send('Error parsing Python response');
            }
        } else {
            console.error('Python script failed with code:', code);
            res.status(500).send('Python script failed');
        }
    });
});

app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});