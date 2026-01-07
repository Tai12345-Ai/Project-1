// rsa_tool/static/js/ui.js
/**
 * UI Utilities - Handle UI updates and interactions
 */

const UI = {
    /**
     * Show loading state on button
     */
    setButtonLoading(button, loading = true) {
        if (loading) {
            button.classList.add('loading');
            button.disabled = true;
        } else {
            button.classList.remove('loading');
            button.disabled = false;
        }
    },
    
    /**
     * Show success message
     */
    showSuccess(container, message, data = null) {
        let html = `
            <div class="result-success">
                <span class="result-icon">✓</span>
                <div>
                    <strong>${message}</strong>
                    ${data ? `<div style="margin-top: 0.5rem;">${data}</div>` : ''}
                </div>
            </div>
        `;
        
        container.innerHTML = html;
        container.style.display = 'block';
        this.scrollToElement(container);
    },
    
    /**
     * Show error message
     */
    showError(container, message) {
        container.innerHTML = `
            <div class="result-error">
                <span class="result-icon">✗</span>
                <strong>${message}</strong>
            </div>
        `;
        container.style.display = 'block';
        this.scrollToElement(container);
    },
    
    /**
     * Show key pair output
     */
    showKeyPair(container, publicKey, privateKey) {
        const html = `
            <div class="output-terminal output-success">
✓ Keys generated successfully!

<span style="color: #60a5fa; font-weight: bold;">PUBLIC KEY:</span>
  e = ${publicKey.e}
  n = ${publicKey.n}
  n bit length = ${publicKey.n_bits} bits

<span style="color: #f59e0b; font-weight: bold;">PRIVATE KEY:</span>
  d = ${privateKey.d}
  p = ${privateKey.p} (${privateKey.p_bits} bits)
  q = ${privateKey.q} (${privateKey.q_bits} bits)
  n = p × q

<span style="color: #4ade80;">✓ Keys ready for use!</span>
            </div>
            <button class="copy-btn" onclick="UI.copyToClipboard('${publicKey.e}')">
                📋 Copy Public Key (e)
            </button>
        `;
        
        container.innerHTML = html;
        container.style.display = 'block';
        this.scrollToElement(container);
    },
    
    /**
     * Show encryption output
     */
    showEncryptOutput(container, result, originalMessage) {
        const ciphertextDisplay = result.ciphertext.slice(0, 3).join(',\n');
        const more = result.ciphertext.length > 3 ? `\n... and ${result.ciphertext.length - 3} more blocks` : '';
        
        const html = `
            <div class="output-terminal output-success">
✓ Message encrypted successfully!

<span style="color: #60a5fa;">Original Message:</span>
"${originalMessage}"

<span style="color: #60a5fa;">Encryption Info:</span>
  Number of blocks: ${result.num_blocks}
  Original length: ${result.original_length} bytes

<span style="color: #60a5fa;">Ciphertext (first 3 blocks):</span>
${ciphertextDisplay}${more}

<span style="color: #4ade80;">✓ Copy ciphertext below to decrypt!</span>
            </div>
            <button class="copy-btn" onclick="UI.copyToClipboard('${result.ciphertext.join(', ')}')">
                📋 Copy Ciphertext
            </button>
        `;
        
        container.innerHTML = html;
        container.style.display = 'block';
        this.scrollToElement(container);
    },
    
    /**
     * Show decryption output
     */
    showDecryptOutput(container, result) {
        const crtInfo = result.use_crt ? `\n  CRT optimization used\n  Time: ${result.time_ms.toFixed(2)} ms` : '';
        
        const html = `
            <div class="output-terminal output-success">
✓ Message decrypted successfully!
${crtInfo}

<span style="color: #60a5fa;">Plaintext:</span>
"${result.plaintext}"

<span style="color: #4ade80;">✓ Decryption complete!</span>
            </div>
        `;
        
        container.innerHTML = html;
        container.style.display = 'block';
        this.scrollToElement(container);
    },
    
    /**
     * Show signature output
     */
    showSignOutput(container, signature, message) {
        const sigPreview = signature.length > 100 ? signature.substring(0, 100) + '...' : signature;
        
        const html = `
            <div class="output-terminal output-success">
✓ Message signed successfully!

<span style="color: #60a5fa;">Message:</span>
"${message}"

<span style="color: #60a5fa;">Signature:</span>
${sigPreview}

<span style="color: #4ade80;">✓ Copy signature to verify!</span>
            </div>
            <button class="copy-btn" onclick="UI.copyToClipboard('${signature}')">
                📋 Copy Signature
            </button>
        `;
        
        container.innerHTML = html;
        container.style.display = 'block';
        this.scrollToElement(container);
    },
    
    /**
     * Show verification output
     */
    showVerifyOutput(container, valid, message) {
        const status = valid ? 
            '<span class="output-success">✓ SIGNATURE VALID</span>' : 
            '<span class="output-error">✗ SIGNATURE INVALID</span>';
        
        const explanation = valid ?
            '<span class="output-success">✓ The signature is authentic and matches the message!</span>' :
            '<span class="output-error">✗ The signature does not match the message or has been tampered with!</span>';
        
        const html = `
            <div class="output-terminal">
${status}

<span style="color: #60a5fa;">Message:</span>
"${message}"

<span style="color: #60a5fa;">Verification Result:</span>
${explanation}
            </div>
        `;
        
        container.innerHTML = html;
        container.style.display = 'block';
        this.scrollToElement(container);
    },
    
    /**
     * Show demo output
     */
    showDemoOutput(container, output) {
        container.innerHTML = output;
        container.style.display = 'block';
        this.scrollToElement(container);
    },
    
    /**
     * Copy text to clipboard
     */
    copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            // Find the button that was clicked
            const buttons = document.querySelectorAll('.copy-btn');
            buttons.forEach(btn => {
                if (btn.onclick && btn.onclick.toString().includes(text.substring(0, 20))) {
                    const originalText = btn.innerHTML;
                    btn.innerHTML = '✓ Copied!';
                    btn.classList.add('copied');
                    
                    setTimeout(() => {
                        btn.innerHTML = originalText;
                        btn.classList.remove('copied');
                    }, 2000);
                }
            });
        }).catch(err => {
            console.error('Failed to copy:', err);
            alert('Failed to copy to clipboard');
        });
    },
    
    /**
     * Scroll to element
     */
    scrollToElement(element) {
        setTimeout(() => {
            element.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    },
    
    /**
     * Auto-fill form fields
     */
    autoFillFields(fields) {
        Object.keys(fields).forEach(fieldId => {
            const element = document.getElementById(fieldId);
            if (element) {
                element.value = fields[fieldId];
            }
        });
    },
    
    /**
     * Clear output container
     */
    clearOutput(container) {
        container.innerHTML = '';
        container.style.display = 'none';
    },
    
    /**
     * Get form data as object
     */
    getFormData(formElement) {
        const formData = new FormData(formElement);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        return data;
    },
    
    /**
     * Validate form fields
     */
    validateFields(fields) {
        const errors = [];
        
        Object.keys(fields).forEach(fieldName => {
            const value = fields[fieldName];
            
            if (!value || value.trim() === '') {
                errors.push(`${fieldName} is required`);
            }
        });
        
        return errors;
    }
};