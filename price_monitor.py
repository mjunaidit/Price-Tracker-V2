import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
import os

class PriceMonitor:
    def __init__(self, url, price_selector, email_settings=None, product_name=None):
        self.url = url
        self.price_selector = price_selector
        self.email_settings = email_settings
        # Get the page title first, fall back to provided name or URL
        self.product_name = self._get_page_title() or product_name or url
        # Create a safe filename from product name
        safe_name = self.product_name.lower()
        safe_name = ''.join(c if c.isalnum() else '_' for c in safe_name)  # Replace special chars with _
        safe_name = '_'.join(filter(None, safe_name.split('_')))  # Remove duplicate underscores
        self.history_file = f"price_history_{safe_name}.json"
        print(f"Generated filename: {self.history_file}")  # Debug print
        self.price_history = self._load_price_history()
    
    def _get_page_title(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else None
            # Clean up the title
            if title:
                title = title.strip().replace('\n', ' ').replace('\r', '')
                # Optionally truncate if too long
                if len(title) > 50:
                    title = title[:47] + "..."
            return title
        except Exception as e:
            print(f"Error fetching page title: {e}")
            return None
    
    def _load_price_history(self):
        print(f"\nAttempting to load price history from: {self.history_file}")
        try:
            with open(self.history_file, 'r') as f:
                print(f"Successfully opened {self.history_file}")
                content = f.read().strip()
                if not content:
                    print("File is empty")
                    return {}
                data = json.loads(content)
                print(f"Loaded data: {json.dumps(data, indent=2)}")
                return data
        except FileNotFoundError:
            print(f"File not found: {self.history_file}")
            return {}
        except Exception as e:
            print(f"Error loading price history for {self.product_name}: {e}")
            print(f"Error type: {type(e)}")
            return {}
    
    def _save_price_history(self):
        print(f"\nAttempting to save price history to: {self.history_file}")
        try:
            with open(self.history_file, 'w') as f:
                print(f"Writing data: {json.dumps(self.price_history, indent=2)}")
                json.dump(self.price_history, f, indent=2)
                print("Successfully saved price history")
        except Exception as e:
            print(f"Error saving price history for {self.product_name}: {e}")
            print(f"Error type: {type(e)}")
    
    def get_current_price(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            price_element = soup.select_one(self.price_selector)
            
            if price_element:
                price_text = price_element.text.strip()
                price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
                print(f"Current price: {price}")
                return price
            return None
        except Exception as e:
            print(f"Error fetching price: {e}")
            return None
    
    def send_email_notification(self, old_price, new_price):
        if not self.email_settings:
            print("No email settings provided")
            return
            
        # Check if we have all required email settings
        required_settings = ['sender_email', 'sender_password', 'receiver_email']
        for setting in required_settings:
            if not self.email_settings.get(setting):
                print(f"Missing email setting: {setting}")
                return
            
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        sender_email = self.email_settings['sender_email']
        sender_password = self.email_settings['sender_password']
        receiver_email = self.email_settings['receiver_email']

        print(f"Preparing to send email notification:")
        print(f"From: {sender_email}")
        print(f"To: {receiver_email}")
        print(f"Price change: {old_price} -> {new_price}")

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"Price Change Alert for {self.product_name}: {old_price} -> {new_price}"

        body = f"""
        Price has changed for {self.product_name}
        URL: {self.url}
        
        New price: {new_price}
        Old price: {old_price}
        
        Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        message.attach(MIMEText(body, "plain"))

        try:
            print("\nAttempting to connect to SMTP server...")
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                print("Connected. Attempting login...")
                server.login(sender_email, sender_password)
                print("Logged in. Sending message...")
                server.send_message(message)
                print("Email notification sent successfully!")
        except Exception as e:
            print(f"\nFailed to send email notification:")
            print(f"Error type: {type(e)}")
            print(f"Error message: {str(e)}")
            print("\nPlease check:")
            print("1. Gmail App Password is correct")
            print("2. Sender email is correct")
            print("3. Network connection is stable")
    
    def check_price_change(self):
        current_price = self.get_current_price()
        if current_price is None:
            return
        
        timestamp = datetime.now().isoformat()
        
        # Check if we have any history for this URL
        if self.url in self.price_history and self.price_history[self.url]:
            last_price = self.price_history[self.url][-1]['price']
            
            if last_price != current_price:
                print(f"Price changed! Previous: {last_price}, New: {current_price}")
                self.send_email_notification(last_price, current_price)
                
                # Add new price to history
                self.price_history[self.url].append({
                    'timestamp': timestamp,
                    'price': current_price
                })
                
                # Keep only last 10 entries
                if len(self.price_history[self.url]) > 10:
                    self.price_history[self.url] = self.price_history[self.url][-10:]
                
                self._save_price_history()
            else:
                print("No price change detected")
        else:
            print("First time checking this URL")
            self.price_history[self.url] = [{
                'timestamp': timestamp,
                'price': current_price
            }]
            self._save_price_history() 