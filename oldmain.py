import requests
from bitcoin import *
from colorama import Fore, Back, Style,init
init(autoreset=True)

#from webserver import keep_alive
import datetime
import json
from functools import *
from os.path import exists

SATOSHIS_PER_BTC = 1e+8
# using now() to get current time
current_time = datetime.datetime.now()
vasia = 0
winners = {}
winners_json = "winners.json"
winners_text = "winners.txt"

# read in any saved winners from previous runs
if exists(winners_json):
    with open(winners_json, 'r') as openfile:
        winners = json.load(openfile)
        print("Loading " + str(len(winners)) + " winners.")


@lru_cache(maxsize=1000000)

def check(address):

    try:
        response = requests.get(
          f"https://blockchain.info/balance?active={address}")
        final_balance = response.json()[address]["final_balance"]
        total_received = response.json()[address]["total_received"]
    except: 
        print("\nweb request failure.")
        return

    if ("invalid address" in response.text):
        print(Fore.RED + "\n[" + str(vasia) + "] " + address)
        return

    # reversed the order of the if stmt and color coded
    # the output to YELLOW on winner
    
    if final_balance / SATOSHIS_PER_BTC <= 0.0:
        print(Fore.RED + "\r[" + str(vasia) + "] " + address, end = "")
        return

    # we have a winner
    print(Style.RESET_ALL)
    print(Fore.GREEN + "\n[" + str(vasia) + "] " + address)

    # add to the a dictionary of winners
    winners[str(address)] = {
        "priv_key": str(priv_key),
        "pub_key": str(pub_key),
        "address": str(address),
        "final_balance": str(final_balance/SATOSHIS_PER_BTC),
        "total_received": str(total_received/SATOSHIS_PER_BTC),
        "updated": str(current_time)
    }

    # this will overwrite the contents every time
    # with all winners data.
    with open(winners_json, "w") as outfile:
        json.dump(winners, outfile, indent=4)

    # this will write to the text file
    with open(winners_text, 'a') as file:
        file.write("==================")
        file.write("\n")
        file.write("private key --  " + priv_key)
        file.write("\n")
        file.write("public key --  " + str(pub_key))
        file.write("\n")
        file.write("address --  " + str(addressBTC))
        file.write("\n")
        file.write("amount --  " + str(final_balance / SATOSHIS_PER_BTC))
        file.write("\n")
        file.write("==================")


#keep_alive()
    
      
while True:
    # we need a valid range of high/low priv_keys
    # so we don't waste time on impossible keys
    priv_key = random_key()
    pub_key = privtopub(priv_key)
    addressBTC = pubtoaddr(pub_key)
    check(addressBTC)
    vasia = vasia + 1
