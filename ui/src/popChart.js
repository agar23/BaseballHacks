import React, { Component } from 'react';
import {
  ScatterChart, Scatter, XAxis, YAxis, ZAxis, CartesianGrid, Tooltip
} from 'recharts';
import PopData from './resources/population.json';

class attChart extends Component {
  render() {
    return (
        <ScatterChart
            width={this.props.width}
            height={this.props.height}
            margin={{
            top: 20, right: 20, bottom: 20, left: 20,
            }}>
            <CartesianGrid />
            <XAxis type="number" dataKey="x" name="Population"  />
            <YAxis type="number" dataKey="y" name="Wins" />
            <ZAxis type="number" dataKey="z" name="Year" />
            <Tooltip cursor={{ strokeDasharray: '3 3' }} />
        <Scatter name="A school" data={PopData.chartData} fill="#8884d8" />
      </ScatterChart>
    );
  }
};

export default attChart;