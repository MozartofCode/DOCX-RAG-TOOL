import React, { useState } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);  // Show loading indicator
    setResponse('');  // Reset the response

    try {
      // Send the question to the backend
      const res = await fetch('http://localhost:3000/ask-agent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question }),
      });

      // Check for successful response
      if (!res.ok) {
        throw new Error('Failed to get response from backend');
      }

      const data = await res.json();
      setResponse(data.message || 'No response received');  // Assuming the backend returns a 'message' field
    } catch (err) {
      setResponse('Error: ' + err.message);
    }

    setLoading(false);  // Hide loading indicator
  };

  return (
    <div className="App">
      <h1>Ask the Agent</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          placeholder="Enter your question here"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows="4"
          cols="50"
        />
        <br />
        <button type="submit" disabled={loading}>
          {loading ? 'Sending...' : 'Submit'}
        </button>
      </form>

      {response && (
        <div className="response">
          <h3>Response:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default App;
