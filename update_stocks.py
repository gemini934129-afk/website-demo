#!/usr/bin/env python3
"""
股價更新腳本 - 定時抓取台積電(TSM)和 NVIDIA(NVDA)股價
更新到 stock_data.json，讓網站直接讀取
"""

import json
import os
from datetime import datetime

def fetch_yfinance():
    """使用 yfinance 抓取股價"""
    try:
        import yfinance as yf
        
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
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")
            
            if len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                previous_close = hist['Close'].iloc[-2]
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100
                
                stock_data[symbol] = {
                    **info,
                    'price': round(current_price, 2),
                    'change': round(change, 2),
                    'changePercent': round(change_percent, 2),
                    'timestamp': datetime.now().isoformat()
                }
                print(f"  ✓ {info['name']}: ${stock_data[symbol]['price']} ({change:+.2f}, {change_percent:+.2f}%)")
            else:
                print(f"  ✗ No data for {symbol}")
        
        return stock_data
        
    except ImportError:
        print("Error: yfinance not installed")
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    """主程式：抓取股價並更新檔案"""
    
    stock_data = fetch_yfinance()
    
    if stock_data:
        # 寫入 JSON 檔案
        output = {
            'lastUpdate': datetime.now().isoformat(),
            'stocks': stock_data
        }
        
        with open('stock_data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Saved to stock_data.json")
    else:
        print("\n✗ Failed to update stock prices")
        # 如果抓取失敗，保持原有資料
        if os.path.exists('stock_data.json'):
            print("  Keeping existing stock_data.json")

if __name__ == '__main__':
    main()
