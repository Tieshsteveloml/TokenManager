from config import *
from web3 import Web3

ETH_GAS_MIN_LIMIT = 21000
if USING_TEST_NET:
    WEB3_ENDPOINT = "https://ropsten.infura.io/v3/" + INFURA_TOKEN
    ABI_ENDPOINT = 'https://api-goerli.etherscan.io/api?module=contract&action=getabi&address='
else:
    WEB3_ENDPOINT = "https://mainnet.infura.io/v3/" + INFURA_TOKEN
    ABI_ENDPOINT = 'https://api.etherscan.io/api?module=contract&action=getabi&address='

ETH_WEB3 = Web3(Web3.HTTPProvider(WEB3_ENDPOINT))
ETH_LIMIT_WAIT_TIME = 36000
ETH_GAS_URL = 'https://ethgasstation.info/api/ethgasAPI.json?api-key=9ba4f83d4b284ce6f0930ee643c3fbc5c84b5fce13eb1fad771877d06ee2'
ETH_CONTRACT_ABI = {}
TOKEN_DECIMAL = {CONTRACT_ADDRESS: 0}
