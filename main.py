import datetime
from colorama import Fore, Back, Style, init
import btcscan

concurrent_scanners = 4
scanner = []

for cnt in range(concurrent_scanners):
    scanner.append(btcscan.btcscan(cnt))

# place any addresses to manually include
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

# load manual addresses in first instance only
for manual in manual_addresses:
    success = scanner[0].scan_address(
        manual["pub_key"], manual["priv_key"], manual["address"])
    
    if success < 0:
        print(f"[0]ERROR checking: {scanner[0].address}")
    elif success == 0:
        print(f"[0]EMPTY account: {scanner[0].address}")
    else:
        print(f"[0]WINNER account: {scanner[0].address} Bal: {scanner[0].final_balance}")

# this needs to be asynchronous
def scan_next(cnt):
    instance = scanner[cnt]
    success = instance.scan_random()

    if success < 0:
        print(f"{Fore.RED}[{cnt}][{instance.get_scan_counter()}] ERROR checking: {instance.address}", end="\n")
    elif success == 0:
        print(f"{Fore.BLUE}[{cnt}][{instance.get_scan_counter()}] EMPTY account: {instance.address}", end="\r")
    else:
        print(f"{Fore.WHITE}[{cnt}][{instance.get_scan_counter()}] WINNER account: {instance.address}", end="\n")
    

# main loop / needs to support asynchronous
while True:
    for cnt in range(len(scanner)):
        scan_next(cnt)


   