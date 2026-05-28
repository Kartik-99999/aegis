import { Activity, RotateCcw, ShieldCheck, Wifi, WifiOff } from "lucide-react";
import { useMemo } from "react";
import AgentCard from "./components/AgentCard.jsx";
import AgentGraph from "./components/AgentGraph.jsx";
import ConfidenceMeter from "./components/ConfidenceMeter.jsx";
import DebateArena from "./components/DebateArena.jsx";
import ResultPanel from "./components/ResultPanel.jsx";
import ThoughtStream from "./components/ThoughtStream.jsx";
import { useAegisSession } from "./hooks/useAegisSession.js";
import { useWebSocket } from "./hooks/useWebSocket.js";
import Home from "./pages/Home.jsx";

export default function App() {
  const { session, isLaunching, error, startSession, resetSession } = useAegisSession();
  const live = useWebSocket(session?.session_id);

  const agents = useMemo(() => Object.values(live.agents), [live.agents]);
  const overall = live.scores.Overall ?? 0;

  if (!session) {
    return <Home onLaunch={startSession} isLaunching={isLaunching} error={error} />;
  }

  // Determine if we have an active WebSocket connection
  const isConnected = !live.error;

  return (
    <main className="app-shell">
      <header className="command-header">
        <div>
          <p className="eyebrow">AEGIS Command Center</p>
          <h1>Session #{session.session_id}</h1>
          <p className="goal-line">{session.goal}</p>
        </div>
        
        <div className="header-actions">
          {/* New Connection Status Indicator */}
          <div 
            className="phase-pill" 
            style={{ 
              color: isConnected ? 'var(--teal)' : 'var(--rose)',
              borderColor: isConnected ? 'rgba(70, 211, 154, 0.2)' : 'rgba(239, 71, 111, 0.2)'
            }}
          >
            {isConnected ? <Wifi size={16} /> : <WifiOff size={16} />}
            <span>{isConnected ? 'Live' : 'Disconnected'}</span>
          </div>

          <div className="phase-pill">
            <Activity size={16} />
            <span>{formatPhase(live.phase || session.status)}</span>
          </div>
          
          <button className="icon-button" onClick={resetSession} aria-label="Reset session" title="Start New Session">
            <RotateCcw size={18} />
          </button>
        </div>
      </header>

      <section className="dashboard-grid">
        <div className="panel graph-panel">
          <div className="panel-title">
            <ShieldCheck size={17} />
            <span>Agent Network</span>
          </div>
          <AgentGraph agents={agents} phase={live.phase} />
        </div>

        <div className="panel stream-panel">
          <div className="panel-title">
            <Activity size={17} />
            <span>Live Thought Stream</span>
          </div>
          <ThoughtStream thoughts={live.thoughts} />
        </div>

        <div className="panel agent-panel">
          <div className="panel-title">
            <span>Agent State</span>
          </div>
          <div className="agent-list">
            {agents.map((agent) => (
              <AgentCard key={agent.name} agent={agent} score={live.scores[agent.name]} />
            ))}
            {agents.length === 0 && !live.error && (
              <p className="muted" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span className="status-dot running pulse-ring"></span>
                Agents are assembling...
              </p>
            )}
          </div>
        </div>

        <div className="panel debate-panel">
          <div className="panel-title">
            <span>Debate Arena</span>
          </div>
          <DebateArena events={live.debate} />
        </div>

        <div className="panel confidence-panel">
          <div className="panel-title">
            <span>Confidence Scores</span>
          </div>
          <ConfidenceMeter scores={live.scores} overall={overall} />
        </div>

        <div className="panel result-panel">
          <div className="panel-title">
            <span>Final Output</span>
          </div>
          <ResultPanel result={live.result} error={live.error} />
        </div>
      </section>
    </main>
  );
}

function formatPhase(phase) {
  return String(phase || "queued")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}
