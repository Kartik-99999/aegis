export default function ConfidenceMeter({ scores, overall }) {
  const entries = Object.entries(scores).sort(([name]) => (name === "Overall" ? 1 : -1));

  return (
    <div className="meter-list">
      {entries.map(([name, score]) => (
        <div className="meter-row" key={name}>
          <div className="meter-label">
            <span>{name}</span>
            <strong>{Math.round(score * 100)}%</strong>
          </div>
          <div className="meter-track">
            <div className="meter-fill" style={{ width: `${Math.round(score * 100)}%` }} />
          </div>
        </div>
      ))}
      {!entries.length && (
        <div className="overall-placeholder">
          <strong>{Math.round(overall * 100)}%</strong>
          <span>Overall confidence</span>
        </div>
      )}
    </div>
  );
}

