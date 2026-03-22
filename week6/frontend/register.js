document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("register-form");

  form.addEventListener("submit", function (event) {
    event.preventDefault(); // stop form from automatically submitting, required

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const emailError = document.getElementById("email-error");
    const passwordError = document.getElementById("password-error");
    const tosCheckbox = document.getElementById("tos-checkbox");

    // if tos not checked, alert user
    if (!tosCheckbox.checked) {
        alert("You must agree to the Terms of Service.");
        return;
    }

    // if name, email or password is empty, alert user
    if (name.trim() === "") {
        alert("Please enter your name.");
        return;
    } else if (email.trim() === "") {
        emailError.textContent = "Please enter your email.";
        return;
    } else if (password.trim() === "") {
        passwordError.textContent = "Please enter your password.";
        return;
    }

    const user = {"name":name, "email":email}
    sessionStorage.setItem("user", JSON.stringify(user))
    window.location.href = "welcome.html"
  });
});
