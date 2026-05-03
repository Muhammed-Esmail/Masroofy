const BASE = '/history';

function getCsrf() {
    const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
}

async function request(url, method = 'GET', body = null) {
    const opts = {
    method,
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
    };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(url, opts);
    const text = await res.text();
    try { return JSON.parse(text); } catch { return text; }
}

async function fetchFullHistory() {
    const data = await request(`${BASE}/full_history/`);
    const better = JSON.stringify(data, null, 2);
    let s = better.split('Transaction')

    document.getElementById('fullHistoryResult').textContent = s.join('\nTransaction');
}

async function fetchFiltered(e) {
    e.preventDefault();
    const params = new URLSearchParams();
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const categoryId = document.getElementById('categoryId').value;
    const cycleId = document.getElementById('cycleId').value;
    if (startDate) params.append('startDate', startDate);
    if (endDate) params.append('endDate', endDate);
    if (categoryId) params.append('category_id', categoryId);
    if (cycleId) params.append('cycle_id', cycleId);
    let data = await request(`${BASE}/filtered_history/?${params.toString()}`);
    if (!data) data = "Not Found";
    document.getElementById('filteredResult').textContent = JSON.stringify(data, null, 2);
}

async function fetchCycle(e) {
    e.preventDefault();
    const id = document.getElementById('cycleIdSingle').value;
    const params = new URLSearchParams();
    if (id) params.append('id', id);
    const data = await request(`${BASE}/fetch_cycle_data/?${params.toString()}`);
    document.getElementById('cycleResult').textContent = JSON.stringify(data, null, 2);
}

async function getActiveCycleId(e) {
    e.preventDefault();
    const data = await request(`${BASE}/get_active_cycle_id/`);
    document.getElementById('activeCycleId').textContent = JSON.stringify(data, null, 2);  
}

async function fetchTotalSpent(e) {
    e.preventDefault();
    const data = await request(`${BASE}/get_total_spent/`);
    document.getElementById('totalSpentResult').textContent = JSON.stringify(data, null, 2);
}