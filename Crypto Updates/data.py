import requests
import pandas as pd
import time

# List of coins to track
coins = ['bitcoin', 'ethereum']
vs_currency = 'usd'
days = '30'  # Past 30 days

all_data = []

for coin in coins:
    url = f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart'
    params = {'vs_currency': vs_currency, 'days': days, 'interval': 'daily'}
    response = requests.get(url, params=params)
    data = response.json()

    prices = data['prices']  # [timestamp, price]
    for point in prices:
        timestamp, price = point
        all_data.append({
            'coin': coin.capitalize(),
            'date': pd.to_datetime(timestamp, unit='ms').date(),
            'price': price
        })

    time.sleep(1)  # Avoid rate limit

# Convert to DataFrame
df = pd.DataFrame(all_data)

# Optional: Daily % change
df['pct_change'] = df.groupby('coin')['price'].pct_change() * 100

# Save to CSV for Power BI
df.to_csv("live_crypto_data.csv", index=False)
print("✅ Saved as live_crypto_data.csv")
