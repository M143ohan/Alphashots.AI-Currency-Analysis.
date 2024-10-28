import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def scrape_data():
    data = yf.download('EURINR=X', start='2023-01-01', end='2024-09-30')
    return data

def technical_analysis(data):
    data['1D_MA'] = data['Close'].rolling(window=1).mean()
    data['1W_MA'] = data['Close'].rolling(window=7).mean()

    data['1D_BB_Upper'] = data['1D_MA'] + 2 * data['Close'].rolling(window=1).std()
    data['1D_BB_Lower'] = data['1D_MA'] - 2 * data['Close'].rolling(window=1).std()
    data['1W_BB_Upper'] = data['1W_MA'] + 2 * data['Close'].rolling(window=7).std()
    data['1W_BB_Lower'] = data['1W_MA'] - 2 * data['Close'].rolling(window=7).std()

    def CCI(data, ndays):
        TP = (data['High'] + data['Low'] + data['Close']) / 3
        CCI = (TP - TP.rolling(window=ndays).mean()) / (0.015 * TP.rolling(window=ndays).std())
        return CCI
    data['1D_CCI'] = CCI(data, 1)
    data['1W_CCI'] = CCI(data, 7)

    return data

def plot_graphs(data):
    plt.figure(figsize=(14, 10))

    plt.subplot(3, 1, 1)
    plt.plot(data['Close'], label='Close Price')
    plt.plot(data['1D_MA'], label='1-Day Moving Average')
    plt.plot(data['1W_MA'], label='1-Week Moving Average')
    plt.title('Moving Averages')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(data['Close'], label='Close Price')
    plt.plot(data['1D_BB_Upper'], label='1-Day Bollinger Upper Band')
    plt.plot(data['1D_BB_Lower'], label='1-Day Bollinger Lower Band')
    plt.plot(data['1W_BB_Upper'], label='1-Week Bollinger Upper Band')
    plt.plot(data['1W_BB_Lower'], label='1-Week Bollinger Lower Band')
    plt.title('Bollinger Bands')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(data['1D_CCI'], label='1-Day CCI')
    plt.plot(data['1W_CCI'], label='1-Week CCI')
    plt.title('Commodity Channel Index (CCI)')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Run the analysis and plot graphs
data = scrape_data()
analyzed_data = technical_analysis(data)
plot_graphs(analyzed_data)
