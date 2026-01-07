"""
Demo 02: Miller-Rabin Primality Test
CLRS 31.8 - Primality Testing
"""
from .demo_utils import *

def demo_miller_rabin():
    """Demo 02: Miller-Rabin primality test chi tiết"""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 18 + "DEMO 02: MILLER-RABIN PRIMALITY TEST" + " " * 24 + "║")
    print("║" + " " * 22 + "CLRS 31.8 - Primality Testing" + " " * 27 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # PHẦN 1: Algorithm Explanation
    print("=" * 80)
    print("THUẬT TOÁN MILLER-RABIN")
    print("=" * 80)
    print("""
Ý tưởng: Kiểm tra xem n có phải số nguyên tố không
    
Bước 1: Viết n-1 = 2^s × d (d lẻ)
Bước 2: Chọn ngẫu nhiên a ∈ [2, n-2]
Bước 3: Tính x = a^d mod n
Bước 4: Kiểm tra:
        - Nếu x = 1 hoặc x = n-1: có thể là nguyên tố
        - Lặp s-1 lần: x = x^2 mod n
        - Nếu x = n-1: có thể là nguyên tố
        - Ngược lại: hợp số

Xác suất lỗi: ≤ (1/4)^k với k là số round
""")
    
    # PHẦN 2: Test với các số đã biết
    print("=" * 80)
    print("PHẦN 1: KIỂM TRA CÁC SỐ ĐÃ BIẾT")
    print("=" * 80)
    
    test_cases = [
        (2, "Nguyên tố nhỏ nhất", True),
        (3, "Nguyên tố", True),
        (17, "Nguyên tố", True),
        (19, "Nguyên tố", True),
        (4, "Hợp số: 2²", False),
        (15, "Hợp số: 3 × 5", False),
        (21, "Hợp số: 3 × 7", False),
        (91, "Hợp số: 7 × 13", False),
        (561, "Carmichael number: 3 × 11 × 17", False),
        (1105, "Carmichael number: 5 × 13 × 17", False),
    ]
    
    rounds = 20
    print(f"\nSử dụng {rounds} rounds\n")
    print(f"{'Số':<8} {'Kết quả':<15} {'Mô tả':<35} {'Đúng?'}")
    print("-" * 80)
    
    correct = 0
    for n, desc, expected in test_cases:
        result = is_probable_prime(n, rounds=rounds)
        status = "PRIME" if result else "COMPOSITE"
        check = "✓" if (result == expected) else "✗"
        correct += (result == expected)
        print(f"{n:<8} {status:<15} {desc:<35} {check}")
    
    print(f"\nĐộ chính xác: {correct}/{len(test_cases)} ({correct/len(test_cases)*100:.1f}%)")
    
    # PHẦN 3: Probability Analysis
    print("\n" + "=" * 80)
    print("PHẦN 2: PHÂN TÍCH XÁC SUẤT SAI")
    print("=" * 80)
    
    print("\nXác suất algorithm cho kết quả sai (số hợp số được xác định là nguyên tố):")
    print()
    print(f"{'Rounds (k)':<15} {'Error Probability':<25} {'Percentage'}")
    print("-" * 60)
    
    for k in [1, 5, 10, 20, 40, 100]:
        prob = (0.25) ** k
        print(f"{k:<15} (1/4)^{k} = {prob:<20.2e} {prob*100:.15f}%")
    
    print("\n💡 Với k=40 rounds, xác suất sai < 10^-24")
    print("   (An toàn hơn xác suất lỗi phần cứng!)")
    
    # PHẦN 4: Prime Generation Performance
    print("\n" + "=" * 80)
    print("PHẦN 3: SINH SỐ NGUYÊN TỐ - PERFORMANCE")
    print("=" * 80)
    
    print("\nThời gian sinh số nguyên tố theo kích thước:\n")
    print(f"{'Bits':<10} {'Time (ms)':<15} {'Prime (first 30 digits)...'}")
    print("-" * 80)
    
    for bits in [64, 128, 256, 512]:
        times = []
        prime = None
        
        # Chạy 3 lần và lấy trung bình
        for _ in range(3):
            t0 = time.perf_counter()
            prime = generate_prime(bits, rounds=rounds)
            t1 = time.perf_counter()
            times.append((t1 - t0) * 1000)
        
        avg_time = sum(times) / len(times)
        prime_str = str(prime)
        display = prime_str[:30] + "..." if len(prime_str) > 30 else prime_str
        
        print(f"{bits:<10} {avg_time:<15.2f} {display}")
    
    # PHẦN 5: Compare với Trial Division
    print("\n" + "=" * 80)
    print("PHẦN 4: SO SÁNH VỚI TRIAL DIVISION")
    print("=" * 80)
    
    print("\nTrial Division: Thử chia cho tất cả số từ 2 đến √n")
    print("Miller-Rabin: Probabilistic test với k rounds\n")
    
    def trial_division(n):
        """Slow but certain primality test"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    # Test với số nhỏ
    test_n = 104729  # Prime number
    
    print(f"Testing n = {test_n}")
    
    # Trial Division
    t0 = time.perf_counter()
    result_td = trial_division(test_n)
    t1 = time.perf_counter()
    time_td = (t1 - t0) * 1000
    
    # Miller-Rabin
    t0 = time.perf_counter()
    result_mr = is_probable_prime(test_n, rounds=20)
    t1 = time.perf_counter()
    time_mr = (t1 - t0) * 1000
    
    print(f"\nTrial Division:")
    print(f"   Result: {'PRIME' if result_td else 'COMPOSITE'}")
    print(f"   Time: {time_td:.4f} ms")
    
    print(f"\nMiller-Rabin (k=20):")
    print(f"   Result: {'PRIME' if result_mr else 'COMPOSITE'}")
    print(f"   Time: {time_mr:.4f} ms")
    
    if time_td > 0:
        print(f"\n⚡ Speedup: {time_td/time_mr:.2f}x faster")
    
    print("\n💡 Kết luận:")
    print("   • Miller-Rabin nhanh hơn rất nhiều với số lớn")
    print("   • Cho phép sinh số nguyên tố lớn cho RSA")
    print("   • Trade-off: Certainty vs Speed")
    
    print("\n✅ Demo 02 completed!")
