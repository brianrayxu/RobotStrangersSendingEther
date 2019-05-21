from web3 import Web3, HTTPProvider, EthereumTesterProvider, middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
#from web3.auto import w3
#from solc import compile_source
from web3.contract import ConciseContract
from web3.middleware import geth_poa_middleware

import urllib.request
import requests

my_provider = Web3.IPCProvider('~/.ethereum/rinkeby/geth.ipc')
w3 = Web3(my_provider)
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

#abi can be generated from the command line with solc or online with Remix IDE
abi = '''
[
    {
        "constant": false,
        "inputs": [
            {
                "name": "_locationData",
                "type": "int256"
            }
        ],
        "name": "setLocationData",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "getLocationData",
        "outputs": [
            {
                "name": "",
                "type": "int256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "constructor"
    }
]
'''

#Contract address
address = Web3.toChecksumAddress("0x50b9ac3f74f9b8396f51121ec059ec1d47e733cb")
StoreIntegerValue = w3.eth.contract(
        address, abi=abi, ContractFactoryClass=ConciseContract)

#Account address for laptop
#laptop = '0xe90297d9D028c8233ce2b2621A3c23616e1E7a85'
metamask = '0x0D936F8e98Bb0087e3EF30DF2De1Fe2cAF22f727'
#Example function to submit data to the block chain
def submitLocationData():
        #gasEstimate = Web3.eth.estimateGas({data: bytecode})
        #gasEstimate = w3.eth.generateGasPrice()
#        gasEstimate = w3.eth.gasPrice
#        block = w3.eth.getBlock('latest')
#        print(block)
#        print(gasEstimate)
#        print("something happened")
#        w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
        #note that data must be an integer,
        
        #'gas': 1000000
        #, 'gasPrice': w3.toWei(2,'gwei')
        #'gas': 1; 'gas':4999, 'gas':5000 or more all fail
        fp = urllib.request.urlopen("http://myexternalip.com/raw")
        mybytes = fp.read()

        mystr = mybytes.decode("utf8")
        mystr = mystr.replace(".","")
        data = int(mystr)
        fp.close()
        StoreIntegerValue.setLocationData(int(data), transact={'from': metamask})
#        test_val = StoreIntegerValue.getLocationData(transcat={'from': metamask})
 #       print("Test Val= ", test_val)

        # Getting current router ID from other node
        other_node_address = "0x50b9ac3f74f9b8396f51121ec059ec1d47e733cb"
        page = requests.get("https://rinkeby.etherscan.io/address/"+other_node_address)
        content = page.content
        str_search = b"te' href='/tx/"
        str_start = content.find(str_search)
        id_start = str_start+len(str_search)
        length_of_txhash = 66
        tx_id = content[id_start:id_start+length_of_txhash].decode("utf-8")
        tx_input = w3.eth.getTransaction(tx_id).input
        other_router_hex = "0x"+tx_input[-8:]
        other_router_int = int(other_router_hex,16)
        print("Transaction Id= ", tx_id)
        print("Other Node Router IP = ", other_router_int)
        print("Current IP Address= ", data)
        if other_router_int==data:
                print("IPs Match! In proximity")
        
submitLocationData()


# Structure based on what was found here: https://ethereum.stackexchange.com/questions/38968/how-to-write-a-smart-contract-for-rpi-sensor/44691#44691
