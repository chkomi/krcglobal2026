// ═══════════════════════════════════════════════════════
// KRC GLOBAL 공통 유틸리티 함수
// ═══════════════════════════════════════════════════════

/**
 * 날짜 포맷팅
 * @param {Date|string} date - 날짜 객체 또는 문자열
 * @param {string} format - 포맷 (기본: 'YYYY-MM-DD')
 * @returns {string} 포맷된 날짜 문자열
 */
function formatDate(date, format = 'YYYY-MM-DD') {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    const seconds = String(d.getSeconds()).padStart(2, '0');

    return format
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds);
}

/**
 * 숫자 포맷팅 (천 단위 구분)
 * @param {number} num - 숫자
 * @returns {string} 포맷된 숫자 문자열
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * 통화 포맷팅
 * @param {number} amount - 금액
 * @param {string} currency - 통화 기호 (기본: '₩')
 * @returns {string} 포맷된 통화 문자열
 */
function formatCurrency(amount, currency = '₩') {
    return `${currency}${formatNumber(amount)}`;
}

/**
 * 파일 크기 포맷팅
 * @param {number} bytes - 바이트 크기
 * @returns {string} 포맷된 파일 크기
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * 디바운스 함수
 * @param {Function} func - 실행할 함수
 * @param {number} wait - 대기 시간 (ms)
 * @returns {Function} 디바운스된 함수
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * 쿼리 파라미터 파싱
 * @returns {Object} 파라미터 객체
 */
function getQueryParams() {
    const params = {};
    const queryString = window.location.search.substring(1);
    const pairs = queryString.split('&');

    pairs.forEach(pair => {
        const [key, value] = pair.split('=');
        if (key) {
            params[decodeURIComponent(key)] = decodeURIComponent(value || '');
        }
    });

    return params;
}

/**
 * 로컬 스토리지 헬퍼
 */
const storage = {
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.error('Storage set error:', e);
            return false;
        }
    },

    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.error('Storage get error:', e);
            return defaultValue;
        }
    },

    remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (e) {
            console.error('Storage remove error:', e);
            return false;
        }
    },

    clear() {
        try {
            localStorage.clear();
            return true;
        } catch (e) {
            console.error('Storage clear error:', e);
            return false;
        }
    }
};

/**
 * 사용자 인증 확인
 * @returns {Object|null} 사용자 정보 또는 null
 */
function checkAuth() {
    const userInfo = storage.get('userInfo') || JSON.parse(sessionStorage.getItem('userInfo') || 'null');
    return userInfo;
}

/**
 * 로그아웃
 */
function logout() {
    storage.remove('userInfo');
    sessionStorage.removeItem('userInfo');
    window.location.href = 'index.html';
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatDate,
        formatNumber,
        formatCurrency,
        formatFileSize,
        debounce,
        getQueryParams,
        storage,
        checkAuth,
        logout
    };
}
