from flask import Flask
from string import Template
import pyqrcode
import json
import config as cfg
import tools
from datetime import datetime

from web3.auto import Web3
from web3 import IPCProvider
from web3.middleware import geth_poa_middleware

app = Flask(__name__)
app.debug = True

## FUNCTIONS ###

def qrcreate(url, file):
    logging.debug("Creating QRCode")
    qr = pyqrcode.create(url, error='L', )
    with open(file, 'wb') as fstream:
        qr.png(fstream, scale=2, module_color=[76,77,159])



## ROUTES ###

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Node Notarizazion Check Service</h1>"


@app.route("/<tx>")
def transaction(tx): 

    # Contract Data
    contractAddress = "0x98Fd2757721994B9D8Ca7f22258EaE3b9bc7B156"
    contractABI = [{"anonymous": False,"inputs": [{"indexed": True,"internalType": "bytes32","name": "_filehash","type": "bytes32"},{"indexed": False,"internalType": "string","name": "_filename","type": "string"},{"indexed": False,"internalType": "string","name": "_notes","type": "string"}],"name": "logData","type": "event"},{"constant": False,"inputs": [{"internalType": "bytes32","name": "_filehash","type": "bytes32"},{"internalType": "string","name": "_filename","type": "string"},{"internalType": "string","name": "_notes","type": "string"}],"name": "doLog","outputs": [],"payable": False,"stateMutability": "nonpayable","type": "function"}]

    # Web3 Entry point to contract
    web3 = Web3(IPCProvider(cfg.web3["ipcMiddleware"]))
    # web3.middleware_stack.inject(geth_poa_middleware, layer=0)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    contract =  web3.eth.contract( address = contractAddress, abi = contractABI )
    
    # Read data from BC
    tx_receipt = web3.eth.waitForTransactionReceipt(tx)
    bl = web3.eth.getBlock(tx_receipt['blockNumber'])
    ts = bl["timestamp"]

    # Decode Data --> Encode JSON
    bdt = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    ce = contract.events.logData().processReceipt(tx_receipt)
    res = {
        'blockNumber'       : tx_receipt['blockNumber'],
        'blockHash'         : '0x'+bytes(tx_receipt['blockHash']).hex(),
        'blockDateTime'     : bdt,
        'transactionHash'   : '0x'+bytes(tx_receipt['transactionHash']).hex(),
        'sender'            : tx_receipt['from'],
        'rawData'           : tx_receipt['logs'][0]['data'],
        'data'              : {
            '_filehash'     : '0x'+ce[0]['args']['_filehash'].hex(),
            '_filename'     : ce[0]['args']['_filename'],
            '_notes'        : ce[0]['args']['_notes']
        }            
    }

    return res

    with open(cfg.templates['pageTemplate1'], 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()

    # Create qrcode
    tmp=cfg.paths['qrtmp']+'/'+tx+'.png'
    qrcreate(request.url, tmp)
    
    pageTemplate = Template(template_file_content)
    values = json.loads(evRecord[2], strict=False)
    values["receiver"] =  evRecord[1]
    values["site"] = cfg.urls["site"]
    values["explorer"] = cfg.urls["explorer"]
    values["docCounter"] = evRecord[0]
    values["hash"] = values["data"]["_hash"]
    values["email"] = values["data"]["_email"]
    values["storage"] = values["data"]["_storage"]

    page = pageTemplate.substitute(values)




    return page

if __name__ == "__main__":
    app.run(host='0.0.0.0')
