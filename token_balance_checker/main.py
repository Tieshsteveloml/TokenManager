import time
import requests
from constant import *
import csv
import json


def get_address_from_csv(filename):
    result = []
    try:
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                    continue
                else:
                    address = {'address': row[0], 'private': row[1]}
                    result.append(address)
                    line_count += 1
    except Exception as e:
        print("get_address_from_csv exception: " + str(e))
    return result


def filter_addresses():
    try:
        addresses = get_address_from_csv(SOURCE_FILE_NAME)
        if len(addresses) <= 0:
            print("filter_addresses: source address list is empty")
            return
        with open(OUTPUT_FILE_NAME, 'w', newline='') as csvfile:
            fieldnames = ['address', 'private', 'balance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in addresses:
                balance = 0
                try:
                    balance = get_token_balance(item['address'], CONTRACT_ADDRESS)
                    if balance <= MINIMUM_BALANCE:
                        time.sleep(SLEEP_TIME_PER_ADDRESS)
                        continue
                    writer.writerow({'address': item['address'], 'private': item['private'], 'balance': balance})
                except Exception as e:
                    print('filter_addresses: source_private:' + item['private'] + ', amount:' + str(
                            balance) + " exception:" + str(e))
                time.sleep(SLEEP_TIME_PER_ADDRESS)
    except Exception as e:
        print("filter_addresses exception:" + str(e))


def get_decimals_token(contract_address):
    try:
        if TOKEN_DECIMAL[contract_address] == 0:
            contract_addr = Web3.toChecksumAddress(contract_address)
            contract_abi = get_contract_abi(contract_address)
            contract = ETH_WEB3.eth.contract(contract_addr, abi=contract_abi)
            TOKEN_DECIMAL[contract_address] = contract.functions.decimals().call()
        return TOKEN_DECIMAL[contract_address]
    except Exception as e:
        print(contract_address + ":get_decimals_token:" + str(e))
        return TOKEN_DECIMAL[contract_address]


def get_token_balance(wallet_address, contract_address, raw=False):
    try:
        contract_abi = get_contract_abi(contract_address)
        contract_addr = Web3.toChecksumAddress(contract_address)
        contract = ETH_WEB3.eth.contract(contract_addr, abi=contract_abi)
        token_balance = contract.functions.balanceOf(ETH_WEB3.toChecksumAddress(wallet_address)).call()
        if raw is False:
            decimals = get_decimals_token(contract_address)
            token_balance = float(token_balance / pow(10, decimals))
        return token_balance
    except Exception as e:
        print(contract_address + ":get_token_balance:" + str(e))
        return 0


def get_contract_abi(contract_addr):
    while True:
        try:
            try:
                abi = ETH_CONTRACT_ABI[contract_addr]
                return abi
            except Exception as e:
                print("get_contract_abi:" + str(e))
                if USING_TEST_NET:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                    response = requests.get('%s%s' % (ABI_ENDPOINT, contract_addr), headers=headers)
                else:
                    response = requests.get('%s%s' % (ABI_ENDPOINT, contract_addr))
                response_json = response.json()
                abi_json = json.loads(response_json['result'])
                result = json.dumps(abi_json)
                ETH_CONTRACT_ABI[contract_addr] = result
                return result
        except Exception as e:
            print("get_contract_abi: contract: " + contract_addr + " " + str(e))
            time.sleep(1)


if __name__ == '__main__':
    filter_addresses()
