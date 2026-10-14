import requests

def getUSDtoPLN() -> float:
    url = "http://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json"

    try:
        response = requests.get(url)
        data = response.json()

        rate = data["rates"][0]["mid"]

        return rate 
    
    except Exception as e:
        print(f"Błąd pobierania kursu NBP (USD): {e}")
        return None

def getEURtoPLN() -> float:
    url = "http://api.nbp.pl/api/exchangerates/rates/a/eur/?format=json"

    try:
        response = requests.get(url)
        data = response.json()

        rate = data["rates"][0]["mid"]

        return rate 

    except Exception as e:
        print(f"Błąd pobierania kursu NBP (EUR): {e}")
        return None