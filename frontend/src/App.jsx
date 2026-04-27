import { useState } from "react";
import "./App.css";

export default function App() {
  const [url, setUrl] = useState("");
  const [output, setOutput] = useState("");

  async function explain() {
    const res = await fetch("http://localhost:8000/explain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
    const data = await res.json();
    setOutput(data.explanation);
  }

  return (
    <div>
      <input value={url} onChange={e => setUrl(e.target.value)} placeholder="Paste Bluesky URL" />
      <button onClick={explain}>Explain</button>
      <pre>{output}</pre>
    </div>
  );
}
