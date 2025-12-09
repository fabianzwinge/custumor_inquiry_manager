import React, { useEffect, useState } from 'react';

function App() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    fetch('/api/health')
      .then(res => res.json())
      .then(data => setHealth(data.status))
      .catch(() => setHealth('error'));
  }, []);

  return (
    <div className="App">
     
      <p>Backend Health: {health}</p>
    
    </div>
  );
}

export default App;