/**
 * GBMS - API Module
 * 글로벌사업처 해외사업관리시스템
 * 
 * API communication layer for Flask backend
 */

const API = {
    // Base URL for API
    // 개발 환경: Live Server(5500) 사용 시 Flask 서버(5001)로 요청 전달
    get BASE_URL() {
        // 현재 포트가 5500이면 Flask 서버(5001)로 요청
        if (window.location.port === '5500' || window.location.port === '') {
            return 'http://127.0.0.1:5001/api';
        }
        // Flask 서버와 같은 포트에서 실행되는 경우
        return '/api';
    },

    /**
     * Make API request
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Fetch options
     * @returns {Promise<Object>} Response data
     */
    async request(endpoint, options = {}) {
        const url = `${this.BASE_URL}${endpoint}`;

        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        // Add auth token if available
        const token = Utils.storage.get('gbms_token');
        if (token) {
            defaultOptions.headers['Authorization'] = `Bearer ${token}`;
        }

        const mergedOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers,
            },
        };

        try {
            const response = await fetch(url, mergedOptions);

            // Handle 401 Unauthorized
            if (response.status === 401) {
                Auth.logout();
                throw new Error('인증이 만료되었습니다. 다시 로그인해주세요.');
            }

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || '요청 처리 중 오류가 발생했습니다.');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    /**
     * GET request
     */
    async get(endpoint, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const url = queryString ? `${endpoint}?${queryString}` : endpoint;
        return this.request(url, { method: 'GET' });
    },

    /**
     * POST request
     */
    async post(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    /**
     * PUT request
     */
    async put(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    /**
     * DELETE request
     */
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    },

    /**
     * Upload file
     */
    async upload(endpoint, formData) {
        const token = Utils.storage.get('gbms_token');
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${this.BASE_URL}${endpoint}`, {
            method: 'POST',
            headers,
            body: formData,
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || '파일 업로드 중 오류가 발생했습니다.');
        }

        return response.json();
    },

    // ==========================================
    // Projects API
    // ==========================================
    projects: {
        /**
         * Get all projects with optional filters
         */
        async list(filters = {}) {
            return API.get('/projects', filters);
        },

        /**
         * Get single project by ID
         */
        async get(id) {
            return API.get(`/projects/${id}`);
        },

        /**
         * Create new project
         */
        async create(data) {
            return API.post('/projects', data);
        },

        /**
         * Update project
         */
        async update(id, data) {
            return API.put(`/projects/${id}`, data);
        },

        /**
         * Delete project
         */
        async delete(id) {
            return API.delete(`/projects/${id}`);
        },

        /**
         * Get project statistics
         */
        async getStats() {
            return API.get('/projects/stats');
        },

        /**
         * Get projects by type
         */
        async getByType(type) {
            return API.get('/projects', { type });
        },

        /**
         * Get projects by department
         */
        async getByDepartment(deptCode) {
            return API.get('/projects', { department: deptCode });
        }
    },

    // ==========================================
    // Budget API
    // ==========================================
    budgets: {
        async list(projectId = null) {
            const params = projectId ? { project_id: projectId } : {};
            return API.get('/budgets', params);
        },

        async get(id) {
            return API.get(`/budgets/${id}`);
        },

        async create(data) {
            return API.post('/budgets', data);
        },

        async update(id, data) {
            return API.put(`/budgets/${id}`, data);
        },

        async addExecution(budgetId, data) {
            return API.post(`/budgets/${budgetId}/executions`, data);
        },

        async getStats(year = null) {
            const params = year ? { year } : {};
            return API.get('/budgets/stats', params);
        }
    },

    // ==========================================
    // Documents API
    // ==========================================
    documents: {
        async list(filters = {}) {
            return API.get('/documents', filters);
        },

        async get(id) {
            return API.get(`/documents/${id}`);
        },

        async upload(formData) {
            return API.upload('/documents/upload', formData);
        },

        async delete(id) {
            return API.delete(`/documents/${id}`);
        },

        async download(id) {
            // Return download URL
            return `${API.BASE_URL}/documents/${id}/download`;
        }
    },

    // ==========================================
    // Offices API
    // ==========================================
    offices: {
        async list() {
            return API.get('/offices');
        },

        async get(id) {
            return API.get(`/offices/${id}`);
        },

        async create(data) {
            return API.post('/offices', data);
        },

        async update(id, data) {
            return API.put(`/offices/${id}`, data);
        }
    },

    // ==========================================
    // Users API
    // ==========================================
    users: {
        async list() {
            return API.get('/users');
        },

        async get(id) {
            return API.get(`/users/${id}`);
        },

        async create(data) {
            return API.post('/users', data);
        },

        async update(id, data) {
            return API.put(`/users/${id}`, data);
        },

        async updatePassword(id, data) {
            return API.put(`/users/${id}/password`, data);
        }
    },

    // ==========================================
    // Dashboard API
    // ==========================================
    dashboard: {
        async getOverview() {
            return API.get('/dashboard/overview');
        },

        async getRecentProjects(limit = 5) {
            return API.get('/dashboard/recent-projects', { limit });
        },

        async getUpcomingEvents(limit = 5) {
            return API.get('/dashboard/upcoming-events', { limit });
        }
    },

    // ==========================================
    // GIS API
    // ==========================================
    gis: {
        /**
         * Get all projects with GIS data
         */
        async getProjects(filters = {}) {
            return API.get('/gis/projects', filters);
        },

        /**
         * Get GIS statistics
         */
        async getStats() {
            return API.get('/gis/stats');
        },

        /**
         * Update project location
         */
        async updateLocation(projectId, latitude, longitude) {
            return API.put(`/gis/projects/${projectId}/location`, {
                latitude,
                longitude
            });
        }
    }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API;
}
