export default function DebateArena({ events }) {
  return (
    <div className="debate-list">
      {events.map((event, index) => (
        <article
          key={`${event.timestamp}-${index}`}
          className={event.type === "debate_attack" ? "debate-item attack" : "debate-item defense"}
        >
          <div>
            <span>{event.type === "debate_attack" ? event.from : event.from}</span>
            {event.target && <small>to {event.target}</small>}
          </div>
          <p>{event.text}</p>
        </article>
      ))}
      {events.length === 0 && <p className="muted">Debate opens after agent outputs land.</p>}
    </div>
  );
}

