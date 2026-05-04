(function () {
  const form = document.getElementById("auth");
  const auth = new AuthService();
  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const Email = form.querySelector('input[name="Email"]');
    const Password = form.querySelector('input[name="password"]');
    const UserName = form.querySelector('input[name="userName"]');
    if (!Email || !Password) {
      console.error("Email or password input not found.");
      return;
    }
    const email = Email.value.trim();
    const password = Password.value;
    const userName = UserName ? UserName.value.trim() : null;
    const submitBtn = form.querySelector('[type="submit"]');
    try {
      const result = await auth.authUser(email, userName, password);
      if (result.status === "success") {
        window.location.href = "/dashboard/";
      } else {
        alert(result.message || "Please try again.");
      }
    } catch (err) {
      console.error("unexpected error –", err);
      alert("Please try again later.");
    }
  });
})();
