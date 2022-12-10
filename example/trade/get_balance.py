from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *

g_api_key = "yTs6XP8Z8DAA1qWfXv3HOwFFEQ3C2A4KEcMpRECsh66KEdkdpBydztifOjH2kGi3"
g_secret_key = "klO3fDwZpApgEU67rapOSHOqbSWrEVZ60WkVeAF4vvk9RQAKOLUHquAKODJtqhNE"

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
result = request_client.get_balance()
PrintMix.print_data(result)
