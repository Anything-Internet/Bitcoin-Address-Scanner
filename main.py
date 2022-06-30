import datetime
import time
import asyncio
from colorama import Fore, Back, Style, init
import btcscan

max_iterations = 1000
concurrent_scanners = 5
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
        balance = '{0:.6f}'.format(float(scanner[0].final_balance/scanner[0].SATOSHIS_PER_BTC))
        
        short_address = scanner[0].address[0:5] + "..."
        print(f"{Fore.WHITE}[0][{scanner[0].get_scan_counter()}] WINNER account: {short_address} Bal: {balance}", end="\n")

        
# this needs to be asynchronous
async def scan_next(cnt):
    instance = scanner[cnt]
    success = instance.scan_random()
    short_address = instance.address[0:5] + "..."

    if success < 0:
        print(f"{Fore.RED}[{cnt}][{instance.get_scan_counter()}] ERROR checking: {short_address}", end="\n")
    elif success == 0:
        print(f"{Fore.BLUE}[{cnt}][{instance.get_scan_counter()}] EMPTY account: {short_address}", end="\r")
    else:
        balance = '{0:.6f}'.format(float(instance.final_balance/instance.SATOSHIS_PER_BTC))
        print(f"{Fore.WHITE}[{cnt}][{instance.get_scan_counter()}] WINNER account: {short_address} Bal: {balance}", end="\n")

# main loop / needs to support asynchronous


async def main():
    start = datetime.datetime.now()
    print(f"{Fore.WHITE}started at {time.strftime('%X')}")

    # run short sample and time it
    for i in range(max_iterations):
    #while True:
        tasks = []
        for cnt in range(len(scanner)):
            tasks.append(asyncio.create_task(scan_next(cnt)))
            
        for cnt in range(len(scanner)):
            await tasks[cnt]
    
    stop = datetime.datetime.now()
    print(f"\n{Fore.WHITE}finished: {(stop-start)/concurrent_scanners} secs per instance")



asyncio.run(main())

