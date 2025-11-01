import { login, logout } from './auth.js';
import { runScout, getMetrics } from './api.js';

const $ = (id)=>document.getElementById(id);

$("login").onclick = async () => {
  const email = $("email").value; const password = $("password").value;
  const { user, error } = await login(email, password);
  $("auth-info").textContent = error ? `Login error: ${error.message}` : `Logged as ${user?.email}`;
};
$("logout").onclick = async () => { await logout(); $("auth-info").textContent = 'Logged out'; };

$("btn-scout").onclick = async () => {
  try { const data = await runScout(); $("output").textContent = JSON.stringify(data, null, 2); }
  catch(e){ $("output").textContent = e.message; }
};

$("btn-metrics").onclick = async () => {
  try { const data = await getMetrics(); $("output").textContent = JSON.stringify(data, null, 2); }
  catch(e){ $("output").textContent = e.message; }
};
