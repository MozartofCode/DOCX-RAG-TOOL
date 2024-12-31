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
    console.log("inside the python function")
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('C:\\Users\\berta\\AppData\\Local\\Programs\\Python\\Python311\\python.exe', ['run_agent.py', inputData]);

        let result = '';
        pythonProcess.stdout.on('data', (data) => {
            console.log("HERE1")
            result += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            console.log("HERE2")
            console.error(`Error: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            console.log("HERE3")
            if (code !== 0) {
                console.log("HERE4")
                reject(`Process exited with code ${code}`);
            } else {
                console.log("HERE5")
                console.log(result.trim())
                console.log(result)
                resolve(result.trim());
            }
        });
    });
}


app.post('/ask-agent', async (req, res) => {
    console.log("inside the agent function")
    const question = req.body.question
    
    if (!question) {
        return res.status(400).json({ error: "Question is required" });
    }

    try {
        const result = await callPythonFunction(question);
        console.log("result: ", result)
        res.json({ success: true, result });
    } catch (error) {
        console.log("error: ", error)
        res.status(500).json({ success: false, error: error.toString() });
    }
});