const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export async function fetchAlerts() {
  const res = await fetch(`${API_URL}/alerts`);
  if (!res.ok) throw new Error('Failed to fetch alerts');
  return res.json();
}

export async function fetchTriageRules() {
  const res = await fetch(`${API_URL}/triage_rules`);
  if (!res.ok) throw new Error('Failed to fetch triage rules');
  return res.json();
} 