from web3 import Web3
import time
from datetime import datetime
import random
import os
from dotenv import load_dotenv

load_dotenv()

SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
TEA_SEPOLIA_RPC = os.getenv("TEA_SEPOLIA_RPC")

RECEIVER_ADDRESSES = os.getenv("RECEIVER_ADDRESSES").split(',')

TRANSFER_AMOUNT = 0.0001  # TEA
INTERVAL_SECONDS = 6
GAS_LIMIT = 21000

w3 = Web3(Web3.HTTPProvider(TEA_SEPOLIA_RPC, request_kwargs={'timeout': 60}))

def send_tea_transfer():
    try:
        sender = Web3.to_checksum_address(SENDER_ADDRESS)
        receiver = Web3.to_checksum_address(random.choice(RECEIVER_ADDRESSES))

        nonce = w3.eth.get_transaction_count(sender)
        gas_price = w3.to_wei(3000, 'gwei')

        tx = {
            'nonce': nonce,
            'to': receiver,
            'value': w3.to_wei(TRANSFER_AMOUNT, 'ether'),
            'gas': GAS_LIMIT,
            'gasPrice': gas_price,
            'chainId': w3.eth.chain_id
        }

        gas_cost = w3.from_wei(tx['gasPrice'] * tx['gas'], 'ether')
        print(f"[i] Biaya gas estimasi: {gas_cost:.8f} TEA ke {receiver}")

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        return tx_hash.hex()

    except Exception as e:
        print(f"[!] Gagal transfer: {str(e)}")
        return None

def auto_transfer():
    counter = 1
    while True:
        print(f"\n=== Transfer #{counter} === {datetime.now().strftime('%H:%M:%S')}")
        try:
            if not w3.is_connected():
                raise ConnectionError("Tidak terhubung ke jaringan")

            balance = w3.from_wei(w3.eth.get_balance(SENDER_ADDRESS), 'ether')
            print(f"Saldo: {balance:.6f} TEA")

            tx_hash = send_tea_transfer()
            if tx_hash:
                print(f"✅ Transfer berhasil! Hash: {tx_hash}")
            else:
                print("❌ Gagal transfer, coba lagi nanti.")

        except Exception as e:
            print(f"[!] Error utama: {str(e)}")

        time.sleep(INTERVAL_SECONDS)
        counter += 1

print("=== Auto Transfer TEA Sepolia ===")
if w3.is_connected():
    print(f"Terhubung ke Chain ID: {w3.eth.chain_id}")
    auto_transfer()
else:
    print("Gagal koneksi ke jaringan.")
