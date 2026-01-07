// rsa_tool/static/js/main.js
/**
 * Main Application - Event handlers and initialization
 */

// Store current keys globally for easy access
let currentKeys = {
    public: null,
    private: null
};

/**
 * Initialize application
 */
document.addEventListener('DOMContentLoaded', () => {
    initializeNavigation();
    initializeKeyGeneration();
    initializeEncryption();
    initializeDecryption();
    initializeSignature();
    initializeVerification();
    initializeDemos();
});

/**
 * Navigation between sections
 */
function initializeNavigation() {
    const menuItems = document.querySelectorAll('.menu-item');
    const sections = document.querySelectorAll('.page-section');
    
    menuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            const targetPage = item.dataset.page;
            
            // Update active menu item
            menuItems.forEach(mi => mi.classList.remove('active'));
            item.classList.add('active');
            
            // Show corresponding section
            sections.forEach(section => {
                if (section.id === targetPage) {
                    section.classList.add('active');
                } else {
                    section.classList.remove('active');
                }
            });
            
            // Update URL hash
            window.location.hash = targetPage;
        });
    });
    
    // Handle initial hash
    const hash = window.location.hash.substring(1);
    if (hash) {
        const targetItem = document.querySelector(`[data-page="${hash}"]`);
        if (targetItem) {
            targetItem.click();
        }
    }
}

/**
 * Key Generation Handler
 */
function initializeKeyGeneration() {
    const form = document.getElementById('keygenForm');
    const output = document.getElementById('keygenOutput');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const bits = parseInt(document.getElementById('keyBits').value);
        
        UI.setButtonLoading(submitBtn, true);
        UI.clearOutput(output);
        
        try {
            const response = await API.generateKey(bits);
            
            if (response.success) {
                const { public_key, private_key } = response.data;
                
                // Store keys globally
                currentKeys.public = public_key;
                currentKeys.private = private_key;
                
                // Show output
                UI.showKeyPair(output, public_key, private_key);
                
                // Auto-fill other forms
                UI.autoFillFields({
                    'encryptE': public_key.e,
                    'encryptN': public_key.n,
                    'decryptD': private_key.d,
                    'decryptN': private_key.n,
                    'signD': private_key.d,
                    'signN': private_key.n,
                    'verifyE': public_key.e,
                    'verifyN': public_key.n
                });
            } else {
                UI.showError(output, response.error || 'Key generation failed');
            }
        } catch (error) {
            UI.showError(output, `Error: ${error.message}`);
        } finally {
            UI.setButtonLoading(submitBtn, false);
        }
    });
}

/**
 * Encryption Handler
 */
function initializeEncryption() {
    const form = document.getElementById('encryptForm');
    const output = document.getElementById('encryptOutput');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = document.getElementById('encryptMessage').value;
        const e_value = document.getElementById('encryptE').value;
        const n = document.getElementById('encryptN').value;
        
        // Validate
        const errors = UI.validateFields({ message, e: e_value, n });
        if (errors.length > 0) {
            UI.showError(output, errors.join(', '));
            return;
        }
        
        UI.setButtonLoading(submitBtn, true);
        UI.clearOutput(output);
        
        try {
            const response = await API.encrypt(message, e_value, n);
            
            if (response.success) {
                UI.showEncryptOutput(output, response.data, message);
                
                // Auto-fill decrypt form
                UI.autoFillFields({
                    'decryptCiphertext': response.data.ciphertext.join(', ')
                });
            } else {
                UI.showError(output, response.error || 'Encryption failed');
            }
        } catch (error) {
            UI.showError(output, `Error: ${error.message}`);
        } finally {
            UI.setButtonLoading(submitBtn, false);
        }
    });
}

/**
 * Decryption Handler
 */
function initializeDecryption() {
    const form = document.getElementById('decryptForm');
    const output = document.getElementById('decryptOutput');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const ciphertextStr = document.getElementById('decryptCiphertext').value;
        const d = document.getElementById('decryptD').value;
        const n = document.getElementById('decryptN').value;
        const useCRT = document.getElementById('useCRT').checked;
        
        // Validate
        const errors = UI.validateFields({ ciphertext: ciphertextStr, d, n });
        if (errors.length > 0) {
            UI.showError(output, errors.join(', '));
            return;
        }
        
        // Parse ciphertext
        const ciphertext = ciphertextStr.split(',').map(s => s.trim());
        
        // Get p and q if using CRT
        let p = null, q = null;
        if (useCRT && currentKeys.private) {
            p = currentKeys.private.p;
            q = currentKeys.private.q;
        }
        
        UI.setButtonLoading(submitBtn, true);
        UI.clearOutput(output);
        
        try {
            const response = await API.decrypt(ciphertext, d, n, p, q, useCRT);
            
            if (response.success) {
                UI.showDecryptOutput(output, response.data);
            } else {
                UI.showError(output, response.error || 'Decryption failed');
            }
        } catch (error) {
            UI.showError(output, `Error: ${error.message}`);
        } finally {
            UI.setButtonLoading(submitBtn, false);
        }
    });
}

/**
 * Signature Handler
 */
function initializeSignature() {
    const form = document.getElementById('signForm');
    const output = document.getElementById('signOutput');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = document.getElementById('signMessage').value;
        const d = document.getElementById('signD').value;
        const n = document.getElementById('signN').value;
        
        // Validate
        const errors = UI.validateFields({ message, d, n });
        if (errors.length > 0) {
            UI.showError(output, errors.join(', '));
            return;
        }
        
        UI.setButtonLoading(submitBtn, true);
        UI.clearOutput(output);
        
        try {
            const response = await API.sign(message, d, n);
            
            if (response.success) {
                const signature = response.data.signature;
                UI.showSignOutput(output, signature, message);
                
                // Auto-fill verify form
                UI.autoFillFields({
                    'verifyMessage': message,
                    'verifySignature': signature
                });
            } else {
                UI.showError(output, response.error || 'Signing failed');
            }
        } catch (error) {
            UI.showError(output, `Error: ${error.message}`);
        } finally {
            UI.setButtonLoading(submitBtn, false);
        }
    });
}

/**
 * Verification Handler
 */
function initializeVerification() {
    const form = document.getElementById('verifyForm');
    const output = document.getElementById('verifyOutput');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = document.getElementById('verifyMessage').value;
        const signature = document.getElementById('verifySignature').value;
        const e_value = document.getElementById('verifyE').value;
        const n = document.getElementById('verifyN').value;
        
        // Validate
        const errors = UI.validateFields({ message, signature, e: e_value, n });
        if (errors.length > 0) {
            UI.showError(output, errors.join(', '));
            return;
        }
        
        UI.setButtonLoading(submitBtn, true);
        UI.clearOutput(output);
        
        try {
            const response = await API.verify(message, signature, e_value, n);
            
            if (response.success) {
                UI.showVerifyOutput(output, response.data.valid, message);
            } else {
                UI.showError(output, response.error || 'Verification failed');
            }
        } catch (error) {
            UI.showError(output, `Error: ${error.message}`);
        } finally {
            UI.setButtonLoading(submitBtn, false);
        }
    });
}

/**
 * Demos Handler
 */
function initializeDemos() {
    const demoButtons = document.querySelectorAll('.demo-card');
    const output = document.getElementById('demoOutput');
    
    demoButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const demoName = button.dataset.demo;
            
            // Disable all demo buttons
            demoButtons.forEach(btn => btn.disabled = true);
            
            // Show loading
            output.innerHTML = `
                <div style="text-align: center; padding: 2rem;">
                    <span class="spinner" style="width: 40px; height: 40px; border-width: 4px;"></span>
                    <p style="margin-top: 1rem; color: #d4d4d4;">Running ${button.querySelector('.demo-title').textContent}...</p>
                </div>
            `;
            output.style.display = 'block';
            UI.scrollToElement(output);
            
            try {
                const response = await API.runDemo(demoName);
                
                if (response.success) {
                    UI.showDemoOutput(output, response.data.output);
                } else {
                    output.innerHTML = `<span style="color: var(--error);">✗ Error: ${response.error}</span>`;
                }
            } catch (error) {
                output.innerHTML = `<span style="color: var(--error);">✗ Error: ${error.message}</span>`;
            } finally {
                // Re-enable demo buttons
                demoButtons.forEach(btn => btn.disabled = false);
            }
        });
    });
}

/**
 * Utility: Format large numbers
 */
function formatNumber(num) {
    const str = num.toString();
    if (str.length > 100) {
        return str.substring(0, 50) + '...' + str.substring(str.length - 50);
    }
    return str;
}

/**
 * Utility: Validate numeric input
 */
function isValidNumber(str) {
    return /^\d+$/.test(str.trim());
}