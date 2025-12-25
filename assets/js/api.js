// ═══════════════════════════════════════════════════════
// KRC GLOBAL API 통신 모듈
// ═══════════════════════════════════════════════════════

const API_BASE_URL = 'http://localhost:5000/api';

/**
 * API 요청 헬퍼
 * @param {string} endpoint - API 엔드포인트
 * @param {Object} options - fetch 옵션
 * @returns {Promise} API 응답
 */
async function apiRequest(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const config = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers,
        },
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API request error:', error);
        throw error;
    }
}

/**
 * GET 요청
 */
const api = {
    get(endpoint) {
        return apiRequest(endpoint, { method: 'GET' });
    },

    post(endpoint, data) {
        return apiRequest(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    put(endpoint, data) {
        return apiRequest(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    delete(endpoint) {
        return apiRequest(endpoint, { method: 'DELETE' });
    },
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { api, apiRequest };
}
