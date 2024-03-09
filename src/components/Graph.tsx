'use client'

import React, { useEffect } from 'react';
import * as d3 from 'd3';

const Graph = () => {
  useEffect(() => {
    // D3.js code for creating a basic bar chart
    const data = [10, 20, 30, 40, 50];

    const svg = d3.select('#chart-container')
      .append('svg')
      .attr('width', 400)
      .attr('height', 200);

    svg.selectAll('rect')
      .data(data)
      .enter()
      .append('rect')
      .attr('x', (_:number, i:number) => i * 80)
      .attr('y', (d:number) => 200 - d)
      .attr('width', 75)
      .attr('height', (d:number) => d)
      .attr('fill', 'blue');
  }, []);

  return <div id="chart-container"></div>;
};

export default Graph;

