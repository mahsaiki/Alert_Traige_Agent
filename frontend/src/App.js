import React, { useEffect, useState } from 'react';
import { fetchAlerts, fetchTriageRules } from './api';

function App() {
  const [alerts, setAlerts] = useState([]);
  const [rules, setRules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [alertsData, rulesData] = await Promise.all([
          fetchAlerts(),
          fetchTriageRules()
        ]);
        setAlerts(alertsData);
        setRules(rulesData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{color: 'red'}}>Error: {error}</div>;

  return (
    <div style={{ padding: 32 }}>
      <h1>Alert Triage Agent Dashboard</h1>
      <h2>Alerts</h2>
      <ul>
        {alerts.length === 0 && <li>No alerts</li>}
        {alerts.map(alert => (
          <li key={alert.id}>
            <strong>{alert.title}</strong> [{alert.severity}] - {alert.status}<br/>
            <small>{alert.message}</small>
          </li>
        ))}
      </ul>
      <h2>Triage Rules</h2>
      <ul>
        {rules.length === 0 && <li>No triage rules</li>}
        {rules.map(rule => (
          <li key={rule.id}>
            <strong>{rule.name}</strong> (Priority: {rule.priority})<br/>
            <small>{rule.description}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App; 