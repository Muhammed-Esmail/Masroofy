export class API {
  BASE = "";

  getCsrf() {
    const cookie = document.cookie.split(";").find((c) => c.trim().startsWith("csrftoken="));
    return cookie ? cookie.split("=")[1] : "";
  }

  getBase() {
    return this.BASE;
  }

  setBase(base) {
    this.BASE = base;
  }

  async request(url, method = "GET", body = null) {
    const fullUrl = `${this.BASE}${url}`;

    const opts = {
      method,
      credentials: "include", // Enable sending/receiving cookies
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": this.getCsrf(),
      },
    };

    if (body) opts.body = JSON.stringify(body);

    try {
      const res = await fetch(fullUrl, opts);
      const text = await res.text();

      // Handle empty responses or non-JSON gracefully
      let data;
      try {
        data = text ? JSON.parse(text) : {};
      } catch {
        data = text;
      }

      return {
        ok: res.ok,
        status: res.status,
        data: data,
      };
    } catch (error) {
      console.error("Network/Fetch Error:", error);
      throw error;
    }
  }
}
