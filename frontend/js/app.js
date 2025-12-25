/**
 * GBMS - Main Application
 * 글로벌사업처 해외사업관리시스템
 */

const App = {
    /**
     * Initialize application
     */
    init() {
        // Check authentication
        if (!Auth.requireAuth()) {
            return;
        }

        // Setup user info
        this.setupUserInfo();

        // Bind events
        this.bindEvents();

        // Load dashboard data
        this.loadDashboardData();

        console.log('GBMS Application initialized');
    },

    /**
     * Setup user info in header
     */
    setupUserInfo() {
        const user = Auth.getCurrentUser();
        if (user) {
            const userName = document.getElementById('userName');
            const userDept = document.getElementById('userDept');
            const userAvatar = document.getElementById('userAvatar');
            const welcomeName = document.getElementById('welcomeName');

            if (userName) userName.textContent = user.name;
            if (userDept) userDept.textContent = user.departmentName;
            if (userAvatar) userAvatar.textContent = user.name.charAt(0);
            if (welcomeName) welcomeName.textContent = user.name;
        }
    },

    /**
     * Bind event listeners
     */
    bindEvents() {
        // Sidebar toggle
        const sidebarToggle = document.getElementById('sidebarToggle');
        const headerToggle = document.getElementById('headerToggle');
        const sidebar = document.getElementById('sidebar');

        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', () => {
                sidebar.classList.toggle('collapsed');
                this.saveSidebarState(sidebar.classList.contains('collapsed'));
            });
        }

        if (headerToggle) {
            headerToggle.addEventListener('click', () => {
                sidebar.classList.toggle('collapsed');
                this.saveSidebarState(sidebar.classList.contains('collapsed'));
            });
        }

        // Restore sidebar state
        this.restoreSidebarState();

        // Logout button
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                Auth.logout();
            });
        }

        // Dropdowns
        this.initDropdowns();

        // Active nav item
        this.setActiveNavItem();
    },

    /**
     * Initialize dropdown menus
     */
    initDropdowns() {
        const dropdowns = document.querySelectorAll('.dropdown');

        dropdowns.forEach(dropdown => {
            const trigger = dropdown.querySelector('.btn, .header-user');

            if (trigger) {
                trigger.addEventListener('click', (e) => {
                    e.stopPropagation();

                    // Close other dropdowns
                    dropdowns.forEach(d => {
                        if (d !== dropdown) d.classList.remove('active');
                    });

                    dropdown.classList.toggle('active');
                });
            }
        });

        // Close on outside click
        document.addEventListener('click', () => {
            dropdowns.forEach(d => d.classList.remove('active'));
        });
    },

    /**
     * Set active navigation item based on current URL
     */
    setActiveNavItem() {
        const currentPath = window.location.pathname;
        const navItems = document.querySelectorAll('.nav-item');

        navItems.forEach(item => {
            item.classList.remove('active');
            const href = item.getAttribute('href');
            if (href && currentPath.includes(href.replace('.html', ''))) {
                item.classList.add('active');
            }
        });
    },

    /**
     * Save sidebar state to localStorage
     */
    saveSidebarState(collapsed) {
        Utils.storage.set('sidebar_collapsed', collapsed);
    },

    /**
     * Restore sidebar state from localStorage
     */
    restoreSidebarState() {
        const collapsed = Utils.storage.get('sidebar_collapsed');
        const sidebar = document.getElementById('sidebar');

        if (collapsed && sidebar) {
            sidebar.classList.add('collapsed');
        }
    },

    /**
     * Load dashboard data
     */
    async loadDashboardData() {
        try {
            // For now, use mock data since backend isn't ready
            // In production, replace with API calls:
            // const overview = await API.dashboard.getOverview();

            this.renderDashboardStats();
        } catch (error) {
            console.error('Error loading dashboard data:', error);
        }
    },

    /**
     * Render dashboard statistics (mock data for now)
     */
    renderDashboardStats() {
        // This will be replaced with actual API data
        const stats = {
            totalProjects: 32,
            totalBudget: '1,245억',
            totalCountries: 18,
            totalOffices: 6
        };

        // Update stat values if elements exist
        const elements = {
            totalProjects: document.getElementById('totalProjects'),
            totalBudget: document.getElementById('totalBudget'),
            totalCountries: document.getElementById('totalCountries'),
            totalOffices: document.getElementById('totalOffices')
        };

        for (const [key, el] of Object.entries(elements)) {
            if (el && stats[key]) {
                el.textContent = stats[key];
            }
        }
    },

    /**
     * Navigate to page
     */
    navigateTo(url) {
        window.location.href = url;
    },

    /**
     * Show confirmation dialog
     */
    confirm(message, onConfirm, onCancel) {
        const result = window.confirm(message);
        if (result && onConfirm) {
            onConfirm();
        } else if (!result && onCancel) {
            onCancel();
        }
        return result;
    },

    /**
     * Format table data
     */
    formatTableData(data, columns) {
        return data.map(item => {
            const row = {};
            columns.forEach(col => {
                if (col.formatter) {
                    row[col.key] = col.formatter(item[col.key], item);
                } else {
                    row[col.key] = item[col.key];
                }
            });
            return row;
        });
    }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = App;
}
