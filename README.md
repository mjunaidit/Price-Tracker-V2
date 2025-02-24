# Price Monitor

This project monitors multiple products' prices on websites and tracks their price histories. It can send email notifications when prices change.

## Setup

1. Fork or clone this repository
2. Set up the following repository secrets:
   - `SENDER_EMAIL`: Email address to send notifications from
   - `SENDER_PASSWORD`: Email password or app-specific password
   - `RECEIVER_EMAIL`: Email address to receive notifications
   - `PRODUCT_URL_1`: URL of the first product to monitor
   - `PRODUCT_URL_2`: URL of the second product to monitor
   - Add more `PRODUCT_URL_X` secrets as needed

## How it Works

- The script runs every hour via GitHub Actions
- Each product's price history is stored in its own JSON file (e.g., `price_history_product_1.json`)
- Email notifications are sent when prices change, identifying which product changed
- You can also trigger a price check manually from the Actions tab

## Files

- `monitor_example.py`: Main script that checks prices and sends notifications
- `price_monitor.py`: Core price monitoring functionality
- `.github/workflows/price_monitor.yml`: GitHub Actions workflow configuration
- `price_history_*.json`: Stores the price histories (automatically created)

## Adding More Products

To monitor additional products:
1. Add a new product entry in `monitor_example.py`
2. Add a new `PRODUCT_URL_X` secret in your repository settings
3. Add the environment variable to the workflow file

## Note

If using Gmail as your sender email, you'll need to:
1. Enable 2-factor authentication
2. Generate an App Password (use this as SENDER_PASSWORD)

## Price History

Each product's price history is stored in a separate JSON file:
- `price_history_product_1.json` for Product 1
- `price_history_product_2.json` for Product 2
- etc.

These files are automatically created and updated by the script.
