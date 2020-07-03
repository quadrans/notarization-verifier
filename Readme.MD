
# Node Notarization verifier
It's a python/flask web app that, provided a tx-hash in the url, checks the content of the transaction against the Quadrans node notarizazion smart contract (main-net only) in order to provide witha convenient way to retrieve and check notarization data
  

## Installation notes

- wsgi service must run as user quadrans, group www-data
	- quadrans : to connect to ipc socket
	- www-data : to use the webapp
  
- folder and files must be owned by user quadrans, group www-data
	- the wsgi socket might be an exception
