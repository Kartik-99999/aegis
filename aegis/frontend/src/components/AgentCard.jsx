export default function AgentCard({ agent, score }) {
  return (
    <article className="agent-card">
      <div>
        <h3>{agent.name}</h3>
        <p>{agent.role || agent.task}</p>
      </div>
      <div className="agent-meta">
        <span className={`status-dot ${agent.status || "spawned"}`} />
        <span>{agent.status || "spawned"}</span>
        {typeof score === "number" && <strong>{Math.round(score * 100)}%</strong>}
      </div>
    </article>
  );
}

