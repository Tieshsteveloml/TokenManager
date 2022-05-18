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


def send_token():
    try:
        addresses = get_address_from_csv(SOURCE_FILE_NAME)
        if len(addresses) <= 0:
            print("transfer_token: source address list is empty")
            return
        with open(OUTPUT_FILE_NAME, 'w', newline='') as csvfile:
            fieldnames = ['address', 'code', 'tx', 'message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in addresses:
                try:
                    res = transfer_token(item['address'], item['private'], DEST_ADDRESS, GAS_LIMIT, GAS_PRICE, CONTRACT_ADDRESS, IS_WAIT_FOR_CONFIRM)
                    writer.writerow(res)
                except Exception as e:
                    print('filter_addresses: source_private:' + item['private'] + ', message:' + res['message'] + " exception:" + str(e))
                time.sleep(SLEEP_TIME_PER_ADDRESS)
    except Exception as e:
        print("filter_addresses exception:" + str(e))


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


def transfer_token(source_address, source_private_key, dest_address, gas_limit, gas_price, contract_address, wait=False):
    result = {'address': source_address, 'code': -1, 'tx': '', 'message': ''}
    try:
        # ---------- get contract object ---------- #
        contract_addr = Web3.toChecksumAddress(contract_address)
        contract_abi = get_contract_abi(contract_address)
        contract = ETH_WEB3.eth.contract(contract_addr, abi=contract_abi)
        # ---------- check source wallet balance ---------- #
        source_balance = contract.functions.balanceOf(source_address).call()
        eth_balance = ETH_WEB3.eth.getBalance(source_address)
        print(source_address + ':transfer_token : balance:' + str(source_balance) + " eth_balance:" + str(eth_balance))
        if source_balance <= MINIMUM_BALANCE:
            result['code'] = -3
            result['message'] = 'not enough money'
            result['tx'] = ''
            return result
        wei_gas = ETH_WEB3.toWei(gas_price * gas_limit, 'gwei')

        if eth_balance < wei_gas:
            result['code'] = -4
            result['message'] = 'not enough gas'
            result['tx'] = ''
            return result
        # ---------- make transaction hash object ---------- #

        tx_hash = contract.functions.transfer(dest_address, source_balance).buildTransaction({
            'chainId': 1,
            'gasPrice': ETH_WEB3.toWei(gas_price, 'gwei'),
            'gas': gas_limit,
            'nonce': ETH_WEB3.eth.getTransactionCount(source_address),
        })

        # ---------- sign and do transaction ---------- #
        signed_txn = ETH_WEB3.eth.account.signTransaction(tx_hash, private_key=source_private_key)
        txn_hash = ETH_WEB3.eth.sendRawTransaction(signed_txn.rawTransaction)
        if wait is True:
            txn_receipt = ETH_WEB3.eth.waitForTransactionReceipt(txn_hash, ETH_LIMIT_WAIT_TIME)
            if txn_receipt is None or 'status' not in txn_receipt or txn_receipt['status'] != 1 or 'transactionIndex' not in txn_receipt:
                result['code'] = -5
                result['message'] = 'waiting failed'
                result['tx'] = txn_hash.hex()
                return result
        result['code'] = 0
        result['message'] = 'completed'
        result['tx'] = txn_hash.hex()
        return result
    except Exception as e:
        print(source_address + ":transfer_token:" + str(e))
        result['code'] = -2
        result['message'] = str(e)
        result['tx'] = ''
        return result


if __name__ == '__main__':
    send_token()
