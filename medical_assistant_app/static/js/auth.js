document.addEventListener('DOMContentLoaded', () => {
    const loginContainer = document.getElementById('login-container');
    const signupContainer = document.getElementById('signup-container');
    const showSignupLink = document.getElementById('show-signup');
    const showLoginLink = document.getElementById('show-login');
    const loadingOverlay = document.getElementById('loading-overlay');

    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');

    const loginError = document.getElementById('login-error');
    const signupError = document.getElementById('signup-error');

    // Toggle forms
    showSignupLink.addEventListener('click', (e) => {
        e.preventDefault();
        loginContainer.classList.add('hidden');
        signupContainer.classList.remove('hidden');
    });

    showLoginLink.addEventListener('click', (e) => {
        e.preventDefault();
        signupContainer.classList.add('hidden');
        loginContainer.classList.remove('hidden');
    });

    // --- Form Submission Logic ---
    const showLoading = (show) => {
        loadingOverlay.classList.toggle('hidden', !show);
    };

    const handleFormSubmit = async (url, body, errorElement) => {
        showLoading(true);
        errorElement.textContent = '';
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify(body),
            });
            const data = await response.json();

            if (response.ok && data.success) {
                window.location.href = '/chat/'; // Redirect to chat page on success
            } else {
                errorElement.textContent = data.error || 'An unknown error occurred.';
            }
        } catch (error) {
            console.error('API Error:', error);
            errorElement.textContent = 'Could not connect to the server.';
        } finally {
            showLoading(false);
        }
    };

    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        handleFormSubmit('/api/login/', { email, password }, loginError);
    });

    signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('signup-name').value;
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;
        handleFormSubmit('/api/signup/', { name, email, password }, signupError);
    });
});