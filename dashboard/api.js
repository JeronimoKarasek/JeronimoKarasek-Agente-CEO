import { getSession } from './auth.js';
const API_BASE_URL = 'http://localhost:8080/api';

async function authedFetch(url, options = {}) {
  const session = await getSession();
  const token = session?.access_token;
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(url, { ...options, headers });
  if (!res.ok) throw new Error((await res.json()).detail || 'API request failed');
  return res.json();
}

export const runScout = (term='trending dropshipping product') => authedFetch(`${API_BASE_URL}/run/scout`, { method:'POST', body: JSON.stringify({ search_term: term }) });
export const getMetrics = () => authedFetch(`${API_BASE_URL}/metrics/summary`);
