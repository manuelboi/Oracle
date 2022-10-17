from web3 import Web3
import asyncio
import sqlite3

# Configure Infura
w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/a2d3ce8effcf445b8fea9dad109c9150"))
if not w3.isConnected():
    raise ConnectionError("La connessione al nodo Infura è fallita")

# Contract infos
contractAddress = '0x2a15849be62b46C416e84A134c3f196B0B4850c0'
contractABI = '[ { "anonymous": false, "inputs": [ { "indexed": false, "internalType": "address", "name": "adr", "type": "address" } ], "name": "dataReadyEvent", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "internalType": "address", "name": "adr", "type": "address" } ], "name": "dataRequestEvent", "type": "event" }, { "inputs": [ { "internalType": "address", "name": "adr", "type": "address" } ], "name": "emitDataReadyEvent", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "emitDataRequestEvent", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "components": [ { "internalType": "string", "name": "name", "type": "string" }, { "internalType": "string", "name": "surname", "type": "string" }, { "components": [ { "internalType": "string", "name": "id", "type": "string" }, { "internalType": "string", "name": "studyCourse", "type": "string" }, { "internalType": "int256", "name": "completed", "type": "int256" } ], "internalType": "struct StudentCurriculum.Career[]", "name": "careers", "type": "tuple[]" } ], "internalType": "struct StudentCurriculum.Student", "name": "student", "type": "tuple" }, { "internalType": "address", "name": "adr", "type": "address" } ], "name": "setData", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "adr", "type": "address" } ], "name": "requestData", "outputs": [ { "components": [ { "internalType": "string", "name": "name", "type": "string" }, { "internalType": "string", "name": "surname", "type": "string" }, { "components": [ { "internalType": "string", "name": "id", "type": "string" }, { "internalType": "string", "name": "studyCourse", "type": "string" }, { "internalType": "int256", "name": "completed", "type": "int256" } ], "internalType": "struct StudentCurriculum.Career[]", "name": "careers", "type": "tuple[]" } ], "internalType": "struct StudentCurriculum.Student", "name": "student", "type": "tuple" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "", "type": "address" } ], "name": "students", "outputs": [ { "internalType": "string", "name": "name", "type": "string" }, { "internalType": "string", "name": "surname", "type": "string" } ], "stateMutability": "view", "type": "function" } ]'

# Wallet infos
privateKey = '2fba56769b62d9bfa52eaa77f782fabfdc4b96d2d124b142a9ca3ad511e36f34'
walletAddress = w3.eth.account.from_key(privateKey).address

# Contract instance create and link
contract = w3.eth.contract(address=contractAddress, abi=contractABI)


# Event handling
def handle_event(event):
    # Event print
    print()
    print('NUOVA RICHIESTA DI DATI')
    print("Evento:")
    print(event)

    # Get blockchain address from event
    blockchain_address = event.args['adr']

    # Initialaze database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get student data
    c.execute('SELECT ID, Nome, Cognome FROM Studenti WHERE Studenti.IndirizzoBlockchain = ?', (blockchain_address,))
    student_data = c.fetchone()

    # Student data organization
    ID = student_data[0]
    name = student_data[1]
    surname = student_data[2]

    # Get careers data
    c.execute('SELECT Matricola, CorsoDiStudio, Completata FROM Carriere WHERE Carriere.StudenteID = ?', (ID,))
    careers_data = c.fetchall()

    # Close database connection
    conn.commit()
    conn.close()

    data = (name, surname, careers_data)

    # Transaction to set data
    nonce = w3.eth.getTransactionCount(walletAddress)
    # Build transaction
    transaction = contract.functions.setData(data, blockchain_address).buildTransaction(
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
