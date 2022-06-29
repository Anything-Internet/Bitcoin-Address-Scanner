import datetime
from colorama import Fore, Back, Style,init
import btcscan

scanner = btcscan.btcscan()

### set to TRUE to load
load_manual_addresses = False

manual_addresses = [
    {
        "address": "35bKSaLGG4AcEeRLtbn2kvzt4NK4j6j7oE", 
        "pub_key": 0, 
        "priv_key": 0
    },
    {
        "address": "3N5BjPE5rbkhRTwRKz6Eu5JyhSv4EeJeoL", 
        "pub_key": 0, 
        "priv_key": 0
    },
]


if load_manual_addresses:
    for manual in manual_addresses:
        success = scanner.scan_address(
            manual["pub_key"], manual["priv_key"], manual["address"])
    
        if success < 0:
            print(f"ERROR checking: {scanner.address}")
        elif success == 0:
            print(f"EMPTY account: {scanner.address}")
        else:
            print(f"WINNER account: {scanner.address}")
    

while True:
    current_time = datetime.datetime.now()
    success = scanner.scan_random()

    if success < 0:
        print(f"{Fore.RED}[{scanner.get_scan_counter()}] ERROR checking: {scanner.address}", end="\n")
    elif success == 0:
        print(f"{Fore.BLUE}[{scanner.get_scan_counter()}] EMPTY account: {scanner.address}", end="\r")
    else:
        print(f"{Fore.WHITE}[{scanner.get_scan_counter()}] WINNER account: {scanner.address}", end="\n")

    