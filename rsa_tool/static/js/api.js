// rsa_tool/static/js/api.js
/**
 * API Service - Handle all API calls
 */

const API = {
    baseURL: '/api',
    
    /**
     * Generic request handler
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    /**
     * Key Generation API
     */
    async generateKey(bits = 1024, e = 65537) {
        return this.request('/key/generate', {
            method: 'POST',
            body: JSON.stringify({ bits, e })
        });
    },
    
    /**
     * Encryption API
     */
    async encrypt(message, e, n) {
        return this.request('/crypto/encrypt', {
            method: 'POST',
            body: JSON.stringify({ message, e, n })
        });
    },
    
    /**
     * Decryption API
     */
    async decrypt(ciphertext, d, n, p = null, q = null, use_crt = false) {
        return this.request('/crypto/decrypt', {
            method: 'POST',
            body: JSON.stringify({ 
                ciphertext, 
                d, 
                n, 
                p: p || 0, 
                q: q || 0,
                use_crt 
            })
        });
    },
    
    /**
     * Sign Message API
     */
    async sign(message, d, n) {
        return this.request('/crypto/sign', {
            method: 'POST',
            body: JSON.stringify({ message, d, n })
        });
    },
    
    /**
     * Verify Signature API
     */
    async verify(message, signature, e, n) {
        return this.request('/crypto/verify', {
            method: 'POST',
            body: JSON.stringify({ message, signature, e, n })
        });
    },
    
    /**
     * Run Demo API
     */
    async runDemo(demoName) {
        return this.request(`/demo/${demoName}`, {
            method: 'GET'
        });
    },
    
    /**
     * List Demos API
     */
    async listDemos() {
        return this.request('/demo/list', {
            method: 'GET'
        });
    }
};