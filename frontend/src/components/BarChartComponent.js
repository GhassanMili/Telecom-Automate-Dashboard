// src/components/BarChartComponent.js

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const BarChartComponent = ({ data }) => {
  // Map data to the required format
  const chartData = data.map(item => ({
    service_type: item.SERVICE_TYPE,
    nb_sms: parseInt(item.NB_SMS, 10) || 0,
    total_price: parseFloat(item.TOTAL_PRICE) || 0,
  }));

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart
        data={chartData}
        margin={{
          top: 20, right: 30, left: 20, bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="service_type" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="nb_sms" fill="#8884d8" />
        <Bar dataKey="total_price" fill="#82ca9d" />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default BarChartComponent;
