export default function ResultPanel({ result, error }) {
  if (error) {
    return <p className="error-text">{error}</p>;
  }

  if (!result) {
    return <p className="muted">Synthesis pending.</p>;
  }

  return (
    <div className="result-content">
      <p>{result.synthesis}</p>
      <h3>Action Plan</h3>
      <ol>
        {result.action_plan.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ol>
      <h3>Winner Logic</h3>
      <p>{result.winner_logic}</p>
    </div>
  );
}

