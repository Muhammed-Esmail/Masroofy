import { API } from "/static/api/API.js";

export class AuthService extends API {
  constructor() {
    super()
    this.setBase("/api");
  }

  async authUser(email, username = null, password) {
    try {
        const response = await this.request('/auth/', 'POST', { 
            email: email, 
            username: username, 
            password: password 
        });

        if (response.ok) {
            window.location.reload();
            return { status: "success", data: response.data };
        } else {
            return { 
                status: "error", 
                message: response.data.message || "Authentication failed", 
                errors: response.data.errors || [] 
            };
        }
    } catch (error) {
        return { status: "error", message: "Network connection failed\n" + response };
    }
  }

  async verifySession() {
      try {
          const response = await this.request('/verify/', 'GET');

          if (response.ok) {
              return { status: "success", data: response.data };
          } else {
              return { status: "error", message: "No active session" };
          }
      } catch (error) {
          return { status: "error", message: "Network error" };
      }
  }
}
