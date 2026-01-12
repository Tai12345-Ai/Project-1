"""
RSA Cryptography Tool - Main Application
Kiến trúc: app.py (routes) → services.py (logic) → demos.py (demonstrations)
"""
from flask import Flask, render_template, request, jsonify
import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import local modules
from services import RSAService
from demos import DemoService
from playground import PlaygroundService

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-rsa-tool')
app.config['DEBUG'] = os.environ.get('FLASK_ENV', 'development') != 'production'

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Trang chủ - Main page"""
    return render_template('index.html')

@app.route('/api/key/generate', methods=['POST'])
def generate_key():
    """
    API: Sinh cặp khóa RSA
    
    POST /api/key/generate
    Body: {"bits": 1024, "e": 65537}
    Returns: {"success": true, "data": {"public_key": {...}, "private_key": {...}}}
    """
    try:
        data = request.json or {}
        bits = int(data.get('bits', 1024))
        e = int(data.get('e', 65537))
        
        # Validation
        if bits < 512 or bits > 4096:
            raise ValueError("Key size must be between 512 and 4096 bits")
        
        # Generate keys using service
        result = RSAService.generate_keys(bits=bits, e=e)
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as err:
        return jsonify({'success': False, 'error': str(err)}), 400

@app.route('/api/crypto/encrypt', methods=['POST'])
def encrypt():
    """
    API: Mã hóa message
    
    POST /api/crypto/encrypt
    Body: {"message": "text", "e": "65537", "n": "123...", "padding_mode": "textbook|oaep"}
    """
    try:
        data = request.json
        message = data.get('message', '')
        e = int(data.get('e'))
        n = int(data.get('n'))
        padding_mode = data.get('padding_mode', 'textbook')
        
        if not message:
            raise ValueError("Message cannot be empty")
        
        result = RSAService.encrypt_with_padding(message, e, n, padding_mode)
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as err:
        return jsonify({'success': False, 'error': str(err)}), 400

@app.route('/api/crypto/decrypt', methods=['POST'])
def decrypt():
    """
    API: Giải mã ciphertext
    
    POST /api/crypto/decrypt
    Body: {"ciphertext": ["123", "456"], "d": "789", "n": "101112", "padding_mode": "textbook|oaep"}
    """
    try:
        data = request.json
        ciphertext = data.get('ciphertext')
        
        # Validate ciphertext first
        if not ciphertext:
            raise ValueError("Ciphertext cannot be empty")
        
        # Handle both int and list
        if isinstance(ciphertext, list):
            if len(ciphertext) == 0:
                raise ValueError("Ciphertext list cannot be empty")
            # Convert each element, handling scientific notation
            converted = []
            for c in ciphertext:
                if c and str(c).strip():
                    c_str = str(c).strip()
                    # Handle scientific notation
                    if 'e' in c_str.lower():
                        try:
                            c_int = int(float(c_str))
                        except:
                            raise ValueError(f"Invalid ciphertext value: {c_str}")
                    else:
                        c_int = int(c_str)
                    converted.append(c_int)
            if len(converted) == 0:
                raise ValueError("No valid ciphertext values provided")
            ciphertext = converted
        else:
            ciphertext_str = str(ciphertext).strip()
            if not ciphertext_str:
                raise ValueError("Ciphertext cannot be empty")
            # Handle scientific notation
            if 'e' in ciphertext_str.lower():
                try:
                    ciphertext = int(float(ciphertext_str))
                except:
                    raise ValueError(f"Invalid ciphertext format: {ciphertext_str}")
            else:
                ciphertext = int(ciphertext_str)
        
        d = int(data.get('d'))
        n = int(data.get('n'))
        p = int(data.get('p', 0)) or None
        q = int(data.get('q', 0)) or None
        use_crt = data.get('use_crt', False)
        padding_mode = data.get('padding_mode', 'textbook')
        
        result = RSAService.decrypt_with_padding(ciphertext, d, n, padding_mode, p, q, use_crt)
        
        return jsonify({
            'success': True,
            'data': result
        })
    except ValueError as err:
        return jsonify({'success': False, 'error': str(err)}), 400
    except Exception as err:
        return jsonify({'success': False, 'error': f'Decryption failed: {str(err)}'}), 400

@app.route('/api/crypto/sign', methods=['POST'])
def sign():
    """
    API: Ký số message
    
    POST /api/crypto/sign
    Body: {"message": "text", "d": "789", "n": "101112", "padding_mode": "textbook|pss"}
    """
    try:
        data = request.json
        message = data.get('message', '')
        d = int(data.get('d'))
        n = int(data.get('n'))
        padding_mode = data.get('padding_mode', 'textbook')
        
        if not message:
            raise ValueError("Message cannot be empty")
        
        result = RSAService.sign_with_padding(message, d, n, padding_mode)
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as err:
        return jsonify({'success': False, 'error': str(err)}), 400

@app.route('/api/crypto/verify', methods=['POST'])
def verify():
    """
    API: Xác minh chữ ký
    
    POST /api/crypto/verify
    Body: {"message": "text", "signature": "123", "e": "65537", "n": "789", "padding_mode": "textbook|pss"}
    """
    try:
        data = request.json
        message = data.get('message', '')
        signature = int(data.get('signature'))
        e = int(data.get('e'))
        n = int(data.get('n'))
        padding_mode = data.get('padding_mode', 'textbook')
        
        if not message:
            raise ValueError("Message cannot be empty")
        
        result = RSAService.verify_with_padding(message, signature, e, n, padding_mode)
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as err:
        return jsonify({'success': False, 'error': str(err)}), 400

@app.route('/api/demo/<demo_name>', methods=['GET'])
def run_demo(demo_name):
    """
    API: Chạy demonstration
    
    GET /api/demo/<demo_name>
    
    Demos available:
    - basic_rsa: Demo 01 - Basic RSA
    - miller_rabin: Demo 02 - Miller-Rabin
    - crt_speed: Demo 03 - CRT Speed
    - pollard_rho: Demo 04 - Pollard Rho
    - textbook_padding: Demo 05 - Textbook Padding
    - wiener_attack: Demo 06 - Wiener's Attack
    - key_size_security: Demo 07 - Key Size Security
    - rsa_properties: Demo 08 - RSA Properties
    """
    try:
        output = DemoService.run(demo_name)
        
        return jsonify({
            'success': True,
            'data': {'output': output}
        })
    except Exception as err:
        return jsonify({'success': False, 'error': str(err)}), 500

@app.route('/api/demo/list', methods=['GET'])
def list_demos():
    """API: Liệt kê tất cả demos"""
    demos = [
        {
            'id': 'basic_rsa',
            'title': 'Demo 01: Basic RSA',
            'description': 'RSA encryption, decryption, signatures với step-by-step',
            'icon': '📝'
        },
        {
            'id': 'miller_rabin',
            'title': 'Demo 02: Miller-Rabin',
            'description': 'Primality testing và prime generation chi tiết',
            'icon': '🔢'
        },
        {
            'id': 'crt_speed',
            'title': 'Demo 03: CRT Speed',
            'description': 'Chinese Remainder Theorem optimization analysis',
            'icon': '⚡'
        },
        {
            'id': 'pollard_rho',
            'title': 'Demo 04: Pollard Rho',
            'description': 'Factorization attack trên RSA yếu',
            'icon': '💥'
        },
        {
            'id': 'textbook_padding',
            'title': 'Demo 05: Textbook Padding',
            'description': 'Security vulnerabilities của textbook RSA',
            'icon': '⚠️'
        },
        {
            'id': 'wiener_attack',
            'title': 'Demo 06: Wiener\'s Attack',
            'description': 'Attack RSA khi d quá nhỏ (continued fraction)',
            'icon': '🎯'
        },
        {
            'id': 'key_size_security',
            'title': 'Demo 07: Key Size Security',
            'description': 'Phân tích security theo key size và performance',
            'icon': '🔐'
        },
        {
            'id': 'rsa_properties',
            'title': 'Demo 08: RSA Properties',
            'description': 'Mathematical properties: homomorphic, CRT, etc.',
            'icon': '🧮'
        },
        {
            'id': 'padding_comparison',
            'title': 'Demo 09: Padding Comparison',
            'description': 'So sánh Textbook vs OAEP vs PSS - Security analysis',
            'icon': '🔒'
        }
    ]
    
    return jsonify({
        'success': True,
        'data': {'demos': demos}
    })

# ==================== PLAYGROUND ROUTES ====================

@app.route('/api/playground/list', methods=['GET'])
def playground_list():
    """
    API: List all available playground labs
    
    GET /api/playground/list
    Returns: {"success": true, "data": {"labs": [...]}}
    """
    try:
        labs = PlaygroundService.list_all()
        return jsonify({
            'success': True,
            'data': {'labs': labs}
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/playground/<lab_id>/info', methods=['GET'])
def playground_info(lab_id):
    """
    API: Get detailed information about a specific lab
    
    GET /api/playground/<lab_id>/info
    Returns: {"success": true, "data": {lab metadata, parameters, examples}}
    """
    try:
        info = PlaygroundService.get_lab_info(lab_id)
        return jsonify({
            'success': True,
            'data': info
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/playground/<lab_id>/run', methods=['POST'])
def playground_run(lab_id):
    """
    API: Execute a playground lab with parameters
    
    POST /api/playground/<lab_id>/run
    Body: {lab-specific parameters}
    Returns: {"success": true, "data": {experiment results}}
    """
    try:
        params = request.json or {}
        result = PlaygroundService.execute(lab_id, params)
        return jsonify({
            'success': True,
            'data': result
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') != 'production'
    
    print("Starting RSA Tool...")
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Open browser at: http://127.0.0.1:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
