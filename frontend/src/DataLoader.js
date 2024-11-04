// src/DataLoader.js

import React, { useEffect } from 'react';
import Papa from 'papaparse';

const DataLoader = ({ onDataLoaded }) => {
  useEffect(() => {
    fetch('/calculated_data.csv')
      .then(response => response.text())
      .then(text => {
        const result = Papa.parse(text, { header: true });
        onDataLoaded(result.data);
      });
  }, [onDataLoaded]);

  return null;
};

export default DataLoader;
