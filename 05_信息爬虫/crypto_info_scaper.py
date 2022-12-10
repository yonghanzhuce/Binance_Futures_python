import requests

def get_funding():

    url = "https://open-api.coinglass.com/public/v2/funding"

    headers = {
        "accept": "application/json",
        "coinglassSecret": "5d5f5675abc147aaaf15633962c00f34"
    }

    response = requests.get(url, headers=headers)

    print(response.text)


def get_funding_history_usdt():
    url = "https://open-api.coinglass.com/public/v2/funding_usd_history?symbol=BTC&time_type=h8"

    headers = {
        "accept": "application/json",
        "coinglassSecret": "5d5f5675abc147aaaf15633962c00f34"
    }

    response = requests.get(url, headers=headers)

    print(response.text)


def get_funding_history_coinm():

    url = "https://open-api.coinglass.com/public/v2/funding_usd_history?symbol=BTC&time_type=h8"

    headers = {
        "accept": "application/json",
        "coinglassSecret": "5d5f5675abc147aaaf15633962c00f34"
    }

    response = requests.get(url, headers=headers)

    print(response.text)

if __name__ == "__main__":
    get_funding()
    get_funding_history_usdt()
    get_funding_history_coinm()
    
