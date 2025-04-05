import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [location, setLocation] = useState(null);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const getLocation = () => {
    if (!navigator.geolocation) {
      setError("Geolocation is not supported by your browser.");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });
        setError('');
      },
      (err) => setError("Unable to retrieve your location.")
    );
  };

  const submitQuestion = async () => {
    if (!location || !question) {
      setError("Please get your location and enter a question.");
      return;
    }

    setLoading(true);
    setError('');
    setAnswer('');

    try {
      const response = await axios.post('https://your-api-endpoint.com/ask', {
        question,
        latitude: location.latitude,
        longitude: location.longitude
      });

      setAnswer(response.data.answer);
    } catch (err) {
      setError("Error fetching answer from server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20, maxWidth: 600, margin: "0 auto" }}>
      <h1>RAG Assistant</h1>
      <button onClick={getLocation}>📍 Get My Location</button>
      {location && (
        <p>Location: {location.latitude.toFixed(4)}, {location.longitude.toFixed(4)}</p>
      )}
      <textarea
        rows={4}
        style={{ width: "100%", marginTop: 10 }}
        placeholder="Ask me something..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={submitQuestion} disabled={loading} style={{ marginTop: 10 }}>
        {loading ? "Loading..." : "Submit"}
      </button>
      {answer && (
        <div style={{ marginTop: 20, padding: 10, backgroundColor: "#f0f0f0" }}>
          <strong>Answer:</strong> {answer}
        </div>
      )}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default App;
