import os
from price_monitor import PriceMonitor
import time

def main():
    # Get email settings that will be shared across all monitors
    email_settings = {
        'sender_email': os.getenv('SENDER_EMAIL'),
        'sender_password': os.getenv('SENDER_PASSWORD'),
        'receiver_email': os.getenv('RECEIVER_EMAIL')
    }
    
    # Define multiple URLs and their selectors
    products = [
        {
            'url': os.getenv('PRODUCT_URL_1'),
            'selector': '.tracker',
            'name': 'Product 1'
        },
        {
            'url': os.getenv('PRODUCT_URL_2'),
            'selector': '.tracker',
            'name': 'Product 2'
        },
        # Add more products as needed
    ]
    
    # Check each product
    for product in products:
        if not product['url']:
            print(f"Skipping {product['name']}: No URL provided")
            continue
            
        print(f"\nChecking price for {product['name']}:")
        print(f"URL: {product['url']}")
        
        monitor = PriceMonitor(
            url=product['url'],
            price_selector=product['selector'],
            email_settings=email_settings,
            product_name=product['name']  # New parameter
        )
        monitor.check_price_change()

if __name__ == "__main__":
    main() 