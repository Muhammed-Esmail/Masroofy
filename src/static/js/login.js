import { AuthService } from "./auth.js";

(function () {
  console.log("LOGIN JS LOADED");
  const form = document.getElementById("auth");
  console.log("form element:", form);
  const auth = new AuthService();

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const Email = form.querySelector('input[name="Email"]');
    const Password = form.querySelector('input[name="password"]');
    const UserName = form.querySelector('input[name="userName"]');
    const email = Email.value.trim();
    const password = Password.value;
    const userName = UserName ? UserName.value.trim() : null;

    const result = await auth.authUser(email, userName, password);

    if (result.status === "success") {
      window.location.href = "dashboard/";
    } else {
      if (result.errors && result.errors.length > 0) {
        alert(result.errors.join("\n"));
      } else {
        alert(result.message || "Something went wrong.");
      }
    }
  });
})();
