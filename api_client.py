import requests
import time
from config import Config
from datetime import datetime, timedelta

def fetch_stock_data(symbol: str) -> dict:
    quote_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={Config.API_KEY}"
    quote_response = requests.get(quote_url)
    quote_data = quote_response.json()
    
    profile_url = f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={Config.API_KEY}"
    profile_response = requests.get(profile_url)
    profile_data = profile_response.json()
    
    if "c" in quote_data and quote_data["c"] != 0:
        currency = profile_data.get("currency", "USD")
        
        stock_info = {
            "symbol": symbol,
            "price": float(quote_data["c"]),
            "change_percent": float(quote_data["dp"]),
            "currency": currency
        }
        return stock_info
    else:
        print(f"Błąd: Nie udało się pobrać danych dla {symbol}.")
        return None

def fetch_fundamentals(symbol: str) -> dict:
    url = f"https://finnhub.io/api/v1/stock/metric?symbol={symbol}&metric=all&token={Config.API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "metric" in data:
            m = data["metric"]
            
            fundamentals = {
                # peAnnual - Cena do Zysku (Standard Roczny)
                "C/Z": m.get("peAnnual", "Brak danych"),
                
                # pbQuarterly - Cena do Wartości Księgowej (MRQ - ostatni kwartał)
                # Fallback do pbAnnual jeśli brak danych kwartalnych
                "C/WK": m.get("pbQuarterly", m.get("pbAnnual", "Brak danych")),
                
                # psAnnual - Cena do Przychodu (Standard Roczny)
                "C/P": m.get("psAnnual", "Brak danych"),
                
                # evToEbitdaAnnual - EV/EBITDA (Standard Roczny)
                "EV/EBITDA": m.get("evToEbitdaAnnual", "Brak danych")
            }
            return fundamentals
        else:
            return None
            
    except Exception as e:
        print(f"Błąd pobierania wskaźników fundamentalnych: {e}")
        return None

def run_scanner(threshold: float = -3.0):
    top_55_symbols = [
        "AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "GOOG", "BRK-B", "LLY", "AVGO",
        "TSLA", "JPM", "WMT", "UNH", "V", "XOM", "MA", "JNJ", "PG", "HD",
        "COST", "MRK", "ABBV", "CRM", "CVX", "AMD", "NFLX", "PEP", "KO", "BAC",
        "TMO", "WFC", "LIN", "DIS", "ADBE", "MCD", "CSCO", "QCOM", "INTU", "IBM",
        "AMAT", "CAT", "DHR", "VZ", "PFE", "NOW", "BX", "GE", "TXN", "AMGN",
        "COP", "ISRG", "SPGI", "PM", "HON"
    ]
    
    print(f"\nSkanowanie {len(top_55_symbols)} największych spółek...")
    print(f"Szukam spadków poniżej {threshold}% w ostatnim tygodniu.")
    print("Skanowanie potrwa około minuty...\n")
    
    znalezione = 0
    to_time = int(time.time())
    from_time = int((datetime.now() - timedelta(days=8)).timestamp())

    for index, symbol in enumerate(top_55_symbols, 1):
        print(f"Skanowanie [{index}/{len(top_55_symbols)}]: {symbol}...     ", end="\r")
        
        # Pojedyncze zapytanie o dane historyczne dla konkretnej spółki
        url = f"https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution=D&from={from_time}&to={to_time}&token={Config.API_KEY}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if data.get("s") == "ok":
                closes = data["c"]
                if len(closes) >= 2:
                    old_price = closes[0]
                    current_price = closes[-1]
                    change_percent = ((current_price - old_price) / old_price) * 100
                    
                    if change_percent <= threshold:
                        print(f"\n[ZNALEZIONO] {symbol}: spadek o {change_percent:.2f}%")
                        znalezione += 1
                        
        except Exception:
            pass
            
        time.sleep(1.05)
        
    print(f"\nSkanowanie zakończone. Znaleziono {znalezione} spółek spełniających kryteria.")