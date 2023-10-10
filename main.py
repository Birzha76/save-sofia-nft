import asyncio
from loguru import logger

from utils.helpers import get_wallets
from utils.module import run_module, create_tasks


async def main():
    print("\n❤️ Save Sofia NFT Minter [zkSync Era]")
    print("❤️ Manual Mint - https://omnisea.org/1YzWfevRxbznt3WWTKJ1 \n")
    print("\nCost per mint 1 NFT - 0.0005 ETH (~1.3$) \n")

    nft_amount = int(input("Enter the number of Save Sofia NFTs for the mint on each account: "))

    wallets = get_wallets()
    if not len(wallets):
        return logger.error("No private wallet keys have been added to the accounts.txt file to start the NFT minting!")

    await create_tasks(wallets=wallets, nft_amount=nft_amount)

    print("Thank you for participating in the project! There is no such thing as a little help   ❤️ ")


if __name__ == "__main__":
    asyncio.run(main())