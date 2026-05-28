import { motion } from "framer-motion";
import { Play, Sparkles } from "lucide-react";
import { useState } from "react";

const defaultGoal = "Increase e-commerce revenue by 20% without raising ad spend.";

export default function Home({ onLaunch, isLaunching, error }) {
  const [goal, setGoal] = useState(defaultGoal);

  async function handleSubmit(event) {
    event.preventDefault();
    await onLaunch(goal);
  }

  return (
    <main className="home-shell">
      <motion.section
        className="launch-console"
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <div className="brand-lockup">
          <span className="brand-mark">
            <Sparkles size={22} />
          </span>
          <div>
            <p className="eyebrow">AEGIS</p>
            <h1>Adaptive Emergent General Intelligence System</h1>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="goal-form">
          <label htmlFor="goal">Goal</label>
          <textarea
            id="goal"
            value={goal}
            onChange={(event) => setGoal(event.target.value)}
            minLength={8}
            rows={5}
          />
          {error && <p className="error-text">{error}</p>}
          <button className="launch-button" type="submit" disabled={isLaunching}>
            <Play size={18} />
            <span>{isLaunching ? "Launching" : "Launch AEGIS"}</span>
          </button>
        </form>
      </motion.section>
    </main>
  );
}

