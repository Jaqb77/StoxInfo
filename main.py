from api_client import fetch_stock_data, fetch_fundamentals, run_scanner
from convert import getUSDtoPLN, getEURtoPLN

def check_single_stock():
    symbol = input("Podaj symbol spółki giełdowej (np. AAPL, BMW.DE): ").upper()
    print(f"Wysyłam zapytanie do API dla spółki: {symbol}...")
    
    data = fetch_stock_data(symbol)
    
    if data:
        print("\n--- Wyniki z giełdy ---")
        print(f"Spółka: {data['symbol']}")
        print(f"Cena: {data['price']} {data['currency']}")
        print(f"Zmiana: {data['change_percent']}%")
        
        waluta = data['currency']
        rate = None
        
        if waluta == 'USD':
            rate = getUSDtoPLN()
        elif waluta == 'EUR':
            rate = getEURtoPLN()
        else:
            print(f"Brak obsługi przelicznika NBP dla waluty: {waluta}")
        
        if rate is not None:
            price_pln = round(data['price'] * rate, 2)
            print(f"Cena w PLN: {price_pln} PLN (po aktualnym kursie {rate})")
            
        print("\n--- Wskaźniki Fundamentalne ---")
        fundamentals = fetch_fundamentals(symbol)
        
        if fundamentals:
            print(f"C/Z (P/E): {fundamentals['C/Z']}")
            print(f"C/WK (P/B): {fundamentals['C/WK']}")
            print(f"C/P (P/S): {fundamentals['C/P']}")
            print(f"EV/EBITDA: {fundamentals['EV/EBITDA']}")
        else:
            print("Brak dostępnych wskaźników dla tej spółki.")
            
        print("-----------------------\n")

if __name__ == "__main__":
    while True:
        print("\n=== STOXINFO MENU ===")
        print("1. Sprawdź pojedynczą spółkę")
        print("2. Skaner TOP 55 S&P 500 (spadek > 5% w tydzień)")
        print("3. Zakończ")
        
        wybor = input("Wybierz opcję (1-3): ")
        
        if wybor == '1':
            check_single_stock()
        elif wybor == '2':
            # Wywołanie funkcji skanera z pliku api_client.py
            run_scanner(-5.0)
        elif wybor == '3':
            print("Zamykanie programu...")
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")