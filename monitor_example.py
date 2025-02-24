import os
from price_monitor import PriceMonitor
import time

def main():
    # Get settings from environment variables
    url = os.getenv('PRODUCT_URL')
    price_selector = ".tracker"
    
    email_settings = {
        'sender_email': os.getenv('SENDER_EMAIL'),
        'sender_password': os.getenv('SENDER_PASSWORD'),
        'receiver_email': os.getenv('RECEIVER_EMAIL')
    }
    
    monitor = PriceMonitor(url, price_selector, email_settings)
    
    # For GitHub Actions, we'll just do one check instead of running continuously
    print(f"Checking price for {url}...")
    monitor.check_price_change()

if __name__ == "__main__":
    main() 