---
layout: base
title: Volunteer Schedule
permalink: /volunteer-schedule
---

<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  :root {
    --bg-base: #f0ebe2;
    --primary-dark: #000000;
    --primary-pure: #ffffff;
    --accent-wood: #4a3f35;
    --text-main: #1f1b17;
    --text-soft: #4a3f35;
    --border-light: #e2dbd0;
    --shadow-sm: 0 8px 20px rgba(0,0,0,0.03), 0 2px 4px rgba(0,0,0,0.05);
    --shadow-md: 0 12px 28px rgba(0,0,0,0.06);
  }
  body { background: var(--bg-base); font-family: 'Inter', system-ui, sans-serif; }
  .page-content, .wrapper { max-width: none !important; padding: 0 !important; background: var(--bg-base) !important; }
  .vol-page { background: var(--bg-base); min-height: 100vh; }
  .vol-wrap { max-width: 1400px; margin: 0 auto; padding: 24px 28px 48px; display: flex; flex-direction: column; gap: 24px; }
  .vol-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; border-bottom: 2px solid var(--accent-wood); padding-bottom: 8px; }
  .vol-title h1 { font-size: 1.9rem; font-weight: 700; color: var(--primary-dark); }
  .vol-title p { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.2px; color: var(--accent-wood); margin-top: 6px; }
  .vol-back { background: var(--primary-pure); border: 1px solid var(--border-light); border-radius: 60px; padding: 8px 20px; text-decoration: none; font-weight: 600; color: var(--accent-wood); }
  .vol-back:hover { background: var(--accent-wood); color: white; }
  .stats-row { display: flex; flex-wrap: wrap; gap: 20px; }
  .stat-card { background: var(--primary-pure); border-radius: 28px; padding: 18px 24px; flex: 1 1 180px; box-shadow: var(--shadow-sm); border: 1px solid var(--border-light); }
  .stat-card .stat-label { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: var(--accent-wood); }
  .stat-card .stat-number { font-size: 2.2rem; font-weight: 800; color: var(--primary-dark); margin-top: 8px; }
  .filters { display: flex; flex-wrap: wrap; gap: 16px; justify-content: space-between; }
  .filter-buttons { display: flex; flex-wrap: wrap; gap: 10px; }
  .filter-btn { background: var(--primary-pure); border: 1px solid var(--border-light); padding: 8px 18px; border-radius: 40px; font-size: 0.8rem; font-weight: 600; cursor: pointer; }
  .filter-btn.active { background: var(--accent-wood); color: white; }
  .search-box { display: flex; align-items: center; background: var(--primary-pure); border: 1px solid var(--border-light); border-radius: 48px; padding: 6px 16px; gap: 8px; }
  .search-box input { border: none; background: transparent; padding: 8px 4px; width: 180px; outline: none; }
  .schedule-table-container { background: var(--primary-pure); border-radius: 28px; box-shadow: var(--shadow-md); overflow-x: auto; border: 1px solid var(--border-light); }
  .vol-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; min-width: 880px; }
  .vol-table th { text-align: left; padding: 18px 16px; background: #faf8f4; border-bottom: 1px solid var(--border-light); font-weight: 700; color: var(--accent-wood); }
  .vol-table td { padding: 18px 16px; border-bottom: 1px solid #ede6dd; }
  .vol-table tr:hover td { background-color: #fefcf9; }
  .date-cell { font-weight: 700; white-space: nowrap; }
  .badge-event { display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 60px; font-size: 0.75rem; font-weight: 600; background: #f2ede6; border: 1px solid #e2d9cf; }
  .volunteer-buttons { display: flex; gap: 10px; flex-wrap: wrap; }
  .vol-btn { background: #f4f0ea; border: 1px solid var(--border-light); padding: 6px 14px; border-radius: 40px; font-size: 0.7rem; font-weight: 600; cursor: pointer; }
  .vol-btn.signup { background: var(--accent-wood); color: white; }
  .vol-btn.signup:hover { background: #2c241e; }
  .vol-btn.cancel { background: #fff0ea; color: #8b5a3c; }
  .vol-status { font-size: 0.7rem; background: #f2ede6; display: inline-block; padding: 5px 12px; border-radius: 40px; }
  .slot-full { color: #b45a2b; font-size: 0.7rem; margin-top: 5px; }
  .shift-count { font-size: 0.7rem; color: var(--text-soft); margin-top: 6px; }
</style>

<div class="vol-page">
<div class="vol-wrap">
  <div class="vol-header">
    <div class="vol-title">
      <h1>Volunteer Crew Schedule</h1>
      <p>Poway–Midland Railroad · Operations Sign-up</p>
    </div>
    <a href="{{ "/calendar" | relative_url }}" class="vol-back">← Back to Calendar</a>
  </div>

  <div class="stats-row">
    <div class="stat-card"><div class="stat-label">Total Shifts</div><div class="stat-number" id="totalShifts">—</div></div>
    <div class="stat-card"><div class="stat-label">Open Spots</div><div class="stat-number" id="openSpots">—</div></div>
    <div class="stat-card"><div class="stat-label">Signed Up</div><div class="stat-number" id="signedUpCount">—</div></div>
    <div class="stat-card"><div class="stat-label">Steam Saturdays</div><div class="stat-number" id="steamCount">—</div></div>
  </div>

  <div class="filters">
    <div class="filter-buttons">
      <button class="filter-btn active" data-filter="all">All shifts</button>
      <button class="filter-btn" data-filter="steam">🔥 Steam</button>
      <button class="filter-btn" data-filter="cable">🚋 Cable Car</button>
      <button class="filter-btn" data-filter="speeder">🚃 Speeder</button>
      <button class="filter-btn" data-filter="open">🟢 Open spots</button>
      <button class="filter-btn" data-filter="my">⭐ My sign-ups</button>
    </div>
    <div class="search-box"><span>🔍</span><input type="text" id="searchInput" placeholder="Search by date" autocomplete="off"></div>
  </div>

  <div class="schedule-table-container">
    <table class="vol-table">
      <thead><tr><th>Date & Day</th><th>Operation Type</th><th>Time</th><th>Volunteer Slots (max 4)</th><th>Actions</th></tr></thead>
      <tbody id="tableBody"><tr><td colspan="5" style="text-align:center;padding:48px;">Loading schedule from server...</td></tr></tbody>
    </table>
  </div>
</div>
</div>

<script>
const API_BASE = 'http://localhost:8428/api';
let allShifts = [];
let currentFilter = "all";
let searchQuery = "";
let currentUserEmail = localStorage.getItem('volunteer_email') || '';
let currentUserName = localStorage.getItem('volunteer_name') || '';

async function loadShifts() {
  try {
    const response = await fetch(`${API_BASE}/volunteer/shifts`);
    if (!response.ok) throw new Error('Failed to load');
    allShifts = await response.json();
    renderTable();
    updateStats();
  } catch (error) {
    document.getElementById('tableBody').innerHTML = `<tr><td colspan="5" style="text-align:center;padding:48px;color:red;">❌ Failed to load schedule. Make sure backend is running on port 8428.</td></tr>`;
  }
}

async function signUpForShift(shiftId) {
  if (!currentUserEmail || !currentUserName) {
    const name = prompt("Enter your full name:");
    const email = prompt("Enter your email address:");
    if (!name || !email) return;
    currentUserName = name;
    currentUserEmail = email;
    localStorage.setItem('volunteer_name', name);
    localStorage.setItem('volunteer_email', email);
  }
  
  const job = prompt("Select job: Conductor, Ticket Taker, Safety Officer, Engineer, Fireman, Brake Operator", "Conductor");
  if (!job) return;
  
  try {
    const response = await fetch(`${API_BASE}/volunteer/shifts/${shiftId}/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: currentUserName, email: currentUserEmail, phone: '', job: job })
    });
    if (!response.ok) { const err = await response.json(); alert(err.error || 'Sign up failed'); return; }
    alert('✅ Successfully signed up!');
    loadShifts();
  } catch (error) { alert('Network error'); }
}

async function cancelSignUp(shiftId) {
  if (!confirm('Cancel your sign-up?')) return;
  try {
    const response = await fetch(`${API_BASE}/volunteer/shifts/${shiftId}/signup`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: currentUserEmail })
    });
    if (!response.ok) { const err = await response.json(); alert(err.error || 'Cancel failed'); return; }
    alert('✅ Cancelled');
    loadShifts();
  } catch (error) { alert('Network error'); }
}

function isUserSignedUp(shift) {
  if (!currentUserEmail) return false;
  return shift.volunteers && shift.volunteers.some(v => v.email === currentUserEmail);
}

function formatDate(dateStr) {
  const months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const weekdays = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const [y,m,d] = dateStr.split('-');
  const date = new Date(y, m-1, d);
  return `${months[parseInt(m)-1]} ${parseInt(d)}, ${y}<br><span style="font-size:0.7rem;color:var(--text-soft);">${weekdays[date.getDay()]}</span>`;
}

function renderTable() {
  let filtered = [...allShifts];
  if (currentFilter === 'steam') filtered = filtered.filter(s => s.train_type === 'steam');
  else if (currentFilter === 'cable') filtered = filtered.filter(s => s.train_type === 'cable');
  else if (currentFilter === 'speeder') filtered = filtered.filter(s => s.train_type === 'speeder');
  else if (currentFilter === 'open') filtered = filtered.filter(s => s.slots_available > 0);
  else if (currentFilter === 'my') filtered = filtered.filter(s => isUserSignedUp(s));
  
  if (searchQuery) {
    const q = searchQuery.toLowerCase();
    filtered = filtered.filter(s => s.date.includes(q));
  }
  filtered.sort((a,b) => new Date(a.date) - new Date(b.date));
  
  const tbody = document.getElementById('tableBody');
  if (filtered.length === 0) { tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:48px;">✨ No shifts match the filter ✨</td></tr>'; return; }
  
  tbody.innerHTML = filtered.map(shift => {
    const isSigned = isUserSignedUp(shift);
    const isFull = shift.slots_available === 0;
    const icons = { steam: '🔥', cable: '🚋', speeder: '🚃' };
    const labels = { steam: 'Steam Locomotive', cable: 'Cable Car', speeder: 'Speeder' };
    const volunteerNames = shift.volunteers?.length ? shift.volunteers.map(v => `${v.name} (${v.job})`).join(', ') : '— no volunteers yet';
    
    return `<tr>
      <td class="date-cell">${formatDate(shift.date)}</td>
      <td><span class="badge-event">${icons[shift.train_type] || '🚂'} ${labels[shift.train_type] || shift.train_type}</span></td>
      <td>${shift.time_start} – ${shift.time_end}</td>
      <td><strong>${shift.current_volunteers}/${shift.max_volunteers} slots filled</strong><div class="shift-count">👥 ${volunteerNames}</div>${isFull ? '<div class="slot-full">⚠️ Shift full</div>' : `<div style="color:#4a3f35;font-size:0.7rem;">✅ ${shift.slots_available} spot(s) open</div>`}</td>
      <td class="volunteer-buttons">
        ${(!isSigned && !isFull) ? `<button class="vol-btn signup" onclick="signUpForShift(${shift.id})">➕ Sign up</button>` : ''}
        ${isSigned ? `<button class="vol-btn cancel" onclick="cancelSignUp(${shift.id})">✖ Cancel</button>` : ''}
        ${isSigned ? '<span class="vol-status">✓ Signed</span>' : (isFull ? '<span class="vol-status">🔒 Full</span>' : '<span class="vol-status">Open</span>')}
      </td>
    </tr>`;
  }).join('');
}

function updateStats() {
  const total = allShifts.length;
  const openSpots = allShifts.reduce((s, shift) => s + shift.slots_available, 0);
  const signedUp = allShifts.reduce((s, shift) => s + shift.current_volunteers, 0);
  const steamDays = allShifts.filter(s => s.train_type === 'steam').length;
  document.getElementById('totalShifts').innerText = total;
  document.getElementById('openSpots').innerText = openSpots;
  document.getElementById('signedUpCount').innerText = signedUp;
  document.getElementById('steamCount').innerText = steamDays;
}

document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    renderTable();
  });
});
document.getElementById('searchInput').addEventListener('input', e => { searchQuery = e.target.value; renderTable(); });

loadShifts();
</script>
