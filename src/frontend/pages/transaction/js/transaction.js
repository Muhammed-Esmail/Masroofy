import { API } from '/static/api/API.js';

const api = new API();
api.setBase('/transaction');

async function logTransaction(e) {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
    const response = await api.request('/log_transaction/', 'POST', data);
    if (response.success) {
        alert('Transaction logged!');
    } else {
        alert('Failed: ' + JSON.stringify(response));
    }

    if (response.state) {
        alert(response.state);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('create-form').addEventListener('submit', logTransaction);
});