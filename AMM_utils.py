import os

from web3 import Web3, HTTPProvider
from web3.exceptions import TimeExhausted
from dotenv import load_dotenv


def AMM_connect_web3(network, apikey):
    # Mainnet #
    if network == "ethereum":
        rpc_url = "https://mainnet.infura.io/v3/" + apikey
    elif network == "polygon":
        rpc_url = "https://polygon-mainnet.infura.io/v3/" + apikey
    # Testnet #
    elif network == "sepolia":
        rpc_url = "https://sepolia.infura.io/v3/" + apikey
    elif network == "amoy":
        rpc_url = "https://polygon-amoy.infura.io/v3/" + apikey
    else:
        None
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    
    return web3


def AMM_get_contract(web3, contractAddress, contractAbi):
    file = open(contractAbi, 'r', encoding='utf-8')
    contractAddr = web3.to_checksum_address(contractAddress)
    contract = web3.eth.contract(abi=file.read(), address=contractAddr)
    
    return contract


def AMM_token_approve(web3, contract, From, From_pk, To, tokenAmount):
    From_add = web3.to_checksum_address(From)
    To_add = web3.to_checksum_address(To)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    tokenAmount = tokenAmount * 10**contract.functions.decimals().call()
    tx = contract.functions.approve(To_add, tokenAmount).build_transaction(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, From_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)
    
    return txHash, tx_receipt


def AMM_governance_token_approve(web3, contract, From, From_pk, To, token1Amount, token2Amount):
    From_add = web3.to_checksum_address(From)
    To_add = web3.to_checksum_address(To)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    value = (token1Amount + token2Amount) * 10**contract.functions.decimals().call()
    tx = contract.functions.approve(To_add, value).build_transaction(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, From_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)
    
    return txHash, tx_receipt


def AMM_add_Liquidity(web3, contract, From, From_pk, token1Contract, token1Amount, token2Contract, token2Amount, governanceTokenContract):
    From_add = web3.to_checksum_address(From)
    AMM_token_approve(web3, token1Contract, From, From_pk, contract.address, token1Amount)
    AMM_token_approve(web3, token2Contract, From, From_pk, contract.address, token2Amount)
    AMM_governance_token_approve(web3, governanceTokenContract, From, From_pk, contract.address, token1Amount, token2Amount)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    token1Amount = token1Amount * 10**contract.functions.decimals().call()
    token2Amount = token2Amount * 10**contract.functions.decimals().call()
    tx = contract.functions.addLiquidity(token1Amount, token2Amount).build_transaction(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, From_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)
    
    return txHash, tx_receipt


def AMM_remove_Liquidity(web3, contract, From, From_pk, value):
    From_add = web3.to_checksum_address(From)
    value = value * 10**contract.functions.decimals().call()
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    tx = contract.functions.removeLiquidity(value).build_transaction(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, From_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)
    
    return txHash, tx_receipt