# Indices_Lots_Calculators
Enter your entry price, stop loss price, and expected maximum loss, and it will help you calculate your lot size.

This is a Python tool designed specifically for CFD and Index traders.
It solves the biggest headaches for traders: **"Confusion over broker contract specifications"** and **"Exchange rate conversions for non-USD instruments."**

With this tool, you can accurately calculate position sizes (lots) for instruments like GER40, UK100, AUS200, and strictly control the USD risk for every trade.

## ✨ Key Features

* **Automatic Exchange Rate Conversion**: Connects to the Yahoo Finance API via `yfinance` to automatically fetch real-time exchange rates for EUR/USD, GBP/USD, and AUD/USD, calculating precise USD risk.
* **Contract Size Safety Check**: Built-in common broker specifications (e.g., DAX 1 point = €1 vs. 1 point = €25) to prevent huge losses due to incorrect contract sizes.
* **Auto-Fill Open Price**: Automatically fetches the day's open price for the index to use as default values for Entry and Stop Loss, speeding up calculations.
* **Visualized Risk Management**:
    * Real-time display of Stop Loss Distance.
    * Real-time display of Value per Pip/Point.
    * **Pro Interface**: Optimized UI layout with a distinct green calculation button.

## 🛠️ Supported Instruments

| Symbol | Index | Currency | Supported Specs |
| :--- | :--- | :--- | :--- |
| **GER40** | DAX (Germany) | EUR | Retail (1), Futures (25), Mini (10) |
| **UK100** | FTSE 100 (UK) | GBP | Retail (1), Large (10) |
| **US30** | Dow Jones (USA) | USD | Retail (1), Large (10), Special (5) |
| **EU50** | Stoxx 50 (Eurozone)| EUR | Retail (1), Futures (10) |
| **AUS200** | ASX 200 (Australia)| AUD | Retail (1), Futures (25) |
| **Custom** | Custom Instrument | Any | Manual Input |

## 🚀 Installation & Usage

It is recommended to use a Python `venv` (virtual environment) to ensure stability.

### 1. Clone Project & Create Environment
Open Git Bash or Terminal and run the following commands:

```bash
# Create virtual environment (Recommended)
python -m venv venv

# Activate virtual environment (Windows Git Bash)
source venv/Scripts/activate

# Activate virtual environment (Mac/Linux)
# source venv/bin/activate
````

### 2\. Install Dependencies

```bash
pip install -r requirements.txt
```

*If you do not have requirements.txt, you can run:*
`pip install streamlit yfinance pandas`

### 3\. Run Application

```bash
streamlit run calc.py
```

After starting, the browser will automatically open the interface (usually http://localhost:8501).

## ⚠️ Notes

1.  **Exchange Rate Latency**: Although the program fetches 1-minute charts, free APIs may have slight delays. Please use for risk estimation only.
2.  **Open Price Data**: In the first few minutes of the market opening, Yahoo Finance may not have updated the day's Open Price yet. Please enter the price manually in this case.
3.  **Environment Issues**: If you encounter a `ModuleNotFoundError`, please ensure your terminal shows `(venv)` at the beginning, indicating the virtual environment is correctly activated.
4.  **Broker Specifics**: FTMO calculates EU50 in USD. This App does not currently support this specific USD-denominated EU50 calculation.

## 📝 License

MIT License
