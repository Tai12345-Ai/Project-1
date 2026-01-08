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
from .demo_09_padding_comparison import demo_padding_comparison

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
        'rsa_properties': demo_rsa_properties,
        'padding_comparison': demo_padding_comparison
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
        demo_func = DemoService.DEMOS.get(demo_name)
        if not demo_func:
            return f"❌ Unknown demo: {demo_name}"
        
        # Call demo function and get result
        try:
            result = demo_func()
            # If result is a string, return it directly
            if isinstance(result, str) and result:
                return result
        except Exception as e:
            return f"❌ Demo error: {str(e)}"
        
        # Fallback: capture stdout for demos that use print()
        output = io.StringIO()
        try:
            with redirect_stdout(output):
                demo_func()
            return output.getvalue()
        except Exception as e:
            return f"❌ Demo execution error: {str(e)}"
    
    @staticmethod
    def list_all():
        """Liệt kê tất cả demos"""
        return list(DemoService.DEMOS.keys())

__all__ = ['DemoService']
