
BASE_URL  = "https://blockstream.info/api"
ENDPOINTS = {
    "GET_BLOCK_FROM_HEIGHT": "/block-height/:height",
    "GET_BLOCK_TRANSACTIONS_PAGINATED": "/block/:hash/txs/:start_index",
    "GET_BLOCK_TRANSACTIONS_ALL": "/block/:hash/txids",
    "GET_TRANSACTION_INFO": "/tx/:txid"
}