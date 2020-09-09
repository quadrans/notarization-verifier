from flask import Flask
from flask import request
from string import Template
import pyqrcode
import io
from datetime import datetime

from web3.auto import Web3
from web3 import IPCProvider
from web3.middleware import geth_poa_middleware

app = Flask(__name__)
app.debug = True

# Web3 Data
provider = "http://127.0.0.1:8545"
ipcMiddleware = "/home/quadrans/.quadrans/geth.ipc"

# Contract Data
contractAddress = "0x98Fd2757721994B9D8Ca7f22258EaE3b9bc7B156"
contractABI = [{"anonymous": False,"inputs": [{"indexed": True,"internalType": "bytes32","name": "_filehash","type": "bytes32"},{"indexed": False,"internalType": "string","name": "_filename","type": "string"},{"indexed": False,"internalType": "string","name": "_notes","type": "string"}],"name": "logData","type": "event"},{"constant": False,"inputs": [{"internalType": "bytes32","name": "_filehash","type": "bytes32"},{"internalType": "string","name": "_filename","type": "string"},{"internalType": "string","name": "_notes","type": "string"}],"name": "doLog","outputs": [],"payable": False,"stateMutability": "nonpayable","type": "function"}]
abiString = "[{\"anonymous\": False,\"inputs\": [{\"indexed\": True,\"internalType\": \"bytes32\",\"name\": \"_filehash\",\"type\": \"bytes32\"},{\"indexed\": False,\"internalType\": \"string\",\"name\": \"_filename\",\"type\": \"string\"},{\"indexed\": False,\"internalType\": \"string\",\"name\": \"_notes\",\"type\": \"string\"}],\"name\": \"logData\",\"type\": \"event\"},{\"constant\": False,\"inputs\": [{\"internalType\": \"bytes32\",\"name\": \"_filehash\",\"type\": \"bytes32\"},{\"internalType\": \"string\",\"name\": \"_filename\",\"type\": \"string\"},{\"internalType\": \"string\",\"name\": \"_notes\",\"type\": \"string\"}],\"name\": \"doLog\",\"outputs\": [],\"payable\": False,\"stateMutability\": \"nonpayable\",\"type\": \"function\"}]"

# Template
pageTemplate1 = "/var/www/node/templates/page_template.html"

## FUNCTIONS ###

def qrcreate(url):
    qr = pyqrcode.create(url, error='L', )
    b = io.BytesIO()
    qr.svg(b, scale=4, module_color="#4C4D9F")
    return b.getvalue().decode('utf-8')

## ROUTES ###

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Node Notarizazion Check Service</h1>"


@app.route("/abi")
def sendABI(): 
    return abiString

@app.route("/<tx>")
def transaction(tx): 

    # Web3 Entry point to contract
    web3 = Web3(IPCProvider(ipcMiddleware))
    # web3.middleware_stack.inject(geth_poa_middleware, layer=0)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    contract =  web3.eth.contract( address = contractAddress, abi = contractABI )
    
    # Read data from BC
    try:
        tx_receipt = web3.eth.getTransactionReceipt(tx)
    except :
        page = "<h1>Error</h1>"
        page += "There was an error retreivng transaction "+tx+"<br>"
        page += "the transaction was not found.<p>"
        page += "Probably you are searching in the wrong chain<br>"
        page += "Please make sure your node is running in the same network where the orginal transaction was made"
        page += "<p>"
        page += "Try to:"
        page += "<ul>"
        page += "<li><a href=\"https://explorer.quadrans.io/tx/"+tx+"\">look for the transaction in main net</a></li>"
        page += "<li><a href=\"https://explorer.testnet.quadrans.io/tx/"+tx+"\">loof for the transaction un test net</a></li>"
        page += "</ul>"
        return page

    tx_sent = web3.eth.getTransaction(tx)
    bl = web3.eth.getBlock(tx_receipt['blockNumber'])
    ts = bl["timestamp"]

    # Decode Data --> Encode JSON
    bdt = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    ce = contract.events.logData().processReceipt(tx_receipt)
    if not ce or not ce[0] or not ce[0]['args'] or not ce[0]['args']['_filehash']:
        page = "<h1>Error</h1>"
        page += "There was an error decoding the transaction "+tx+"<br>"
        page += "the transaction is not compatible with the smart contract.<p>"
        page += "Probably you submitted the wrong transaction<br>"
        return page
    
    res = {
        'blockNumber'       : tx_receipt['blockNumber'],
        'blockHash'         : '0x'+bytes(tx_receipt['blockHash']).hex(),
        'blockDateTime'     : bdt,
        'transactionHash'   : '0x'+bytes(tx_receipt['transactionHash']).hex(),
        'sender'            : tx_receipt['from'],
        'contract'          : tx_receipt['to'],
        #'rawData'           : tx_receipt['logs'][0]['data'],
        'rawData'           : tx_sent['input'],
        '_filehash'     : '0x'+ce[0]['args']['_filehash'].hex(),
        '_filename'     : ce[0]['args']['_filename'],
        '_notes'        : ce[0]['args']['_notes']
    }

    rdata =  tx_sent['input']
    rdata = rdata[2:]
    res["rawData"] = ""
    res["rawData"] += rdata[0:8]+"\n"
    rdata = rdata[8:]
    while len(rdata) >0:
        res["rawData"] += rdata[0:64]+"\n"
        rdata = rdata[64:]

    # Create qrcode
    res["qr"] = qrcreate(request.url)
    res["page"] = request.url
    
    with open(pageTemplate1, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    pageTemplate = Template(template_file_content)


    page = pageTemplate.substitute(res)
    return page

if __name__ == "__main__":
    app.run(host='0.0.0.0')
