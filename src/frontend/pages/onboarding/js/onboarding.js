import '/static/api/API.js';

class FinanceService extends API {
    constructor(base) {
        super()
        this.setBase(base)
    }
}

const financeService = new FinanceService('/cycle');

