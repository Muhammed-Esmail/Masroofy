import API from '/static/api/API.js';

class FinanceService extends API {
    constructor(base) {
        super()
        this.setBase(base)
    }
}

const financeService = new FinanceService('/cycle');

async function createCycle(event) {
    event.preventDefault();
    const form = event.target.closest('form');
    const formData = new FormData(form);
    const body = Object.fromEntries(formData.entries());
    
    const message = await financeService.request('/start_cycle/', 'POST', body);

    if(message.success == false) {
        alert(message.description);
        return;
    }

    window.location.replace(message.data);
}

document.getElementById('start-btn').addEventListener('click', createCycle);