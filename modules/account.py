import time
import random
from typing import Union

from loguru import logger
from web3 import Web3
from eth_account import Account as EthereumAccount
from web3.eth import AsyncEth
from web3.exceptions import TransactionNotFound

import asyncio

from config import RPC
from settings import GAS_MULTIPLIER
from utils.helpers import sleep


class Account:
    def __init__(self, account_id: int, private_key: str, chain: str) -> None:
        self.account_id = account_id
        self.private_key = private_key
        self.chain = chain
        self.explorer = RPC[chain]["explorer"]
        self.token = RPC[chain]["token"]

        self.w3 = Web3(
            Web3.AsyncHTTPProvider(random.choice(RPC[chain]["rpc"])),
            modules={"eth": (AsyncEth,)},
        )
        self.account = EthereumAccount.from_key(private_key)
        self.address = self.account.address

    def get_contract(self, contract_address: str, abi: str):
        contract_address = Web3.to_checksum_address(contract_address)
        contract = self.w3.eth.contract(address=contract_address, abi=abi)

        return contract

    async def wait_until_tx_finished(self, hash: str, max_wait_time=180):
        start_time = time.time()
        while True:
            try:
                receipts = await self.w3.eth.get_transaction_receipt(hash)
                status = receipts.get("status")
                if status == 1:
                    logger.success(f"[{self.account_id}][{self.address}] {self.explorer}{hash} successfully!")
                    return True
                elif status is None:
                    time.sleep(0.3)
                else:
                    logger.error(f"[{self.account_id}][{self.address}] {self.explorer}{hash} transaction failed!")
                    return False
            except TransactionNotFound:
                if time.time() - start_time > max_wait_time:
                    print(f'FAILED TX: {hash}')
                    return False
                await asyncio.sleep(1)

    async def sign(self, transaction):
        gas = await self.w3.eth.estimate_gas(transaction)
        gas = int(gas * GAS_MULTIPLIER)

        transaction.update({"gas": gas})

        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)

        return signed_txn

    async def send_raw_transaction(self, signed_txn):
        txn_hash = await self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return txn_hash
