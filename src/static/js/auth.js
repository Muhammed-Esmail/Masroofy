import { API } from "/static/api/API.js";

export class AuthService extends API {
  constructor() {
    super();
    this.setBase("/api");
  }

  async authUser(email, username = null, password) {
    try {
      const response = await this.request("/auth/", "POST", {
        email: email,
        username: username,
        password: password,
      });
      
      if (response.success) {
        window.location.reload();
        return { status: "success", description: response.data };
      } else {
        return {
          status: "error",
          description: response.description || "Authentication failed",
        };
      }
    } catch (error) {
      return { status: "error", description: "Network connection failed\n" + response };
    }
  }
}
