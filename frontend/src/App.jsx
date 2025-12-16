import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [pasteText, setPasteText] = useState("");
  const [parsed, setParsed] = useState(null);
  const [jobText, setJobText] = useState("");
  const [matchResult, setMatchResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [weight, setWeight] = useState(0.6);

  const backendBase = "http://127.0.0.1:8000";

  const upload = async () => {
    setMatchResult(null);
    setParsed(null);
    setLoading(true);
    try {
      const form = new FormData();
      if (file) form.append("file", file);
      else form.append("paste_text", pasteText);

      const res = await axios.post(`${backendBase}/upload_resume`, form);
      setParsed(res.data);
    } catch (err) {
      alert("Upload error");
    } finally {
      setLoading(false);
    }
  };

  const aiMatch = async () => {
    if (!parsed?.parsed_text) return alert("Upload resume first");
    if (!jobText.trim()) return alert("Paste job description");

    setLoading(true);
    setMatchResult(null);
    try {
      const form = new FormData();
      form.append("resume_text", parsed.parsed_text);
      form.append("job_text", jobText);
      form.append("weight_semantic", String(weight));

      const res = await axios.post(`${backendBase}/ai_match`, form);
      setMatchResult(res.data);
    } catch (err) {
      alert("Match error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: "40px auto" }}>
      <h1>AI-RecruitX</h1>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <br /><br />

      <textarea
        placeholder="Or paste resume text"
        rows={5}
        style={{ width: "100%" }}
        value={pasteText}
        onChange={(e) => setPasteText(e.target.value)}
      />

      <br /><br />
      <button onClick={upload}>{loading ? "Uploading..." : "Upload Resume"}</button>

      {parsed && (
        <>
          <h3>Parsed Resume</h3>
          <pre>{parsed.parsed_text}</pre>

          <textarea
            placeholder="Paste Job Description"
            rows={5}
            style={{ width: "100%" }}
            value={jobText}
            onChange={(e) => setJobText(e.target.value)}
          />

          <br /><br />
          <label>
            Semantic Weight: {weight}
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={weight}
              onChange={(e) => setWeight(parseFloat(e.target.value))}
            />
          </label>

          <br /><br />
          <button onClick={aiMatch}>
            {loading ? "Matching..." : "Compute AI Match"}
          </button>
        </>
      )}

      {matchResult && (
        <>
          <h3>Match Result</h3>
          <p><b>Final:</b> {matchResult.final_score}%</p>
          <p><b>Semantic:</b> {matchResult.semantic_score}%</p>
          <p><b>Keyword:</b> {matchResult.keyword_score}%</p>

          <h4>Matched Skills</h4>
          <ul>
            {matchResult.matched_skills.map((s) => <li key={s}>{s}</li>)}
          </ul>

          <h4>Missing Skills</h4>
          <ul>
            {matchResult.missing_skills.map((s) => <li key={s}>{s}</li>)}
          </ul>
        </>
      )}
    </div>
  );
}

export default App;
