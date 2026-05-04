import '/static/api/API.js';

class HistoryService extends API {
    constructor(base) {
        super()
        this.setBase(base)
    }
}

const historyService = new HistoryService('/history');

async function fetchFullHistory() {
    const data = await historyService.request(`/full_history/`);
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
    let data = await historyService.request(`/filtered_history/?${params.toString()}`);
    if (!data) data = "Not Found";
    document.getElementById('filteredResult').textContent = JSON.stringify(data, null, 2);
}

async function fetchCycle(e) {
    e.preventDefault();
    const id = document.getElementById('cycleIdSingle').value;
    const params = new URLSearchParams();
    if (id) params.append('id', id);
    const data = await historyService.request(`/fetch_cycle_data/?${params.toString()}`);
    document.getElementById('cycleResult').textContent = JSON.stringify(data, null, 2);
}

async function getActiveCycleId(e) {
    e.preventDefault();
    const data = await historyService.request(`/get_active_cycle_id/`);
    document.getElementById('activeCycleId').textContent = JSON.stringify(data, null, 2);  
}

async function fetchTotalSpent(e) {
    e.preventDefault();
    const data = await historyService.request(`${BASE}/get_total_spent/`);
    document.getElementById('totalSpentResult').textContent = JSON.stringify(data, null, 2);
}