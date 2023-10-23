from loguru import logger
import random
import time
from typing import Union

from config import OMNISEA_DROPS_MANAGER_CONTRACT, OMNISEA_DROPS_MANAGER_ABI, SAVE_SOFIA_CONTRACT
from settings import NFT_PRICE
from utils.gas_checker import check_gas
from utils.helpers import retry, check_mint_date
from .account import Account


class Omnisea(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="zksync")

        self.contract = self.get_contract(OMNISEA_DROPS_MANAGER_CONTRACT, OMNISEA_DROPS_MANAGER_ABI)

    async def get_tx_data(self):
        tx = {
            "chainId": await self.w3.eth.chain_id,
            "from": self.address,
            "gasPrice": await self.w3.eth.gas_price,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
        }
        return tx

    async def get_fee(self):
        return await self.contract.functions.fixedFee().call()

    @retry
    @check_gas
    async def mint(self, amount: int):
        logger.info(f"[{self.account_id}][{self.address}] Mint Save Sofia NFT on Omnisea")

        tx = await self.get_tx_data()

        nft_cost_in_wei = self.w3.to_wei(NFT_PRICE, "ether") * amount
        omnisea_mint_fee = await self.get_fee()

        tx.update({
            "value": nft_cost_in_wei + omnisea_mint_fee
        })

        transaction = await self.contract.functions.mint([
            SAVE_SOFIA_CONTRACT,
            amount,
            [],
            1
        ]).build_transaction(tx)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

        logger.success(f"[{self.account_id}][{self.address}] Mint Save Sofia NFT Success")
