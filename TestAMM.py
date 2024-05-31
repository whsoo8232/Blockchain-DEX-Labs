import os

from web3 import Web3, HTTPProvider
from web3.exceptions import TimeExhausted
from dotenv import load_dotenv
from AMM_utils import *

if __name__ == "__main__":
    load_dotenv(".env")

    network = "amoy"

    apikey = os.getenv("INFURA_API_KEY")
    web3 = AMM_connect_web3(network, apikey)

    account1 = os.getenv("MY_TESTMAIN")
    pk1 = os.getenv("MY_TESTMAIN_PK")
    account2 = os.getenv("MY_TESTTEST")
    pk2 = os.getenv("MY_TESTTEST_PK")

    AMMContractAddress = "0xE2a853007b3719A74e60019E7588D6613A53bac7"
    AMMAbi = "./TestAMM.abi"
    AMMContract = AMM_get_contract(web3, AMMContractAddress, AMMAbi)

    token1Address = "0x82357Fb36B13E4a5e13FB4e292fCa01260cA7E7E"
    token1Abi = "./TestAlpha.abi"
    token1Contract = AMM_get_contract(web3, token1Address, token1Abi)

    token2Address = "0xd0018302138E8fb982b44C7c008b9BC83A2C8d6a"
    token2Abi = "./TestBeta.abi"
    token2Contract = AMM_get_contract(web3, token2Address, token2Abi)

    governanceAddress = "0xBafBe8Dc6b88868A7b58F6E5df89c3054dec93bB"
    governanceAbi = "./testGovernance.abi"
    governanceContract = AMM_get_contract(web3, governanceAddress, governanceAbi)
    governanceOwner = governanceContract.functions.owner().call()

    print(governanceContract.functions.balanceOf(AMMContractAddress).call())
    print(AMMContract.functions.owner().call())
    
    
    From_add = web3.to_checksum_address(account1)
    To_add = web3.to_checksum_address(AMMContractAddress)
    nonce = web3.eth.get_transaction_count(From_add)
    value = 1
    gas_estimate = web3.eth.estimate_gas({'from': From_add, 'to': To_add, 'value': web3.to_wei(value, "ether")})
    gas_price = web3.eth.gas_price
    tx = {
            'nonce': nonce,
            'from': From_add,
            'to': To_add,
            'value': web3.to_wei(value, 'ether'),
            'gas': gas_estimate,
            "gasPrice": gas_price
        }
    sign_tx = web3.eth.account.sign_transaction(tx, pk1)
    tx_hash = web3.eth.send_raw_transaction(sign_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)
    
    
    # From_add = web3.to_checksum_address(AMMContractAddress)
    # To_add = web3.to_checksum_address(account2)
    # gas_price = web3.eth.gas_price
    # nonce = web3.eth.get_transaction_count(AMMContractAddress)
    # tokenAmount = governanceContract.functions.balanceOf(AMMContractAddress).call()
    # tx = governanceContract.functions.transferFrom(From_add, To_add, tokenAmount).build_transaction(
    #     {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
    # )
    # signed_txn = web3.eth.account.sign_transaction(tx, pk1)
    # txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    # print(tx_receipt)
    

# # add pair token number
#     token1Amount = 10000
#     token2Amount = 10000

# # addLiquidity
#     AMM_add_Liquidity(web3, AMMContract, account1, pk1, token1Contract, token1Amount, token2Contract, token2Amount, governanceContract)
    

# # removeLiquidity
#     AMM_remove_Liquidity(web3, AMMContract, account1, pk1, value)
