/**
 * GBMS - Authentication Module
 * 글로벌사업처 해외사업관리시스템
 */

const Auth = {
    // Storage keys
    TOKEN_KEY: 'gbms_token',
    USER_KEY: 'gbms_user',

    /**
     * Initialize login page
     */
    init() {
        this.bindEvents();
        this.checkExistingSession();
    },

    /**
     * Bind event listeners
     */
    bindEvents() {
        const loginForm = document.getElementById('loginForm');
        const togglePassword = document.getElementById('togglePassword');

        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }

        if (togglePassword) {
            togglePassword.addEventListener('click', () => this.togglePasswordVisibility());
        }
    },

    /**
     * Check if user is already logged in
     */
    checkExistingSession() {
        const token = Utils.storage.get(this.TOKEN_KEY);
        if (token && this.isTokenValid(token)) {
            // Redirect to dashboard
            window.location.href = 'dashboard.html';
        }
    },

    /**
     * Handle login form submission
     * @param {Event} e - Form submit event
     */
    async handleLogin(e) {
        e.preventDefault();

        const userId = document.getElementById('userId').value.trim();
        const password = document.getElementById('password').value;
        const rememberMe = document.getElementById('rememberMe').checked;

        // Validate inputs
        if (!userId || !password) {
            this.showError('아이디와 비밀번호를 모두 입력해주세요.');
            return;
        }

        // Show loading state
        this.setLoadingState(true);
        this.hideError();

        try {
            // Simulate API call (will be replaced with actual API)
            const response = await this.authenticateUser(userId, password);

            if (response.success) {
                // Store auth data
                Utils.storage.set(this.TOKEN_KEY, response.token);
                Utils.storage.set(this.USER_KEY, response.user);

                // Show success and redirect
                Utils.showToast('로그인 성공!', 'success');

                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 500);
            } else {
                this.showError(response.message || '로그인에 실패했습니다.');
            }
        } catch (error) {
            console.error('Login error:', error);
            this.showError('서버 연결에 실패했습니다. 잠시 후 다시 시도해주세요.');
        } finally {
            this.setLoadingState(false);
        }
    },

    /**
     * Authenticate user (mock - will be replaced with API)
     * @param {string} userId - User ID
     * @param {string} password - Password
     * @returns {Promise<Object>} Authentication result
     */
    async authenticateUser(userId, password) {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 800));

        // Mock users for development (will be replaced with actual API)
        const mockUsers = {
            'admin': {
                password: 'admin123',
                user: {
                    id: 1,
                    userId: 'admin',
                    name: '관리자',
                    department: 'gad',
                    departmentName: '글로벌농업개발부',
                    role: 'admin',
                    email: 'admin@krc.co.kr'
                }
            },
            'user1': {
                password: 'user123',
                user: {
                    id: 2,
                    userId: 'user1',
                    name: '홍길동',
                    department: 'gb',
                    departmentName: '글로벌사업부',
                    role: 'user',
                    email: 'hong@krc.co.kr'
                }
            },
            'user2': {
                password: 'user123',
                user: {
                    id: 3,
                    userId: 'user2',
                    name: '김철수',
                    department: 'aidc',
                    departmentName: '농식품국제개발협력센터',
                    role: 'user',
                    email: 'kim@krc.co.kr'
                }
            }
        };

        const userRecord = mockUsers[userId];

        if (userRecord && userRecord.password === password) {
            return {
                success: true,
                token: 'mock_token_' + Utils.generateId(),
                user: userRecord.user
            };
        }

        return {
            success: false,
            message: '아이디 또는 비밀번호가 올바르지 않습니다.'
        };
    },

    /**
     * Toggle password visibility
     */
    togglePasswordVisibility() {
        const passwordInput = document.getElementById('password');
        const eyeIcon = document.querySelector('.eye-icon');

        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            eyeIcon.textContent = '🙈';
        } else {
            passwordInput.type = 'password';
            eyeIcon.textContent = '👁';
        }
    },

    /**
     * Show error message
     * @param {string} message - Error message
     */
    showError(message) {
        const errorEl = document.getElementById('loginError');
        if (errorEl) {
            errorEl.querySelector('.alert-message').textContent = message;
            Utils.show(errorEl);
        }
    },

    /**
     * Hide error message
     */
    hideError() {
        const errorEl = document.getElementById('loginError');
        if (errorEl) {
            Utils.hide(errorEl);
        }
    },

    /**
     * Set loading state for login button
     * @param {boolean} isLoading - Loading state
     */
    setLoadingState(isLoading) {
        const btn = document.getElementById('loginBtn');
        const btnText = btn.querySelector('.btn-text');
        const btnLoading = btn.querySelector('.btn-loading');

        if (isLoading) {
            btn.disabled = true;
            Utils.hide(btnText);
            Utils.show(btnLoading);
        } else {
            btn.disabled = false;
            Utils.show(btnText);
            Utils.hide(btnLoading);
        }
    },

    /**
     * Check if token is valid (basic check)
     * @param {string} token - Auth token
     * @returns {boolean} Is valid
     */
    isTokenValid(token) {
        // In a real app, this would verify token expiration, etc.
        return token && token.length > 0;
    },

    /**
     * Get current user
     * @returns {Object|null} Current user object
     */
    getCurrentUser() {
        return Utils.storage.get(this.USER_KEY);
    },

    /**
     * Logout user
     */
    logout() {
        Utils.storage.remove(this.TOKEN_KEY);
        Utils.storage.remove(this.USER_KEY);
        window.location.href = 'index.html';
    },

    /**
     * Check if user is authenticated
     * @returns {boolean} Is authenticated
     */
    isAuthenticated() {
        const token = Utils.storage.get(this.TOKEN_KEY);
        return this.isTokenValid(token);
    },

    /**
     * Check if user has required role
     * @param {string|string[]} requiredRole - Required role(s)
     * @returns {boolean} Has role
     */
    hasRole(requiredRole) {
        const user = this.getCurrentUser();
        if (!user) return false;

        if (Array.isArray(requiredRole)) {
            return requiredRole.includes(user.role);
        }
        return user.role === requiredRole;
    },

    /**
     * Require authentication (redirect if not authenticated)
     */
    requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = 'index.html';
            return false;
        }
        return true;
    }
};

/**
 * Initialize login page
 */
function initLoginPage() {
    Auth.init();
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Auth;
}
