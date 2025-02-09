document.addEventListener("DOMContentLoaded", () => {
    const passwordInput = document.getElementById("password");
    const passwordToggle = document.querySelector(".password-toggle");

    passwordToggle.addEventListener("click", () => {
        const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
        passwordInput.setAttribute("type", type);
        passwordToggle.classList.toggle("fa-eye");
        passwordToggle.classList.toggle("fa-eye-slash");
    });

    const form = document.getElementById("signinForm");
    const submitBtn = form.querySelector(".submit-btn");
    const submitBtnText = submitBtn.querySelector("span");
    const submitBtnIcon = submitBtn.querySelector("i");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        submitBtn.disabled = true;
        submitBtnText.textContent = "Signing in...";
        submitBtnIcon.className = "fas fa-spinner fa-spin";

        const formData = {
            email: form.email.value,
            password: form.password.value,
            remember: form.remember.checked
        };

        try {
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            console.log("Form submitted:", formData);
            
            alert("Sign in successful!");
            
        } catch (error) {
            alert("An error occurred. Please try again.");
        } finally {
            submitBtnText.textContent = "Sign In";
            submitBtnIcon.className = "fas fa-arrow-right";
            submitBtn.disabled = false;
        }
    });

    const inputs = document.querySelectorAll("input");

    inputs.forEach(input => {
        input.addEventListener("focus", () => {
            input.parentElement.classList.add("focused");
        });

        input.addEventListener("blur", () => {
            if (!input.value) {
                input.parentElement.classList.remove("focused");
            }
        });
    });
});