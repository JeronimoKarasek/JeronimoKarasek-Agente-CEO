import { getSession } from './auth.js';
import { config } from './config.js';

async function authedFetch(url, options = {}) {
  const session = await getSession();
  const token = session?.access_token;
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(url, { ...options, headers });
  if (!res.ok) throw new Error((await res.json()).detail || 'API request failed');
  return res.json();
}

export const runScout = (term='trending dropshipping product') => authedFetch(`${config.API_BASE_URL}/run/scout`, { method:'POST', body: JSON.stringify({ search_term: term }) });
export const getMetrics = () => authedFetch(`${config.API_BASE_URL}/metrics/summary`);
export const getQueue = () => authedFetch(`${config.API_BASE_URL.replace('/api','')}/api/admin/queue`);
export const getConfig = () => authedFetch(`${config.API_BASE_URL.replace('/api','')}/api/admin/config`);
export const getAudit = () => authedFetch(`${config.API_BASE_URL.replace('/api','')}/api/admin/audit`);
