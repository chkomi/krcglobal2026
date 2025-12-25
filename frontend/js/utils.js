/**
 * GBMS - Utility Functions
 * 글로벌사업처 해외사업관리시스템
 */

const Utils = {
    /**
     * Format date to Korean style (YYYY년 MM월 DD일)
     * @param {Date|string} date - Date object or date string
     * @returns {string} Formatted date string
     */
    formatDate(date, format = 'default') {
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        
        switch(format) {
            case 'korean':
                return `${year}년 ${month}월 ${day}일`;
            case 'short':
                return `${year}.${month}.${day}`;
            case 'iso':
                return `${year}-${month}-${day}`;
            default:
                return `${year}-${month}-${day}`;
        }
    },

    /**
     * Format number with commas (Korean currency style)
     * @param {number} num - Number to format
     * @returns {string} Formatted number string
     */
    formatNumber(num) {
        if (num === null || num === undefined) return '0';
        return Number(num).toLocaleString('ko-KR');
    },

    /**
     * Format currency (원)
     * @param {number} amount - Amount to format
     * @returns {string} Formatted currency string
     */
    formatCurrency(amount) {
        return this.formatNumber(amount) + '원';
    },

    /**
     * Format large currency (억원)
     * @param {number} amount - Amount in 원
     * @returns {string} Formatted as 억원
     */
    formatLargeCurrency(amount) {
        const billionWon = amount / 100000000;
        if (billionWon >= 1) {
            return billionWon.toFixed(1) + '억원';
        }
        const tenThousandWon = amount / 10000;
        return this.formatNumber(tenThousandWon) + '만원';
    },

    /**
     * Calculate percentage
     * @param {number} value - Current value
     * @param {number} total - Total value
     * @returns {number} Percentage (0-100)
     */
    calculatePercentage(value, total) {
        if (total === 0) return 0;
        return Math.round((value / total) * 100);
    },

    /**
     * Debounce function
     * @param {Function} func - Function to debounce
     * @param {number} wait - Wait time in ms
     * @returns {Function} Debounced function
     */
    debounce(func, wait = 300) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Generate unique ID
     * @returns {string} Unique ID
     */
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    },

    /**
     * Show toast notification
     * @param {string} message - Message to display
     * @param {string} type - Type: success, error, warning, info
     * @param {number} duration - Duration in ms
     */
    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <span class="toast-icon">${this.getToastIcon(type)}</span>
            <span class="toast-message">${message}</span>
        `;
        
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        
        container.appendChild(toast);
        
        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 10);
        
        // Remove after duration
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    },

    getToastIcon(type) {
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };
        return icons[type] || icons.info;
    },

    /**
     * Local storage helper with JSON support
     */
    storage: {
        get(key) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : null;
            } catch (e) {
                console.error('Storage get error:', e);
                return null;
            }
        },
        
        set(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
                return true;
            } catch (e) {
                console.error('Storage set error:', e);
                return false;
            }
        },
        
        remove(key) {
            localStorage.removeItem(key);
        },
        
        clear() {
            localStorage.clear();
        }
    },

    /**
     * Show/hide element
     */
    show(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        if (element) {
            element.classList.remove('hidden');
        }
    },

    hide(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        if (element) {
            element.classList.add('hidden');
        }
    },

    /**
     * Validate form data
     * @param {Object} data - Form data object
     * @param {Object} rules - Validation rules
     * @returns {Object} { isValid: boolean, errors: Object }
     */
    validateForm(data, rules) {
        const errors = {};
        
        for (const field in rules) {
            const value = data[field];
            const fieldRules = rules[field];
            
            if (fieldRules.required && !value) {
                errors[field] = fieldRules.message || `${field}은(는) 필수 입력 항목입니다.`;
            } else if (fieldRules.minLength && value && value.length < fieldRules.minLength) {
                errors[field] = `최소 ${fieldRules.minLength}자 이상 입력해주세요.`;
            } else if (fieldRules.maxLength && value && value.length > fieldRules.maxLength) {
                errors[field] = `최대 ${fieldRules.maxLength}자까지 입력 가능합니다.`;
            } else if (fieldRules.pattern && value && !fieldRules.pattern.test(value)) {
                errors[field] = fieldRules.message || '올바른 형식이 아닙니다.';
            }
        }
        
        return {
            isValid: Object.keys(errors).length === 0,
            errors
        };
    },

    /**
     * Get project status badge
     * @param {string} status - Status code
     * @returns {Object} { class, label }
     */
    getStatusBadge(status) {
        const statusMap = {
            'planning': { class: 'badge-info', label: '기획' },
            'in_progress': { class: 'badge-primary', label: '진행중' },
            'completed': { class: 'badge-success', label: '완료' },
            'suspended': { class: 'badge-warning', label: '보류' },
            'cancelled': { class: 'badge-danger', label: '취소' }
        };
        return statusMap[status] || { class: 'badge-secondary', label: status };
    },

    /**
     * Get project type label
     * @param {string} type - Project type code
     * @returns {string} Label
     */
    getProjectTypeLabel(type) {
        const typeMap = {
            'consulting': '해외기술용역',
            'oda_bilateral': 'ODA 양자',
            'oda_multilateral': 'ODA 다자성양자',
            'k_rice_belt': 'K-라이스벨트',
            'investment': '해외농업투자',
            'loan_support': '융자·보조사업'
        };
        return typeMap[type] || type;
    },

    /**
     * Get department label
     * @param {string} code - Department code
     * @returns {string} Label
     */
    getDepartmentLabel(code) {
        const deptMap = {
            'gad': '글로벌농업개발부',
            'gb': '글로벌사업부',
            'aidc': '농식품국제개발협력센터'
        };
        return deptMap[code] || code;
    }
};

// Toast container styles (injected dynamically)
const toastStyles = document.createElement('style');
toastStyles.textContent = `
    .toast-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    
    .toast {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 20px;
        border-radius: 8px;
        background: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transform: translateX(120%);
        transition: transform 0.3s ease;
        font-size: 14px;
    }
    
    .toast.show {
        transform: translateX(0);
    }
    
    .toast-success { border-left: 4px solid #28a745; }
    .toast-error { border-left: 4px solid #dc3545; }
    .toast-warning { border-left: 4px solid #ffc107; }
    .toast-info { border-left: 4px solid #17a2b8; }
    
    .toast-icon {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        color: white;
    }
    
    .toast-success .toast-icon { background: #28a745; }
    .toast-error .toast-icon { background: #dc3545; }
    .toast-warning .toast-icon { background: #ffc107; color: #333; }
    .toast-info .toast-icon { background: #17a2b8; }
`;
document.head.appendChild(toastStyles);

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Utils;
}
