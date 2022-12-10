import os
if(os.path.exists("binance_f/privateconfig.py")):
    from binance_f.privateconfig import *
    g_api_key = p_api_key
    g_secret_key = p_secret_key
else:
    g_api_key = "yTs6XP8Z8DAA1qWfXv3HOwFFEQ3C2A4KEcMpRECsh66KEdkdpBydztifOjH2kGi3"
    g_secret_key = "klO3fDwZpApgEU67rapOSHOqbSWrEVZ60WkVeAF4vvk9RQAKOLUHquAKODJtqhNE"

g_account_id = 12345678



