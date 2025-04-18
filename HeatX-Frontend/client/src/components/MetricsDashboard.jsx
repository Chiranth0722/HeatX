import React, { useEffect, useState } from "react";
import axios from "axios";

function MetricsDashboard() {
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/metrics");
        setMetrics(response.data);
      } catch (err) {
        setError("Failed to fetch metrics");
        console.error(err);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000); // update every 5s
    return () => clearInterval(interval);
  }, []);

  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg w-full max-w-lg text-white">
      <h2 className="text-2xl font-semibold mb-4">System Metrics 🌡️</h2>
      {metrics ? (
        <ul className="space-y-2">
          <li>🧠 CPU Usage: {metrics.cpu_usage}%</li>
          <li>💾 RAM Usage: {metrics.ram_usage}%</li>
          <li>🔥 Temperature: {metrics.temperature}°C</li>
        </ul>
      ) : (
        <p>Loading metrics...</p>
      )}
    </div>
  );
}

export default MetricsDashboard;
