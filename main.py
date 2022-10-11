from web3 import Web3
import asyncio

# Configure Infura
w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/a2d3ce8effcf445b8fea9dad109c9150"))
if not w3.isConnected():
    raise ConnectionError("La connessione al nodo Infura è fallita")

# Contract infos
contractAddress = ''
contractABI = ''

# Wallet infos
walletAddress = '0x2f2a3bE0f87D2EC706576b457b527eBF1E38d168'
privateKey = '2fba56769b62d9bfa52eaa77f782fabfdc4b96d2d124b142a9ca3ad511e36f34'
nonce = w3.eth.getTransactionCount(walletAddress)

# Contract instance create and link
contract = w3.eth.contract(address=contractAddress, abi=contractABI)


# Event handling
def handle_event(event):
    blockchainAddress = event['adr']

    # Build transaction
    transaction = contract.functions.setInformation(STUDENTDATA).buildTransaction(
        {"chainId": 5, "from": walletAddress, "nonce": nonce})

    # Sign transaction
    signedTransaction = w3.eth.account.sign_transaction(transaction, private_key=privateKey)

    # Send transaction
    w3.eth.send_raw_transaction(signedTransaction.rawTransaction)


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
