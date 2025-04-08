import React, { useState, useEffect } from 'react';

function App() {
  const [location, setLocation] = useState(null);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [error, setError] = useState('');

  // Auto-fetch location on component mount
  useEffect(() => {
    if (!navigator.geolocation) {
      setError("Geolocation is not supported by your browser.");
      return;
    }
  
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const loc = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        };
        setLocation(loc);
        setError('');
  
        try {
          const response = await fetch('http://127.0.0.1:5001/rag/init', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(loc),
          });
  
          const data = await response.json();
          if (!response.ok) {
            setError(data.error || 'Index initialization failed');
          }
        } catch (err) {
          setError("Failed to initialize index.");
        }
      },
      () => {
        setError("Failed to retrieve your location.");
      }
    );
  }, []);
  

  const handleSubmit = async () => {
    if (!location || !question) {
      setError("Please ensure your location is fetched and question is filled.");
      return;
    }

    try {
      console.log("entered try!!!");
      const response = await fetch('http://127.0.0.1:5001/rag/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question,
          latitude: location.latitude,
          longitude: location.longitude,
        }),
      });

      const data = await response.json();
      if (data.answer) {
        setAnswer(data.answer);
        setError('');
      } else {
        setError(data.error || 'No answer received.');
      }
    } catch (err) {
      setError("Failed to contact server.");
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
      <h1>🍜 Restaurant RAG Assistant</h1>

      {location ? (
        <iframe
          title="Your Location"
          width="100%"
          height="250"
          frameBorder="0"
          style={{ border: 0 }}
          src={`https://maps.google.com/maps?q=${location.latitude},${location.longitude}&z=15&output=embed`}
          allowFullScreen
        ></iframe>
      ) : (
        <p>📍 Trying to detect your location...</p>
      )}

      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Enter your question (e.g., What's a good sushi place nearby?)"
        rows={4}
        style={{ width: '100%', marginTop: '1rem' }}
      />

      <button onClick={handleSubmit} style={{ marginTop: '1rem' }}>
        🔍 Submit Question
      </button>

      {answer && (
        <div style={{ marginTop: '1rem', background: '#f0f0f0', padding: '1rem' }}>
          <strong>💬 LLM Answer:</strong>
          <p>{answer}</p>
        </div>
      )}

      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default App;