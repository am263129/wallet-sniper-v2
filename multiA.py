#!/usr/bin/env python3
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from typing import Optional

from cProfile import run
import requests
import json
import blocksmith
import secrets
import time



# Get Ethereum BIP44HDWallet information's from address index




running = True
while True:
  running = not running
  print(running)
  addresses = []
  privateKeys = []
  MNEMONIC1: str = generate_mnemonic(language="english", strength=128)
  MNEMONIC2: str = generate_mnemonic(language="english", strength=128)
  print(MNEMONIC1)
  print(MNEMONIC2)
  # Secret passphrase/password for mnemonic
  PASSPHRASE: Optional[str] = None  # "meherett"

  # Initialize Ethereum mainnet BIP44HDWallet
  bip44_hdwallet1: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
  bip44_hdwallet2: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
  # Get Ethereum BIP44HDWallet from mnemonic
  bip44_hdwallet1.from_mnemonic(
      mnemonic=MNEMONIC1, language="english", passphrase=PASSPHRASE
  )
  bip44_hdwallet2.from_mnemonic(
      mnemonic=MNEMONIC2, language="english", passphrase=PASSPHRASE
  )
  # Clean default BIP44 derivation indexes/paths
  bip44_hdwallet1.clean_derivation()
  bip44_hdwallet2.clean_derivation()
  for address_index in range(10):
    # Derivation from Ethereum BIP44 derivation path
    bip44_derivation: BIP44Derivation = BIP44Derivation(
        cryptocurrency=EthereumMainnet, account=0, change=False, address=address_index
    )
    # Drive Ethereum BIP44HDWallet
    bip44_hdwallet1.from_path(path=bip44_derivation)
    bip44_hdwallet2.from_path(path=bip44_derivation)
    # Print address_index, path, address and private_key
    addresses.append(bip44_hdwallet1.address())
    addresses.append(bip44_hdwallet2.address())
    privateKeys.append(bip44_hdwallet1.private_key())
    privateKeys.append(bip44_hdwallet2.private_key())
    # Clean derivation indexes/paths
    bip44_hdwallet1.clean_derivation()
    bip44_hdwallet2.clean_derivation()
  
  target = ""
  for address in addresses:
    target +=address+","
  x = requests.get(f'https://api.bscscan.com/api?module=account&action=balancemulti&address={target[:-1]}&tag=latest&apikey=$ $ $ $ apikey $ $ $ $')
  y = requests.get(f'https://api.etherscan.io/api?module=account&action=balancemulti&address={target[:-1]}&tag=latest&apikey=$ $ $ $ apikey $ $ $ $')
  z = requests.get(f'https://api.polygonscan.com/api?module=account&action=balancemulti&address={target[:-1]}&tag=latest&apikey=$ $ $ $ apikey $ $ $ $')
  bsc_result = json.loads(x.text)
  eth_result = json.loads(y.text)
  polygon_result = json.loads(z.text)
  for i in range(len(bsc_result['result'])):
    if int(bsc_result["result"][i]["balance"]) != 0 or int(eth_result["result"][i]["balance"]) != 0 or int(polygon_result["result"][i]["balance"]) != 0:
      seed = MNEMONIC1 if i % 2 == 0 else MNEMONIC2
      input_dictionary = {"seed":seed, "key" : privateKeys[i], "address" : addresses[i], "bsc_balance":bsc_result["result"][i]["balance"], "eth_balance":eth_result["result"][i]["balance"], "polygon_balance":polygon_result["result"][i]["balance"]}
      file = open("resultA.txt", "a")
      str = repr(input_dictionary)
      file.write("goal! = " + str + "\n")
      file.close()
  time.sleep(0.1)