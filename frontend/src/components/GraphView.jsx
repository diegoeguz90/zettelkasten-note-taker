import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import api from '../api';

export default function GraphView() {
  const svgRef = useRef();
  const [graphData, setGraphData] = useState(null);

  useEffect(() => {
    api.get('/graph').then(res => {
      setGraphData(res.data);
    }).catch(err => console.error(err));
  }, []);

  useEffect(() => {
    if (!graphData || !svgRef.current) return;

    const width = svgRef.current.parentElement.clientWidth;
    const height = svgRef.current.parentElement.clientHeight || 600;

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .call(d3.zoom().on('zoom', (event) => {
        svg.select('g').attr('transform', event.transform);
      }));

    svg.selectAll("*").remove(); // Clear previous render
    
    const g = svg.append("g");

    const nodes = graphData.nodes.map(d => Object.create(d));
    const links = graphData.edges.map(d => Object.create(d));

    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(150))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2));

    const link = g.append("g")
      .attr("stroke", "#94a3b8")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke-width", 2);

    const node = g.append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", 15)
      .attr("fill", "#3b82f6")
      .call(drag(simulation));

    const label = g.append("g")
      .selectAll("text")
      .data(nodes)
      .join("text")
      .text(d => d.label)
      .attr("font-size", 12)
      .attr("dx", 20)
      .attr("dy", 4)
      .attr("fill", "#f8fafc")
      .attr("stroke", "none");

    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
        
      label
        .attr("x", d => d.x)
        .attr("y", d => d.y);
    });

    function drag(simulation) {
      function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
      }
      
      function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      }
      
      function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
      }
      
      return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
    }
  }, [graphData]);

  return (
    <div className="p-4 flex-col h-full" style={{flex: 1}}>
      <div className="glass-panel w-full" style={{flex: 1, minHeight: '600px', padding: 0, overflow: 'hidden'}}>
        <svg ref={svgRef} style={{width: '100%', height: '100%'}}></svg>
      </div>
    </div>
  );
}
