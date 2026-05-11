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
            <div class="t-info">
                <div class="t-desc">${t.description || '—'}</div>
                <div class="t-meta">
                    #${t.id} &nbsp;·&nbsp; ${t.log_date} &nbsp;·&nbsp; Cycle ${t.cycle_id}
                    &nbsp;·&nbsp; ${t.note ? t.note : ''}
                </div>
            </div>
            <span class="t-badge">${t.category_name}</span>
            <span class="t-amount">${t.amount}</span>
            <div class="t-actions">
                <button data-id="${t.id}" class="btn-update">Update</button>
                <button data-id="${t.id}" class="btn-delete">Delete</button>
            </div>
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