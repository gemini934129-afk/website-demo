#!/usr/bin/env python3
"""
股價更新腳本 - 定時抓取台積電(TSM)和 NVIDIA(NVDA)股價
更新到 stock_data.json，讓網站直接讀取
"""

import json
import subprocess
from datetime import datetime
import urllib.request
import urllib.error

def fetch_yahoo_finance(symbol):
    """從 Yahoo Finance 抓取股價"""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=2d"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get('chart', {}).get('result'):
                result = data['chart']['result'][0]
                meta = result['meta']
                
                current_price = meta.get('regularMarketPrice', 0)
                previous_close = meta.get('previousClose', 0)
                
                if current_price and previous_close:
                    change = current_price - previous_close
                    change_percent = (change / previous_close) * 100
                    
                    return {
                        'price': round(current_price, 2),
                        'change': round(change, 2),
                        'changePercent': round(change_percent, 2),
                        'timestamp': datetime.now().isoformat()
                    }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
    
    return None

def main():
    """主程式：抓取股價並更新檔案"""
    stocks = {
        'TSM': {
            'name': '台積電 TSMC',
            'symbol': '2330.TW / TSM'
        },
        'NVDA': {
            'name': 'NVIDIA 輝達',
            'symbol': 'NVDA'
        }
    }
    
    stock_data = {}
    
    for symbol, info in stocks.items():
        print(f"Fetching {symbol}...")
        data = fetch_yahoo_finance(symbol)
        if data:
            stock_data[symbol] = {
                **info,
                **data
            }
            print(f"  ✓ {info['name']}: ${data['price']} ({data['change']:+.2f}, {data['changePercent']:+.2f}%)")
        else:
            print(f"  ✗ Failed to fetch {symbol}")
    
    # 寫入 JSON 檔案
    output = {
        'lastUpdate': datetime.now().isoformat(),
        'stocks': stock_data
    }
    
    with open('stock_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Saved to stock_data.json")
    
    # Git 提交
    try:
        subprocess.run(['git', 'add', 'stock_data.json'], check=True)
        subprocess.run(['git', 'commit', '-m', f'Update stock prices: {datetime.now().strftime("%Y-%m-%d %H:%M")}'], check=True)
        subprocess.run(['git', 'push'], check=True)
        print("✓ Pushed to GitHub")
    except subprocess.CalledProcessError as e:
        print(f"✗ Git error: {e}")

if __name__ == '__main__':
    main()
