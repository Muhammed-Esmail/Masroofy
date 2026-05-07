export function renderTransactions(transactions, listEl) {
    listEl.innerHTML = '';

    if (!Array.isArray(transactions) || transactions.length === 0) {
        listEl.innerHTML = '<li>No transactions found.</li>';
        return;
    }

    transactions.forEach(t => {
        const li = document.createElement('li');
        li.id = `transaction-${t.id}`;
        li.innerHTML = `
            <strong>Transaction #${t.id}</strong><br>
            Amount: <b>${t.amount}</b> &nbsp;|&nbsp;
            Date: ${t.log_date} &nbsp;|&nbsp;
            Cycle ID: ${t.cycle_id} &nbsp;|&nbsp;
            Category Name: ${t.category_name}<br>
            Description: ${t.description || '—'}<br>
            Note: ${t.note || '—'}<br>
            <button data-id="${t.id}" class="btn-update">Update</button>
            <button data-id="${t.id}" class="btn-delete">Delete</button>
            <hr>
        `;
        listEl.appendChild(li);
    });
}

export function renderCycle(cycle, el) {
    if (!cycle || cycle.error) {
        el.innerHTML = '<p>No cycle found.</p>';
        return;
    }

    el.innerHTML = `
        <strong>Cycle #${cycle.id}</strong><br>
        Start Date: ${cycle.startDate} &nbsp;|&nbsp;
        End Date: ${cycle.endDate}<br>
        Budget: <b>${cycle.amount}</b>
    `;
}