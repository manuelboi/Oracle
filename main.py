from web3 import Web3
import asyncio
import sqlite3

# Configure Infura
w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/a2d3ce8effcf445b8fea9dad109c9150"))
if not w3.isConnected():
    raise ConnectionError("La connessione al nodo Infura è fallita")

# Contract infos
contractAddress = '0x054a49AB33d9520F03593b7c9b5abb24BbbECBA1'
contractABI = '[ { "inputs": [], "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, ' \
              '"inputs": [], "name": "dataReadyEvent", "type": "event" }, { "anonymous": false, "inputs": [ { ' \
              '"indexed": false, "internalType": "address", "name": "adr", "type": "address" } ], ' \
              '"name": "dataRequestEvent", "type": "event" }, { "inputs": [], "name": "emitDataReadyEvent", ' \
              '"outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], ' \
              '"name": "emitDataRequestEvent", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, ' \
              '{ "inputs": [ { "components": [ { "internalType": "string", "name": "id", "type": "string" }, ' \
              '{ "internalType": "string", "name": "name", "type": "string" }, { "internalType": "string", ' \
              '"name": "surname", "type": "string" } ], "internalType": "struct StudentCurriculum.Student", ' \
              '"name": "student", "type": "tuple" } ], "name": "setData", "outputs": [], "stateMutability": ' \
              '"nonpayable", "type": "function" }, { "inputs": [], "name": "requestData", "outputs": [ { ' \
              '"components": [ { "internalType": "string", "name": "id", "type": "string" }, { "internalType": ' \
              '"string", "name": "name", "type": "string" }, { "internalType": "string", "name": "surname", ' \
              '"type": "string" } ], "internalType": "struct StudentCurriculum.Student", "name": "student", ' \
              '"type": "tuple" } ], "stateMutability": "view", "type": "function" } ] '

# Wallet infos
walletAddress = '0x2f2a3bE0f87D2EC706576b457b527eBF1E38d168'
privateKey = '2fba56769b62d9bfa52eaa77f782fabfdc4b96d2d124b142a9ca3ad511e36f34'

# Contract instance create and link
contract = w3.eth.contract(address=contractAddress, abi=contractABI)


# Event handling
def handle_event(event):
    # Event print
    print('NUOVA RICHIESTA DI DATI')
    print("Evento:")
    print(event)

    # Get blockchain address from event
    blockchain_address = event.args['adr']

    # Get data from database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Studenti WHERE Studenti.IndirizzoBlockchain = ?', (blockchain_address,))
    student_data = c.fetchone()
    conn.commit()
    conn.close()

    # Data organization
    ID = student_data[0]
    name = student_data[1]
    surname = student_data[2]

    # Transaction to set data
    nonce = w3.eth.getTransactionCount(walletAddress)
    # Build transaction
    transaction = contract.functions.setData(blockchain_address, (ID, name, surname)).buildTransaction(
        {"chainId": 5, "from": walletAddress, "nonce": nonce})
    # Sign transaction
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=privateKey)
    # Send transaction
    sent_transaction = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(sent_transaction)
    print("Ricevuta transazione iniezione dati:")
    print(transaction_receipt)
    # Transaction to emit dataReadyEvent
    nonce = w3.eth.getTransactionCount(walletAddress)
    # Build transaction
    transaction = contract.functions.emitDataReadyEvent(blockchain_address).buildTransaction(
        {"chainId": 5, "from": walletAddress, "nonce": nonce})
    # Sign transaction
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=privateKey)
    # Send transaction
    sent_transaction = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(sent_transaction)
    print("Ricevuta transazione emissione evento dati pronti:")
    print(transaction_receipt)


async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)


def main():
    event_filter = contract.events.dataRequestEvent.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
    finally:
        loop.close()


if __name__ == "__main__":
    main()

# c.execute('SELECT * FROM ((Studenti JOIN Carriere ON Studenti.Matricola = Carriere.EseguitaDa) JOIN Esami ON
# Carriere.ID = Esami.Carriera) JOIN Insegnamenti ON Esami.Insegnamento = Insegnamenti.ID WHERE
# Studenti.IndirizzoBlockchain = ?', ('0x2f2a3bE0f87D2EC706576b457b527eBF1E38d168',))
