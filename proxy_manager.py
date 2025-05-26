import requests
import time
import random

class ProxyManager:
    def __init__(self):
        self.current_proxy = None
        self.last_rotation = 0
        self.rotation_interval = random.randint(300, 600)  # 5-10 minutes
        
    def get_current_proxy(self):
        """Get current proxy configuration"""
        current_time = time.time()
        
        # Check if we need to rotate proxy
        if (current_time - self.last_rotation) > self.rotation_interval:
            self.rotate_proxy()
        
        return self.current_proxy
    
    def rotate_proxy(self):
        """
        Get a new proxy configuration.
        This should be customized based on your VPN's API or manual proxy list.
        """
        # For ProtonVPN, you would typically change servers via their CLI
        # This is a placeholder - implement based on your VPN solution
        print("Rotating proxy/VPN connection...")
        self.last_rotation = time.time()
        
        # Example proxy format for Selenium
        self.current_proxy = {
            'proxyType': 'manual',
            'httpProxy': None,  # Your proxy here
            'sslProxy': None,   # Your proxy here
            'noProxy': []
        }
        
    def test_connection(self, url="https://tickets.rolandgarros.com/"):
        """Test if current proxy/VPN connection works"""
        try:
            response = requests.get(url, 
                                  proxies=self.current_proxy if self.current_proxy else None,
                                  timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False 