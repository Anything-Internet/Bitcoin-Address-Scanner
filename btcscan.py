import requests
from bitcoin import random_key, privtopub, pubtoaddr

import datetime
import json
from os.path import exists


class btcscan:

    # control vars
    log_everything = False
    log_to_screen = False

    SATOSHIS_PER_BTC = 1e+8
    scan_counter = 0
    total_scan_counter = 0

    file_location = "./"
    json_filename = "winners.json"
    text_filename = "winners.txt"
    log_filename = "btcscanlog.txt"
    ctr_filename = "btccounter.txt"
    prefix = ""

    json_file = file_location + json_filename
    text_file = file_location + text_filename
    log_file = file_location + log_filename
    ctr_file = file_location + "tmp/" + ctr_filename
    btc_url = "https://blockchain.info/balance?active="

    winners = {}
    scan_log = {}
    final_balance = 0.0

    #############################################
    # initialize object - not tested for multiple
    # concurrent instances

    def __init__(self, prefix=0):
        self.prefix = str(prefix)

        self.json_file = self.file_location + self.prefix + "-" + self.json_filename
        self.text_file = self.file_location + self.prefix + "-" + self.text_filename
        self.log_file = self.file_location + self.prefix + "-" + self.log_filename
        self.ctr_file = self.file_location + "tmp/" + self.prefix + "-" + self.ctr_filename

        self.get_scan_counter()

        self.log_msg(f"Initialized [{self.prefix}]")

        if exists(self.json_file):
            with open(self.json_file, 'r') as openfile:
                self.winners = json.load(openfile)

        if exists(self.text_file):
            with open(self.text_file, 'w') as openfile:
                openfile.write("")

        self.log_msg("Loading " + str(len(self.winners)) + " winners.")

        # update all winners with current data
        if len(self.winners):
            for winner in self.winners:
                w = self.winners[winner]
                self.scan_address(w["pub_key"], w["priv_key"], w["address"])

        return

    #############################################
    #
    def get_scan_counter(self):
        if self.total_scan_counter > 0:
            return self.total_scan_counter

        if not exists(self.ctr_file):
            return self.total_scan_counter

        with open(self.ctr_file, 'r') as openfile:
            x = openfile.read()
            if len(x):
                self.total_scan_counter = int(x)
            else:
                self.total_scan_counter = 1  # prevent looping

            self.log_msg(f"Resuming scans from {x}")
        return self.total_scan_counter

    def set_scan_counter(self, value):
        self.total_scan_counter = value
        with open(self.ctr_file, 'w') as openfile:
            openfile.write(str(self.total_scan_counter))

    #############################################
    # print to screen and/or file based on control
    # variables.  ALL printing goes through here.

    def log_msg(self, msg):
        current_time = datetime.datetime.now()

        self.scan_log[current_time] = msg

        if (self.log_to_screen):
            print(f"{current_time}: {msg}")

        return

    #############################################
    # generate a random key

    def scan_random(self):
        self.priv_key = random_key()
        self.pub_key = privtopub(self.priv_key)
        self.address = pubtoaddr(self.pub_key)

        return self.scan_address(self.priv_key, self.pub_key, self.address)

    #############################################
    # scan specific key - so can be used with the
    # scan_random or called with known keys

    def scan_address(self, priv_key, pub_key, address):
        self.priv_key = priv_key
        self.pub_key = pub_key
        self.address = address

        self.set_scan_counter(self.total_scan_counter + 1)
        self.scan_counter += 1

        if self.log_everything:
            self.log_msg(
                f"[{self.total_scan_counter}] Checking PrivKey: {self.priv_key} PubKey: {self.pub_key} Address: {self.address}"
            )

        success = self.check_address()

        if success < 0:
            self.log_msg("ERROR retrieving: " + self.address)

        elif success == 0:
            if self.log_everything:
                self.log_msg("EMPTY account: " + self.address)
                self.save_winners_text()

        else:
            self.log_msg("WINNER: " + self.address)
            self.save_winners_json()
            self.save_winners_text()

        return success

    #############################################
    # output current result to the json file

    def save_winners_json(self):
        current_time = datetime.datetime.now()

        # add to the a dictionary of winners
        self.winners[str(self.address)] = {
            "priv_key": str(self.priv_key),
            "pub_key": str(self.pub_key),
            "address": str(self.address),
            "final_balance": str(self.final_balance / self.SATOSHIS_PER_BTC),
            "total_received": str(self.total_received / self.SATOSHIS_PER_BTC),
            "updated": str(current_time)
        }

        # this will overwrite the contents every time
        # with all winners data.
        with open(self.json_file, "w") as outfile:
            json.dump(self.winners, outfile, indent=4)

        return

    #############################################
    # output current result to the text file

    def save_winners_text(self):

        with open(self.text_file, 'w') as file:
            for key in self.winners:
                instance = self.winners[key]

                file.write("\nupdated: " + instance["updated"])
                file.write("\nprivate key: " + instance["priv_key"])
                file.write("\npublic key: " + instance["pub_key"])
                file.write("\naddress: " + instance["address"])
                file.write("\namount: " + instance["final_balance"])
                file.write("\ntotal received: " + instance["total_received"])

                file.write("\n====================================\n")

        return

    #############################################
    # Check one address.  Return -1 on error or
    # 0 or higher for any money in account now or
    # in the past

    def check_address(self):
        url = f"{self.btc_url}{self.address}"

        try:
            self.response = requests.get(url)
            self.final_balance = self.response.json()[
                self.address]["final_balance"]
            self.total_received = self.response.json()[
                self.address]["total_received"]

        except:
            self.log_msg("web request failure.")
            return -1

        if ("invalid address" in self.response.text):
            return -1

        # valid response
        return self.total_received + self.final_balance
