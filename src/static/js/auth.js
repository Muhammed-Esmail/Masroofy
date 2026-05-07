class AuthService {
  constructor() {
    this.api = new API();
    this.api.setBase("http://127.0.0.1:8000/api");
  }
  async authUser(Email, userName = null, password) {
    try {
      const data = await this.api.request("/auth/", "POST", { email: Email, username: userName, password: password });
      console.log("data:", data);

      if (data.token) {
        this.api.setToken(data.token);
      }
      if (response.ok) {
        return { status: "success", data: data };
      } else {
        return { status: "error", message: data.message, errors: data.errors || [] };
      }
    } catch (error) {
      console.error("CATCH ERROR:", error);
      return { status: "error", message: "unknown error", errors: [] };
    }
  }
  async verifySession() {
    try {
      const response = await fetch(`${this.baseUrl}/verify/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        return { status: "success", data: await response.json() };
      } else {
        return { status: "error", message: "No active session" };
      }
    } catch (error) {
      return { status: "error", message: "Network error" };
    }
  }
  getCsrfToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, 10) === "csrftoken=") {
          cookieValue = decodeURIComponent(cookie.substring(10));
          break;
        }
      }
    }
    return cookieValue;
  }
}
