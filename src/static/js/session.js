(function () {
  const login = "/login/";
  if (window.location.pathname === login) return;
  async function checkSession() {
    try {
      const auth = new AuthService();
      const result = await auth.verifySession();
      if (result.status !== "success") {
        alert("session invalid");
        window.location.href = login;
      }
    } catch (err) {
      console.error("unexpected error", err);
      window.location.href = login;
    }
  }
  checkSession();
})();
