import json
from pathlib import Path


config_dir = Path(__file__).parent.resolve()

with open(config_dir / 'data/rpc.json') as file:
    RPC = json.load(file)

with open(config_dir / "accounts.txt", "r") as file:
    ACCOUNTS = [row.strip() for row in file]

with open(config_dir / "data/abi/omnisea/abi.json", "r") as file:
    OMNISEA_DROPS_MANAGER_ABI = json.load(file)


SAVE_SOFIA_CONTRACT = "0xB28116733c37E100d3ced78C3e6D195F90759Af9"

OMNISEA_DROPS_MANAGER_CONTRACT = "0x17a2d7a4F44d049d3659078D0f71F811053CF9DD"