"""
Demos package - Educational Demonstrations
Minh họa các khái niệm RSA từ CLRS Chương 31
"""
from .demo_01_basic_rsa import demo_basic_rsa
from .demo_02_miller_rabin import demo_miller_rabin
from .demo_03_crt_speed import demo_crt_speed
from .demo_04_pollard_rho import demo_pollard_rho
from .demo_05_textbook_padding import demo_textbook_padding
from .demo_06_wiener_attack import demo_wiener_attack
from .demo_07_key_size_security import demo_key_size_security
from .demo_08_rsa_properties import demo_rsa_properties

import io
from contextlib import redirect_stdout

class DemoService:
    """Service chạy các demonstrations"""
    
    DEMOS = {
        'basic_rsa': demo_basic_rsa,
        'miller_rabin': demo_miller_rabin,
        'crt_speed': demo_crt_speed,
        'pollard_rho': demo_pollard_rho,
        'textbook_padding': demo_textbook_padding,
        'wiener_attack': demo_wiener_attack,
        'key_size_security': demo_key_size_security,
        'rsa_properties': demo_rsa_properties
    }
    
    @staticmethod
    def run(demo_name):
        """
        Chạy demo và capture output
        
        Args:
            demo_name: Tên demo (basic_rsa, miller_rabin, etc.)
            
        Returns:
            str: Output của demo
        """
        output = io.StringIO()
        
        with redirect_stdout(output):
            demo_func = DemoService.DEMOS.get(demo_name)
            if demo_func:
                demo_func()
            else:
                print(f"❌ Unknown demo: {demo_name}")
        
        return output.getvalue()
    
    @staticmethod
    def list_all():
        """Liệt kê tất cả demos"""
        return list(DemoService.DEMOS.keys())

__all__ = ['DemoService']
