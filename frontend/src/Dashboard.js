// src/Dashboard.js

import React, { useState, useEffect } from 'react';
import DataLoader from './DataLoader';
import BarChartComponent from './components/BarChartComponent';
import PieChartComponent from './components/PieChartComponent';

const Dashboard = () => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [selectedServiceType, setSelectedServiceType] = useState('');

  const handleDataLoaded = (loadedData) => {
    setData(loadedData);
    // Set default filtered data
    setFilteredData(loadedData);
  };

  useEffect(() => {
    if (selectedServiceType) {
      const filtered = data.filter(item => item.SERVICE_TYPE === selectedServiceType);
      setFilteredData(filtered);
    } else {
      setFilteredData(data);
    }
  }, [selectedServiceType, data]);

  const handleServiceTypeChange = (event) => {
    setSelectedServiceType(event.target.value);
  };

  const uniqueServiceTypes = [...new Set(data.map(item => item.SERVICE_TYPE))];

  return (
    <div style={{ padding: '20px' }}>
      <h1>Telecom Dashboard</h1>
      <DataLoader onDataLoaded={handleDataLoaded} />
      <div>
        <label htmlFor="serviceType">Select Service Type:</label>
        <select id="serviceType" onChange={handleServiceTypeChange} value={selectedServiceType}>
          <option value="">All</option>
          {uniqueServiceTypes.map(serviceType => (
            <option key={serviceType} value={serviceType}>{serviceType}</option>
          ))}
        </select>
      </div>
      {filteredData.length > 0 && (
        <div>
          <h2>Statistics for {selectedServiceType || 'All Service Types'}</h2>
          <BarChartComponent data={filteredData} />
          <PieChartComponent data={filteredData} />
        </div>
      )}
    </div>
  );
};

export default Dashboard;
