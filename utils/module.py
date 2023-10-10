import asyncio
import random

from modules.omnisea import Omnisea
from utils.helpers import sleep
from settings import START_SLEEP_FROM, START_SLEEP_TO


async def create_tasks(wallets: list, nft_amount: int):
    tasks = []
    for wallet in wallets:
        tasks.append(
            asyncio.create_task(run_module(account_id=wallet["id"], private_key=wallet["key"], nft_amount=nft_amount))
        )

    await asyncio.gather(*tasks)


async def run_module(account_id: int, private_key: str, nft_amount: int):
    await sleep(START_SLEEP_FROM, START_SLEEP_TO)

    nft = Omnisea(account_id, private_key)
    await nft.mint(nft_amount)