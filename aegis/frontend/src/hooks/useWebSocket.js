import { useEffect, useMemo, useState } from "react";

const WS_BASE = import.meta.env.VITE_WS_URL || "ws://localhost:8000";

const initialState = {
  phase: "queued",
  agents: {},
  thoughts: [],
  debate: [],
  scores: {},
  result: null,
  error: ""
};

export function useWebSocket(sessionId) {
  const [state, setState] = useState(initialState);

  useEffect(() => {
    if (!sessionId) {
      setState(initialState);
      return undefined;
    }

    setState(initialState);
    const socket = new WebSocket(`${WS_BASE}/ws/${sessionId}`);

    socket.onmessage = (message) => {
      const event = JSON.parse(message.data);
      setState((current) => reduceEvent(current, event));
    };

    socket.onerror = () => {
      setState((current) => ({ ...current, error: "WebSocket connection failed" }));
    };

    return () => socket.close();
  }, [sessionId]);

  return useMemo(() => state, [state]);
}

function reduceEvent(state, event) {
  switch (event.type) {
    case "phase_update":
      return { ...state, phase: event.phase };
    case "agent_spawned":
      return {
        ...state,
        agents: {
          ...state.agents,
          [event.agent]: {
            ...(state.agents[event.agent] || {}),
            name: event.agent,
            role: event.role,
            task: event.task,
            tools: event.tools || [],
            status: "spawned"
          }
        }
      };
    case "thought":
      return {
        ...state,
        thoughts: [...state.thoughts.slice(-80), event],
        agents: {
          ...state.agents,
          [event.agent]: {
            ...(state.agents[event.agent] || { name: event.agent }),
            status: inferStatus(event.text)
          }
        }
      };
    case "debate_attack":
      return { ...state, debate: [...state.debate.slice(-50), event] };
    case "debate_defense":
      return {
        ...state,
        debate: [...state.debate.slice(-50), event],
        agents: {
          ...state.agents,
          [event.from]: {
            ...(state.agents[event.from] || { name: event.from }),
            status: "debated"
          }
        }
      };
    case "score_update":
      return {
        ...state,
        scores: { ...state.scores, [event.agent]: event.score }
      };
    case "session_complete":
      return { ...state, phase: "complete", result: event.result };
    case "session_error":
      return { ...state, phase: "failed", error: event.error };
    default:
      return state;
  }
}

function inferStatus(text = "") {
  const lowered = text.toLowerCase();
  if (lowered.includes("submitted")) return "complete";
  if (lowered.includes("reviewing critic")) return "defending";
  if (lowered.includes("starting")) return "thinking";
  return "running";
}
