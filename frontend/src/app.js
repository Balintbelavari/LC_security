import React, { useState } from "react";
import "./app.css";

function App() {
  const [message, setMessage] = useState("");
  const [prediction, setPrediction] = useState("");
  const [error, setError] = useState("");

  const handlePredict = async () => {
    try {
      setError("");
      setPrediction("");
      const response = await fetch("http://127.0.0.1:8001/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch prediction");
      }

      const data = await response.json();
      setPrediction(data.prediction);
    } catch (err) {
      setError("Error: " + err.message);
    }
  };

  return (
    <div className="container">
      <h1>Scam or Ham Predictor</h1>
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        rows="4"
        cols="50"
        placeholder="Enter your message here"
      />
      <br />
      <button onClick={handlePredict}>Predict</button>
      {prediction && (
        <p className="prediction">
          Prediction: <strong>{prediction}</strong>
        </p>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;
