import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Fetch data from the backend API
    fetch('http://localhost:3000/api/data')
      .then(response => response.json())
      .then(data => {
        setData(data.message);
      })
      .catch(error => console.error('Error:', error));
  }, []);

  return (
    <div>
      {data ? data : 'Loading...'}
    </div>
  );
}

export default App;
