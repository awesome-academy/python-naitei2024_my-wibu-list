// scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const inputs = document.querySelectorAll('input');
    
    form.addEventListener('submit', function(event) {
        let isValid = true;
        
        inputs.forEach(input => {
            if (input.type !== "submit" && input.value.trim() === "") {
                isValid = false;
                input.classList.add('error');
                showError(input, 'This field is required.');
            } else {
                input.classList.remove('error');
                hideError(input);
            }
        });

        if (!isValid) {
            event.preventDefault(); // Ngăn chặn gửi form nếu có lỗi
        }
    });

    function showError(input, message) {
        let error = input.nextElementSibling;
        if (!error || !error.classList.contains('error-message')) {
            error = document.createElement('div');
            error.classList.add('error-message');
            input.parentNode.insertBefore(error, input.nextSibling);
        }
        error.textContent = message;
    }

    function hideError(input) {
        let error = input.nextElementSibling;
        if (error && error.classList.contains('error-message')) {
            error.remove();
        }
    }
});
document.addEventListener('DOMContentLoaded', () => {
    const loginButton = document.getElementById('loginButton');
    const registerButton = document.getElementById('registerButton');
    const formContainer = document.getElementById('formContainer');
    const loginFormContainer = document.getElementById('loginFormContainer');
    const registerFormContainer = document.getElementById('registerFormContainer');
    const closeLoginForm = document.getElementById('closeLoginForm');
    const closeRegisterForm = document.getElementById('closeRegisterForm');

    loginButton.addEventListener('click', () => {
        formContainer.style.display = 'block';
        loginFormContainer.style.display = 'block';
        registerFormContainer.style.display = 'none';
    });

    registerButton.addEventListener('click', () => {
        formContainer.style.display = 'block';
        loginFormContainer.style.display = 'none';
        registerFormContainer.style.display = 'block';
    });

    closeLoginForm.addEventListener('click', () => {
        formContainer.style.display = 'none';
    });

    closeRegisterForm.addEventListener('click', () => {
        formContainer.style.display = 'none';
    });
});

