import React, { useState } from "react";
import axios from "axios";

function App() {
    const [code, setCode] = useState("");
    const [report, setReport] = useState("");

    const analyzeCode = async () => {
        if (!code.trim()) {
            alert("Please enter a code snippet.");
            return;
        }

        try {
            const response = await axios.post("https://codediagnoser.onrender.com", { code });
            setReport(response.data.report);
        } catch (error) {
            console.error("Error analyzing code:", error);
            setReport("Failed to analyze the code.");
        }
    };

    return (
        <div style={{ padding: "20px", maxWidth: "600px", margin: "auto" }}>
            <h2>Code Diagnoser</h2>
            <textarea
                rows="10"
                cols="50"
                placeholder="Enter your code here..."
                value={code}
                onChange={(e) => setCode(e.target.value)}
            ></textarea>
            <br />
            <button onClick={analyzeCode}>Analyze Code</button>
            <h3>Analysis Report:</h3>
            <pre style={{ whiteSpace: "pre-wrap", background: "#f4f4f4", padding: "10px" }}>{report}</pre>
        </div>
    );
}

export default App;
