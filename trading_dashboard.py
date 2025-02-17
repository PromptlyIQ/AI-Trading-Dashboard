from flask import Flask, render_template, jsonify
import yfinance as yf

# Initialize Flask App
dashboard = Flask(__name__)

# List of Stocks to Track
stocks = ["AAPL", "TSLA", "AMZN", "GOOGL", "META"]

# Function to Fetch Real-Time Stock Prices
def get_stock_data():
    stock_data = {}
    for stock in stocks:
        ticker = yf.Ticker(stock)
        stock_info = ticker.history(period="1d")  # Fetch latest data
        if not stock_info.empty:
            current_price = round(stock_info["Close"].iloc[-1], 2)
            predicted_move = round(ticker.info.get("fiftyDayAverage", current_price) - current_price, 2)
            stock_data[stock] = {"current_price": current_price, "predicted_move": predicted_move}
    return stock_data

# Route: Load the Dashboard
@dashboard.route('/')
def index():
    return render_template('dashboard.html')

# Route: Provide Real-Time Stock Data
@dashboard.route('/live-data')
def live_data():
    return jsonify(get_stock_data())

# Run Flask App
if __name__ == "__main__":
    dashboard.run(host="0.0.0.0", port=5000, debug=True)
