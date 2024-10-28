import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def scrape_data():
    # Scrape EUR/INR data from Yahoo Finance
    data = yf.download('EURINR=X', start='2023-01-01', end='2024-09-30')
    return data

def technical_analysis(data):
    # Calculate Moving Average
    data['1D_MA'] = data['Close'].rolling(window=1).mean()
    data['1W_MA'] = data['Close'].rolling(window=7).mean()

    # Calculate Bollinger Bands
    data['1D_BB_Upper'] = data['1D_MA'] + 2 * data['Close'].rolling(window=1).std()
    data['1D_BB_Lower'] = data['1D_MA'] - 2 * data['Close'].rolling(window=1).std()
    data['1W_BB_Upper'] = data['1W_MA'] + 2 * data['Close'].rolling(window=7).std()
    data['1W_BB_Lower'] = data['1W_MA'] - 2 * data['Close'].rolling(window=7).std()

    # Calculate CCI
    def CCI(data, ndays):
        TP = (data['High'] + data['Low'] + data['Close']) / 3
        CCI = (TP - TP.rolling(window=ndays).mean()) / (0.015 * TP.rolling(window=ndays).std())
        return CCI
    data['1D_CCI'] = CCI(data, 1)
    data['1W_CCI'] = CCI(data, 7)

    return data

def decision_making(data):
    # Decision Making Based on Indicators
    decisions = {}
    
    # Simple rules for demonstration purposes
    if data['1D_MA'][-1] > data['Close'][-1]:
        decisions['1D_MA'] = 'BUY'
    else:
        decisions['1D_MA'] = 'SELL'
    
    if data['1W_MA'][-1] > data['Close'][-1]:
        decisions['1W_MA'] = 'BUY'
    else:
        decisions['1W_MA'] = 'SELL'
    
    if data['1D_CCI'][-1] < -100:
        decisions['1D_CCI'] = 'BUY'
    elif data['1D_CCI'][-1] > 100:
        decisions['1D_CCI'] = 'SELL'
    else:
        decisions['1D_CCI'] = 'NEUTRAL'
    
    if data['1W_CCI'][-1] < -100:
        decisions['1W_CCI'] = 'BUY'
    elif data['1W_CCI'][-1] > 100:
        decisions['1W_CCI'] = 'SELL'
    else:
        decisions['1W_CCI'] = 'NEUTRAL'

    return decisions

# Run the analysis
data = scrape_data()
analyzed_data = technical_analysis(data)
decisions = decision_making(analyzed_data)

# Print decisions
print(decisions)
