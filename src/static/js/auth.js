class AuthService {
  constructor() {
    this.baseUrl = "http://127.0.0.1:8000/api";
  }
  async authUser(Email, userName = null, password) {
    try {
      const response = await fetch(`${this.baseUrl}/auth/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": this.getCsrfToken(),
        },
        body: JSON.stringify({ email: Email, username: userName, password: password }),
      });
      const data = await response.json();
      if (response.ok) {
        return { status: "success", data: data };
      } else {
        return { status: "error", message: "Failed to auth the user" };
      }
    } catch (error) {
      console.error("error", error);
      return { status: "error", message: "unkown error" };
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
