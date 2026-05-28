import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || 'https://aegis-elh0.onrender.com'

export function useAegisSession() {
  const [session, setSession] = useState(null);
  const [isLaunching, setIsLaunching] = useState(false);
  const [error, setError] = useState("");

  async function startSession(goal) {
    setIsLaunching(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE}/session/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ goal })
      });

      if (!response.ok) {
        throw new Error(`Launch failed with ${response.status}`);
      }

      const payload = await response.json();
      setSession({ ...payload, goal });
      return payload;
    } catch (err) {
      setError(err.message || "Launch failed");
      return null;
    } finally {
      setIsLaunching(false);
    }
  }

  function resetSession() {
    setSession(null);
    setError("");
  }

  return { session, isLaunching, error, startSession, resetSession };
}

