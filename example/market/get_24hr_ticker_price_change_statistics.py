from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *

request_client = RequestClient(api_key="yTs6XP8Z8DAA1qWfXv3HOwFFEQ3C2A4KEcMpRECsh66KEdkdpBydztifOjH2kGi3", secret_key="klO3fDwZpApgEU67rapOSHOqbSWrEVZ60WkVeAF4vvk9RQAKOLUHquAKODJtqhNE")

result = request_client.get_ticker_price_change_statistics()
# result = request_client.get_ticker_price_change_statistics(symbol="BTCUSDT")

print("======= 24hr Ticker Price Change Statistics =======")
PrintMix.print_data(result)
print("===================================================")
