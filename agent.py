import yfinance as yf

# Get stock price.
# def get_stock_price(symbol):    
#     prices = {
#         "AAPL": "$150", 
#         "GOOG": "$2800", 
#         "TSLA": "$700"
#     }
#     return prices.get(symbol.upper(), "Stock symbol not found")

# Get the real price from Yahoo Finance.
def get_stock_price(symbol):    
    try:
        ticker = yf.Ticker(symbol)

        price = ticker.fast_info['last_price']
        currency = ticker.fast_info['currency']
        return f"{price:.2f} {currency}"

    except Exception:
            return "Stock symbol not found or API error."

tools_list = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get the current stock price for a given ticker symbol",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "The stock ticker (e.g. AAPL)"}
                },
                "required": ["symbol"],
            },
        },
    }
]