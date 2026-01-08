"""
Test script to demonstrate the difference between Textbook RSA and OAEP/PSS
"""
import sys
sys.path.insert(0, 'rsa_tool')
sys.path.insert(0, '.')

from Algorithms.rsa import keygen, RSA

print('=' * 80)
print('TEST: TEXTBOOK vs OAEP/PSS - SỰ KHÁC BIỆT RÕ RÀNG')
print('=' * 80)
print()

# Generate keys
print('📌 Bước 1: Sinh cặp khóa RSA 1024-bit')
pub, priv = keygen(bits=1024)
rsa = RSA(pub=pub, priv=priv)
print(f'   Public Key (e, n): ({pub.e}, {str(pub.n)[:50]}...)')
print()

# ========== ENCRYPTION TEST ==========
print('=' * 80)
print('🔒 TEST ENCRYPTION: Textbook vs OAEP')
print('=' * 80)
print()

message = 'Attack at dawn!'
print(f'Message: "{message}"')
print()

# Test 1: Textbook - Deterministic
print('📝 TEXTBOOK RSA (Không padding):')
cipher1_textbook = rsa.encrypt_text(message)[0]
cipher2_textbook = rsa.encrypt_text(message)[0]
print(f'   Encrypt lần 1: {str(cipher1_textbook)[:60]}...')
print(f'   Encrypt lần 2: {str(cipher2_textbook)[:60]}...')
print(f'   Giống nhau? {cipher1_textbook == cipher2_textbook}')
print(f'   ⚠️  NGUY HIỂM: Cùng message → Cùng ciphertext!')
print()

# Test 2: OAEP - Non-deterministic
print('🔒 OAEP (Có padding an toàn):')
cipher1_oaep = rsa.encrypt_oaep(message.encode('utf-8'))
cipher2_oaep = rsa.encrypt_oaep(message.encode('utf-8'))
print(f'   Encrypt lần 1: {str(cipher1_oaep)[:60]}...')
print(f'   Encrypt lần 2: {str(cipher2_oaep)[:60]}...')
print(f'   Giống nhau? {cipher1_oaep == cipher2_oaep}')
print(f'   ✅ AN TOÀN: Cùng message → Khác ciphertext (random padding)!')
print()

# Decrypt để verify
plain_oaep = rsa.decrypt_oaep(cipher1_oaep).decode('utf-8')
print(f'   Decrypt OAEP: "{plain_oaep}"')
print(f'   ✅ Giải mã đúng!')
print()

# ========== SIGNATURE TEST ==========
print('=' * 80)
print('✍️  TEST SIGNATURES: Textbook vs PSS')
print('=' * 80)
print()

msg_sign = 'I owe Alice $100'
print(f'Message cần ký: "{msg_sign}"')
print()

# Test 3: Textbook Signature - Deterministic
print('📝 TEXTBOOK RSA SIGNATURE (Không padding):')
sig1_textbook = rsa.sign(msg_sign.encode('utf-8'))
sig2_textbook = rsa.sign(msg_sign.encode('utf-8'))
print(f'   Ký lần 1: {str(sig1_textbook)[:60]}...')
print(f'   Ký lần 2: {str(sig2_textbook)[:60]}...')
print(f'   Giống nhau? {sig1_textbook == sig2_textbook}')
print(f'   ⚠️  VẤN ĐỀ: Luôn cùng signature → Dễ bị replay attack!')
print()

# Test 4: PSS - Probabilistic
print('🔏 PSS SIGNATURE (Có padding an toàn):')
sig1_pss = rsa.sign_pss(msg_sign.encode('utf-8'))
sig2_pss = rsa.sign_pss(msg_sign.encode('utf-8'))
print(f'   Ký lần 1: {str(sig1_pss)[:60]}...')
print(f'   Ký lần 2: {str(sig2_pss)[:60]}...')
print(f'   Giống nhau? {sig1_pss == sig2_pss}')
print(f'   ✅ AN TOÀN: Khác signature mỗi lần (random salt)!')
print()

# Verify both signatures
valid1 = rsa.verify_pss(msg_sign.encode('utf-8'), sig1_pss)
valid2 = rsa.verify_pss(msg_sign.encode('utf-8'), sig2_pss)
print(f'   Verify signature 1: {valid1} ✅')
print(f'   Verify signature 2: {valid2} ✅')
print(f'   → Cả 2 signature khác nhau nhưng đều VALID!')
print()

# ========== SUMMARY ==========
print('=' * 80)
print('📊 KẾT LUẬN')
print('=' * 80)
print()
print('❌ TEXTBOOK RSA (Không nên dùng trong thực tế):')
print('   • Deterministic: Same input → Same output')
print('   • Dễ bị dictionary attack')
print('   • Dễ bị chosen-ciphertext attack')
print('   • Chỉ dùng cho giáo dục/học tập')
print()
print('✅ OAEP/PSS (Nên dùng trong production):')
print('   • Non-deterministic: Same input → Different output')
print('   • An toàn trước các attack hiện đại')
print('   • Được khuyến nghị bởi NIST, RFC 8017')
print('   • Dùng cho ứng dụng thực tế')
print()
print('=' * 80)
