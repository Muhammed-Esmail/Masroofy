export class API {
    BASE = '';

    getCsrf() {
        const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
        return cookie ? cookie.split('=')[1] : '';
    }

    getBase() {
        return this.BASE;
    }

    setBase(base) {
        this.BASE = base
    }

    async request(url, method = 'GET', body = null) {
        
        const fullUrl = `${this.getBase()}${url}`;

        const opts = {
        method,
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': this.getCsrf() },
        };
        if (body) opts.body = JSON.stringify(body);
        const res = await fetch(fullUrl, opts);
        const text = await res.text();
        try { return JSON.parse(text); } catch { return text; }
    }
}
