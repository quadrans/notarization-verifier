web3 = {
    "provider"          : "http://127.0.0.1:8545",
    "ipcMiddleware"     : "/home/quadrans/.quadrans/geth.ipc",

    "contractAddress"   : "0x8258f4dea122619198ab9c8a42e7e882cb148396",
    "contractABI"       : [{"constant": False,"inputs": [{"name": "_hash","type": "bytes32"},{"name": "_email","type": "string"},{"name": "_storage","type": "string"}],"name": "doLog","outputs": [],"payable": False,"stateMutability": "nonpayable","type": "function"},{"inputs": [],"payable": False,"stateMutability": "nonpayable","type": "constructor"},{"anonymous": False,"inputs": [{"indexed": True,"name": "_hash","type": "bytes32"},{"indexed": False,"name": "_email","type": "string"},{"indexed": False,"name": "_storage","type": "string"}],"name": "logData","type": "event"}],
}

templates = {
    "pageTemplate1"     : "/var/www/qrscan/templates/page_template.html",
    "plainTemplate1"    : "/home/emcy/Dev/Contracts/SimpleTimestampingService/templates/email_template.txt",
    "pdfTemplate1"      : "/home/emcy/Dev/Contracts/SimpleTimestampingService/templates/pdf_template.html",
    "htmlTemplate1"     : "/home/emcy/Dev/Contracts/SimpleTimestampingService/templates/email_template.html",
}

paths = {
    "qrtmp"             : "/var/www/node/tmp",
}

resources = {
    "pdfTmp"            : "/home/emcy/Dev/Contracts/SimpleTimestampingService/pdf_tmp",
    "bgImage"           : "/home/emcy/Dev/Contracts/SimpleTimestampingService/img/background.jpeg"
}

urls = {
    "site"              : "https://quadrans.io/",
    "explorer"          : "https://explorer.quadrans.io",
    "notaryPage"        : "https://notarize.quadrans.io",
    "nodePage"            : "https://notarize.quadrans.io/node",
}
