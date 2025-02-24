# Price Monitor

This project monitors a product's price on a website and tracks its price history. It can send email notifications when prices change.

## Setup

1. Fork or clone this repository
2. Set up the following repository secrets:
   - `SENDER_EMAIL`: Email address to send notifications from
   - `SENDER_PASSWORD`: Email password or app-specific password
   - `RECEIVER_EMAIL`: Email address to receive notifications
   - `PRODUCT_URL`: URL of the product to monitor

## How it Works

- The script runs every hour via GitHub Actions
- Price history is stored in `price_history.json`
- Email notifications are sent when prices change
- You can also trigger a price check manually from the Actions tab

## Files

- `monitor_example.py`: Main script that checks prices and sends notifications
- `.github/workflows/price_monitor.yml`: GitHub Actions workflow configuration
- `price_history.json`: Stores the price history (automatically created)

## Note

If using Gmail as your sender email, you'll need to:
1. Enable 2-factor authentication
2. Generate an App Password (use this as SENDER_PASSWORD)
