import json
from pathlib import Path


config_dir = Path(__file__).parent.resolve()

with open(config_dir / 'data/rpc.json') as file:
    RPC = json.load(file)

with open(config_dir / "accounts.txt", "r") as file:
    ACCOUNTS = [row.strip() for row in file]

with open(config_dir / "data/abi/omnisea/abi.json", "r") as file:
    OMNISEA_DROPS_MANAGER_ABI = json.load(file)


SAVE_SOFIA_CONTRACT = ""  # Перед запуском скрипта здесь устанавливаем адрес любой NFT-коллекции на Omnisea zkSync для минта

OMNISEA_DROPS_MANAGER_CONTRACT = "0x17a2d7a4F44d049d3659078D0f71F811053CF9DD"