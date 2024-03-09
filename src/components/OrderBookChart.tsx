'use client'

// components/OrderBookChart.js
import { useEffect } from 'react';
import * as d3 from 'd3';

const floorWidth = (money:number,binWidth:number) => {
  return Math.floor(money / binWidth)*binWidth
}
const ceilWidth = (money:number,binWidth:number) => {
  return Math.ceil(money / binWidth)*binWidth
}

const OrderBookChart = (orderBookData:OrderBook) => {
  console.log('Rendering OrderBookChart component');
  useEffect(() => {
    if (!orderBookData) return;

//TODO: NEEDS OUTLIER PROTECTION

const combinedData = [...orderBookData.bid, ...orderBookData.ask];

// Create an array of prices with repetition based on quantity
const pricesWithQuantity = combinedData.flatMap((order: Order) =>
  Array(order.quantity).fill(order.price)
);

//Remove old histogram.
d3. select('#orderBookChart').selectAll('svg').remove() 
// Use D3.js to create a histogram
const width = 800;
const height = 300;
const bin_width = 0.01;
const svg = d3.select('#orderBookChart').append('svg').attr('width', width).attr('height', height);

const min = floorWidth(d3.min(pricesWithQuantity),bin_width);
const max = ceilWidth(d3.max(pricesWithQuantity),bin_width);
const nbins = ((max-min)/bin_width) - 1;
const histogram_height = 20000;
const bins = d3.histogram()
  .value((d: number) => d) // Accessor function for values (prices)
  .domain([min, max]) // Domain based on min and max prices
  .thresholds(nbins)(pricesWithQuantity); // Calculate bins using the pricesWithQuantity array

const axis_size = 50;
const start_x = axis_size;
const end_x = width - axis_size;
const start_y = height - axis_size;
const end_y = axis_size;
// Render the histogram
const x = d3.scaleLinear()
  .domain([min, max]) // Set the domain based on min and max prices
  .range([start_x, end_x]); // Set the range for the x-axis, leaving space for the y-axis

// const y = d3.scaleLinear()
//   .domain([0, d3.max(bins, (d:any) => d.length)]) // Set the domain based on the maximum bin length
//   .range([start_y, end_y]); // Set the range for the y-axis, leaving space for the x-axis

const y = d3.scaleLinear()
  .domain([0, histogram_height]) // Set the domain based on the specified value
  .range([start_y, end_y]); // Set the range for the y-axis, leaving space for the x-axis

const xAxis = d3.axisBottom(x);
const yAxis = d3.axisLeft(y);

svg.append('g')
  .attr('transform', 'translate(0, '+start_y+')') // Position the x-axis
  .call(xAxis);

svg.append('g')
  .attr('transform', 'translate('+start_x+', 0)') // Position the y-axis
  .call(yAxis);

svg.selectAll('rect')
  .data(bins)
  .enter()
  .append('rect')
  .attr('x', (d: any) => x(d.x0))
  .attr('y', (d: any) => y(d.length))
  .attr('width', (d: any) => x(d.x1) - x(d.x0) - 1)
  .attr('height', (d: any) => (start_y) - y(d.length))
  .attr('fill', (d: any) => {
      const binRange = [d.x0, d.x1] as [number, number];
        const bidQuantity = orderBookData.bid.reduce((total, order) => {
          if (order.price >= binRange[0] && order.price < binRange[1]) {
            return total + order.quantity;
          }
          return total;
        }, 0);
        const askQuantity = orderBookData.ask.reduce((total, order) => {
          if (order.price >= binRange[0] && order.price < binRange[1]) {
            return total + order.quantity;
          }
          return total;
        }, 0);
        return bidQuantity > askQuantity ? 'lightgreen' : 'lightcoral';
      });

}, [orderBookData]);

  return <div id="orderBookChart" />;
};

export default OrderBookChart;

