import * as d3 from "d3";
import { useEffect, useMemo, useRef } from "react";

const fallbackAgents = [
  { name: "Market Analyst", status: "standby" },
  { name: "Psych Agent", status: "standby" },
  { name: "Growth Agent", status: "standby" },
  { name: "Executor Agent", status: "standby" }
];

export default function AgentGraph({ agents, phase }) {
  const ref = useRef(null);
  const graph = useMemo(() => buildGraph(agents.length ? agents : fallbackAgents), [agents]);

  useEffect(() => {
    const svg = d3.select(ref.current);
    svg.selectAll("*").remove();

    const width = 720;
    const height = 430;
    const simulation = d3
      .forceSimulation(graph.nodes.map((node) => ({ ...node })))
      .force(
        "link",
        d3
          .forceLink(graph.links.map((link) => ({ ...link })))
          .id((node) => node.id)
          .distance((link) => (link.target === "Critic Agent" ? 140 : 110))
      )
      .force("charge", d3.forceManyBody().strength(-460))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide().radius(54));

    const link = svg
      .append("g")
      .attr("stroke", "rgba(114, 239, 221, 0.34)")
      .attr("stroke-width", 1.4)
      .selectAll("line")
      .data(graph.links)
      .join("line");

    const node = svg
      .append("g")
      .selectAll("g")
      .data(simulation.nodes())
      .join("g")
      .attr("class", "graph-node");

    node
      .append("circle")
      .attr("r", (item) => (item.type === "core" ? 34 : 27))
      .attr("fill", (item) => nodeColor(item))
      .attr("stroke", "rgba(255,255,255,0.58)")
      .attr("stroke-width", 1.2);

    node
      .append("circle")
      .attr("r", (item) => (item.status === "running" || item.status === "thinking" ? 40 : 0))
      .attr("fill", "none")
      .attr("stroke", "rgba(244, 177, 73, 0.46)")
      .attr("stroke-width", 2)
      .attr("class", "pulse-ring");

    node
      .append("text")
      .attr("text-anchor", "middle")
      .attr("dy", 4)
      .text((item) => shortName(item.id))
      .attr("fill", "#f8fbff")
      .attr("font-size", 12)
      .attr("font-weight", 700);

    node.append("title").text((item) => `${item.id} - ${item.status || phase}`);

    simulation.on("tick", () => {
      link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      node.attr("transform", (d) => `translate(${d.x},${d.y})`);
    });

    return () => simulation.stop();
  }, [graph, phase]);

  return <svg ref={ref} className="agent-graph" viewBox="0 0 720 430" role="img" />;
}

function buildGraph(agents) {
  const hasCritic = agents.some((agent) => agent.name === "Critic Agent");
  const agentNodes = agents.map((agent) => ({
    id: agent.name,
    type: agent.name === "Critic Agent" ? "critic" : "agent",
    status: agent.status
  }));
  const nodes = [{ id: "Orchestrator", type: "core", status: "active" }, ...agentNodes];
  const links = agentNodes
    .filter((node) => node.id !== "Critic Agent")
    .map((node) => ({ source: "Orchestrator", target: node.id }));

  if (hasCritic) {
    links.push(
      ...agentNodes
        .filter((node) => node.id !== "Critic Agent")
        .map((node) => ({ source: "Critic Agent", target: node.id }))
    );
  }
  return { nodes, links };
}

function nodeColor(item) {
  if (item.type === "core") return "#16b7c8";
  if (item.type === "critic") return "#ef476f";
  if (item.status === "complete" || item.status === "debated") return "#46d39a";
  if (item.status === "thinking" || item.status === "running") return "#f4b149";
  return "#5c6bc0";
}

function shortName(name) {
  if (name === "Orchestrator") return "O";
  if (name === "Market Analyst") return "M";
  if (name === "Psych Agent") return "P";
  if (name === "Growth Agent") return "G";
  if (name === "Executor Agent") return "E";
  if (name === "Critic Agent") return "C";
  return name.slice(0, 1);
}

