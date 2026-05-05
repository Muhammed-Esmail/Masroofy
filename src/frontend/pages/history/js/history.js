import { renderTransactions, renderCycle } from '/static/shared/js/render.js';
import { API } from '/static/api/API.js';

const historyAPI = new API();
historyAPI.setBase('/history');

const transactionAPI = new API();
transactionAPI.setBase('/transaction');

function openUpdateDialog(t) {
    document.getElementById('dialogTransactionId').textContent = t.id;
    document.getElementById('updateId').value = t.id;
    document.getElementById('updateAmount').value = t.amount;
    document.getElementById('updatecategoryName').value = t.category_name;
    document.getElementById('updateLogDate').value = t.log_date;
    document.getElementById('updateDescription').value = t.description || '';
    document.getElementById('updateNote').value = t.note || '';
    document.getElementById('updateDialog').showModal();
}

async function updateTransaction(e) {
    e.preventDefault();
    const form = document.getElementById('update-form');
    const data = Object.fromEntries(new FormData(form).entries());
    const response = await transactionAPI.request(`/update_transaction/`, 'POST', data);
    if (response.success) {
        alert('Transaction Updated');
        document.getElementById('updateDialog').close();
        fetchFullHistory();
    } else {
        alert('Update failed: ' + JSON.stringify(response));
    }
    if (response.state) {
        alert(response.state);
    }
}

async function deleteTransaction(id) {
    const response = await transactionAPI.request(`/delete_transaction/${id}/`, 'DELETE');
    if (response.success) alert('Transaction Deleted');
    if (response.state) {
        alert(response.state);
    }
    fetchFullHistory();
}

let transactionCache = {};

function onListClick(e) {
    const id = Number(e.target.dataset.id);
    if (!id) return;
    if (e.target.classList.contains('btn-update')) openUpdateDialog(transactionCache[id]);
    if (e.target.classList.contains('btn-delete')) deleteTransaction(id);
}

async function fetchFullHistory() {
    const data = await historyAPI.request(`/full_history/`, 'GET');
    data.forEach(t => transactionCache[t.id] = t);
    renderTransactions(data, document.getElementById('fullHistoryResult'));
}

async function fetchFiltered(e) {
    e.preventDefault();
    const params = new URLSearchParams();
    const startDate    = document.getElementById('startDate').value;
    const endDate      = document.getElementById('endDate').value;
    const categoryName = document.getElementById('categoryName').value;
    const cycleId      = document.getElementById('cycleId').value;
    if (startDate)     params.append('startDate', startDate);
    if (endDate)       params.append('endDate', endDate);
    if (categoryName)  params.append('category_name', categoryName);
    console.log(`[${categoryName}]`);
    if (cycleId)       params.append('cycle_id', cycleId);
    const data = await historyAPI.request(`/filtered_history/?${params}`);
    const list = data || [];
    list.forEach(t => transactionCache[t.id] = t);
    renderTransactions(list, document.getElementById('filteredResult'));
}

async function fetchCycle(e) {
    e.preventDefault();
    const id = document.getElementById('cycleIdSingle').value;
    const params = new URLSearchParams();
    if (id) params.append('id', id);
    const data = await historyAPI.request(`/fetch_cycle_data/?${params}`);
    renderCycle(data, document.getElementById('cycleResult'));
}

async function getActiveCycleId() {
    const data = await historyAPI.request(`/get_active_cycle_id/`);
    document.getElementById('activeCycleId').textContent = JSON.stringify(data, null, 2);
}

async function fetchTotalSpent() {
    const data = await historyAPI.request(`/get_total_spent/`);
    document.getElementById('totalSpentResult').textContent = JSON.stringify(data, null, 2);
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('btn-full-history').addEventListener('click', fetchFullHistory);
    document.getElementById('form-filtered').addEventListener('submit', fetchFiltered);
    document.getElementById('form-fetch-cycle').addEventListener('submit', fetchCycle);
    document.getElementById('btn-active-cycle-id').addEventListener('click', getActiveCycleId);
    document.getElementById('btn-total-spent').addEventListener('click', fetchTotalSpent);
    document.getElementById('fullHistoryResult').addEventListener('click', onListClick);
    document.getElementById('filteredResult').addEventListener('click', onListClick);
    document.getElementById('update-form').addEventListener('submit', updateTransaction);
    document.getElementById('btn-cancel-update').addEventListener('click', () => document.getElementById('updateDialog').close());
});