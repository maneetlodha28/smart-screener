import React from 'react';
import HealthCheck from './components/HealthCheck';
import Landing from './pages/Landing';

const App: React.FC = () => {
  return (
    <div>
      <h1>Smart Screener</h1>
      <HealthCheck />
      <Landing />
    </div>
  );
};

export default App;
