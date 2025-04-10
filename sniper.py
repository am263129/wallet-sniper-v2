from mnemonic import Mnemonic
from bip_utils import (
    Bip39SeedGenerator,    # Converts mnemonic to seed bytes
    Bip44,
    Bip44Coins,
    Bip44Changes,
)
import json
from urllib import request
from cProfile import run
import requests
import json
import blocksmith
import secrets
import time

url = "https://api.mainnet-beta.solana.com"
headers = {
    "Content-Type": "application/json"
}

class Address:
    def __init__(self, sol: str, eth: str, seed: str):
        self.sol = sol
        self.eth = eth
        self.seed = seed


def generate_address():
    mnemo = Mnemonic("english")
    seed_phrase_12 = mnemo.generate(strength=128)
    seed_bytes = Bip39SeedGenerator(seed_phrase_12).Generate()
    bip44_mst_sol = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA)
    bip44_mst_eth = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
    bip44_acc_sol = (
        bip44_mst_sol
        .Purpose()             # 44'
        .Coin()                # 501' (Solana)
        .Account(0)            # 0'
        .Change(Bip44Changes.CHAIN_EXT)  # 0'
        .AddressIndex(0)       # final /0
    )
    bip44_acc_eth = (
        bip44_mst_eth
        .Purpose()            # 44'
        .Coin()               # 60' (Ethereum)
        .Account(0)           # 0'
        .Change(Bip44Changes.CHAIN_EXT)  # 0
        .AddressIndex(0)      # 0
    )
    eth_address = bip44_acc_eth.PublicKey().ToAddress()
    sol_address = bip44_acc_sol.PublicKey().ToAddress()
    address = Address(eth = eth_address, sol=sol_address, seed=seed_phrase_12)
    return address

if __name__ == "__main__":
    running = True
    while True:
        running = not running
        print(running)
        addresses = []
        sol_addresses = []
        target = ""
        for address_index in range(10):
            address = generate_address()
            addresses.append(address)
            sol_addresses.append(address.sol)
            target +=address.eth+","

        try:
            x = requests.get(f'https://api.bscscan.com/api?module=account&action=balancemulti&address={target[:-1]}&tag=latest&apikey=apikey')
            y = requests.get(f'https://api.etherscan.io/api?module=account&action=balancemulti&address={target[:-1]}&tag=latest&apikey=apikey')
            z = requests.get(f'https://api.polygonscan.com/api?module=account&action=balancemulti&address={target[:-1]}&tag=latest&apikey=apikey')
            bsc_result = json.loads(x.text)
            eth_result = json.loads(y.text)
            polygon_result = json.loads(z.text)
            for i in range(len(bsc_result['result'])):
                if int(bsc_result["result"][i]["balance"]) != 0 or int(eth_result["result"][i]["balance"]) != 0 or int(polygon_result["result"][i]["balance"]) != 0:
                    print("OMG")
                    input_dictionary = {"seed":addresses[i].seed, "address" : addresses[i].eth, "bsc_balance":bsc_result["result"][i]["balance"], "eth_balance":eth_result["result"][i]["balance"], "polygon_balance":polygon_result["result"][i]["balance"]}
                    file = open("resultA.txt", "a")
                    str = repr(input_dictionary)
                    file.write("goal! = " + str + "\n")
                    file.close()
            payload = {
                "jsonrpc": "2.0", "id": 1,
                "method": "getMultipleAccounts",
                "params": [
                    sol_addresses,
                    {
                        "encoding": "base58"
                    }
                ]
            }
            data_bytes = json.dumps(payload).encode("utf-8")
            req = request.Request(url, data=data_bytes, headers=headers, method="POST")
            with request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                value_list = result.get("result").get("value")
                for i, item in enumerate(value_list):
                    if item is not None:
                        print("OMG")
                        input_dictionary = {"seed":addresses[i].seed, "address" : addresses[i].sol}
                        print(f"Non-null item found at index {i}:{input_dictionary}")
                        file = open("resultA.txt", "a")
                        str = repr(input_dictionary)
                        file.write("goal! = " + str + "\n")
                        file.close()

        except Exception as e:
            print("request error",e)
        time.sleep(1)
        