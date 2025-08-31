import React, { useEffect, useState } from 'react';
import { fetchHealth } from '../api/client';

const HealthCheck: React.FC = () => {
  const [message, setMessage] = useState<string>('Loading...');

  useEffect(() => {
    fetchHealth()
      .then((data) => setMessage(`Backend: ${data.status}`))
      .catch(() => setMessage('Backend: error'));
  }, []);

  return <div>{message}</div>;
};

export default HealthCheck;
