import threading
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import unittest
from datetime import datetime

# Dummy data detching 
def fetch_stock_data(stock_symbol):
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{stock_symbol}?period1=0&period2=9999999999&interval=1d&events=history"
    response = requests.get(url)
    if response.status_code == 200:
        data = pd.read_csv(pd.compat.StringIO(response.text))
        print(f"Data fetched for {stock_symbol}")
        return data
    else:
        print(f"Failed to fetch data for {stock_symbol}")
        return None

# Function to process stock data
def process_stock_data(data):
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    data['Moving Average'] = data['Close'].rolling(window=20).mean()
    data.dropna(inplace=True)
    return data

# Function to visualize stock data
def visualize_stock_data(stock_symbol, data):
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label=f'{stock_symbol} Close Price')
    plt.plot(data['Moving Average'], label='20-Day Moving Average')
    plt.title(f'{stock_symbol} Stock Price and Moving Average')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()


def save_to_database(stock_symbol, data):
    conn = sqlite3.connect('stock_data.db')
    data.to_sql(stock_symbol, conn, if_exists='replace', index=True)
    conn.close()
    print(f"Data for {stock_symbol} saved to database.")

def thread_worker(stock_symbol):
    data = fetch_stock_data(stock_symbol)
    if data is not None:
        processed_data = process_stock_data(data)
        visualize_stock_data(stock_symbol, processed_data)
        save_to_database(stock_symbol, processed_data)

def fetch_and_analyze_stocks(stock_symbols):
    threads = []
    for symbol in stock_symbols:
        thread = threading.Thread(target=thread_worker, args=(symbol,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Unit tests
class TestStockAnalysis(unittest.TestCase):
    
    def test_fetch_stock_data(self):
        data = fetch_stock_data("AAPL")
        self.assertIsNotNone(data, "Failed to fetch data for AAPL.")
        self.assertIn('Date', data.columns, "Data does not have 'Date' column.")

    def test_process_stock_data(self):
        data = pd.DataFrame({
            'Date': ['2021-01-01', '2021-01-02', '2021-01-03'],
            'Close': [150, 152, 153]
        })
        processed_data = process_stock_data(data)
        self.assertIn('Moving Average', processed_data.columns, "Processed data does not have 'Moving Average' column.")
        self.assertEqual(len(processed_data), 1, "Incorrect number of rows in processed data.")

if __name__ == "__main__":
    stock_symbols = ['AAPL', 'MSFT', 'GOOG']
    fetch_and_analyze_stocks(stock_symbols)
    
    # Run unit tests
    unittest.main(argv=[''], exit=False)
