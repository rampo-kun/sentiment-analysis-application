/* eslint-disable no-unused-vars */
import { useState, useCallback, useEffect } from "react";
import axios from "axios";
import debounce from "lodash.debounce";

function App() {
  const [text, setText] = useState("");
  const [sentiment, setSentiment] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sentimentLabels = {
    0: "negative",
    1: "neutral",
    2: "positive",
  };

  const analyzeSentiment = async (text) => {
    setLoading(true);
    setError(null);
    setSentiment(null);

    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", {
        text,
      });
      const sentimentValue = response.data.sentiment;
      setSentiment(sentimentLabels[sentimentValue]);
    } catch (error) {
      setError("Error fetching sentiment analysis");
    } finally {
      setLoading(false);
    }
  };

  const debouncedAnalyzeSentiment = useCallback(
    debounce(analyzeSentiment, 500),
    []
  );

  const handleChange = (e) => {
    const newText = e.target.value;
    setText(newText);
    debouncedAnalyzeSentiment(newText);
  };

  useEffect(() => {
    // Update the body class based on sentiment
    if (sentiment) {
      document.body.classList.remove("positive", "neutral", "negative");
      document.body.classList.add(sentiment);
    }
  }, [sentiment]);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Sentiment Analysis</h1>
      <textarea
        value={text}
        onChange={handleChange}
        placeholder="Enter text"
        rows={5}
        style={{ width: "100%", marginBottom: "10px" }}
      />
      {loading && <p>Analyzing...</p>}
      {sentiment && (
        <div className="result">
          <h2>Sentiment Result:</h2>
          <h3>{sentiment}</h3>
        </div>
      )}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default App;
