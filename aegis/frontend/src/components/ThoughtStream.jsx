import { useEffect, useRef } from "react";

export default function ThoughtStream({ thoughts }) {
  const ref = useRef(null);

  useEffect(() => {
    if (ref.current) {
      ref.current.scrollTop = ref.current.scrollHeight;
    }
  }, [thoughts]);

  return (
    <div className="thought-stream" ref={ref}>
      {thoughts.map((thought, index) => (
        <div className="thought-line" key={`${thought.timestamp}-${index}`}>
          <span>{thought.agent}</span>
          <p>{thought.text}</p>
        </div>
      ))}
      {thoughts.length === 0 && <p className="muted">Waiting for first signal.</p>}
    </div>
  );
}

