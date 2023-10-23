import asyncio
from tqdm import tqdm
from loguru import logger

import time
import random
from datetime import datetime

from config import ACCOUNTS
from settings import RANDOM_WALLET, RETRY_COUNT


async def sleep(sleep_from: int, sleep_to: int):
    delay = random.randint(sleep_from, sleep_to)
    with tqdm(
            total=delay,
            desc="💤 Sleep",
            bar_format="{desc}: |{bar:20}| {percentage:.0f}% | {n_fmt}/{total_fmt}",
            colour="green"
    ) as pbar:
        for _ in range(delay):
            await asyncio.sleep(1)
            pbar.update(1)


def retry(func):
    async def wrapper(*args, **kwargs):
        retries = 0
        while retries <= RETRY_COUNT:
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Error | {e}")
                await sleep(10, 20)
                retries += 1
    return wrapper


def get_wallets():
    wallets = [
        {
            "id": _id,
            "key": key
        } for _id, key in enumerate(ACCOUNTS, start=1)
    ]

    if RANDOM_WALLET: random.shuffle(wallets)

    return wallets