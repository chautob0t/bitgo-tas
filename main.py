import json
from collections import defaultdict

import requests

from constants import BASE_URL, ENDPOINTS
from ancestry_helper import DFS
from logger import get_logger

log = get_logger(__file__)


class TransactionAncestrySet:
    def __init__(self, block_height, num=10):
        self.__height = block_height
        self.__num_transactions = num
        self.__hash = None
        self.__transactions = set()
        self.__transaction_info = defaultdict(dict)
        self.__ancestry_sets = defaultdict(set)

    def __get_block_hash(self):
        url = (BASE_URL + ENDPOINTS["GET_BLOCK_FROM_HEIGHT"]).replace(":height", str(self.__height))
        response = requests.get(url)
        if 200 <= response.status_code < 300:
            self.__hash = response.text
            log.info(f"Fetched block hash {self.__hash = } for {self.__height = }")
        else:
            log.error(f"Error while fetching block hash for {self.__height = }")
            raise Exception("Error while fetching block hash")

    def __get_transactions_for_block(self):
        url = (BASE_URL + ENDPOINTS["GET_BLOCK_TRANSACTIONS_ALL"]).replace(":hash", str(self.__hash))
        response = requests.get(url)
        if 200 <= response.status_code < 300:
            self.__transactions = set(response.json())
            log.info(f"Fetched all transactions IDs for block {self.__hash = }")
        else:
            log.error(f"Unable to fetch transactions for block {self.__hash = }")
            raise Exception("Error while fetching block hash")

    def __get_tx_details(self, txid):
        if txid in self.__transaction_info:
            return self.__transaction_info[txid]

        url = (BASE_URL + ENDPOINTS["GET_TRANSACTION_INFO"]).replace(":txid", str(txid))
        response = requests.get(url)
        if 200 <= response.status_code < 300:
            self.__transaction_info[txid] = response.json()
            log.debug(f"Fetched details for {txid = }")
        else:
            log.error(f"Unable to fetch details for {txid = }")
            raise Exception("Error while fetching tx details")
        return self.__transaction_info[txid]

    def __prepare_ancestry_sets(self):
        # for txid in self.__transactions:
        # Processing only 10 tx for testing/development
        for txid in list(self.__transactions)[0:10]:
            log.info(f"Processing transaction {txid = }")
            tx_info = self.__get_tx_details(txid)
            vin = tx_info.get("vin", [])
            for obj in vin:
                tx_in_id = obj.get("txid")
                if tx_in_id not in self.__transactions:
                    self.__ancestry_sets[txid].add(tx_in_id)

    def __update_ancestory_sets(self):
        # Update the related ancestors for each transaction
        # Create a graph of transactions
        # For each transaction perform DFS and keep adding the visited nodes to the ancestry set of the transaction
        # While checking that ancestors are part of the same block
        dfs = DFS(self.__transactions, self.__ancestry_sets)
        self.__ancestry_sets = dfs.find_all_ancestors()

    def __find_top_transactions(self, num_transactions):
        set_sizes = []
        for key, value in self.__ancestry_sets.items():
            set_sizes.append({"txid": key, "ancestors": len(value)})
        set_sizes.sort(key=lambda x: x.get("ancestors", 0), reverse=True)
        return set_sizes

    def get_top_transactions(self, *args, **kwargs):
        self.__get_block_hash()
        self.__get_transactions_for_block()
        self.__prepare_ancestry_sets()
        num_transactions = kwargs.get("num_transactions") if kwargs.get("num_transactions") else self.__num_transactions
        top_tx = self.__find_top_transactions(num_transactions)
        return top_tx


if __name__ == "__main__":
    block_height = 680000
    tas = TransactionAncestrySet(block_height)
    top_transactions = tas.get_top_transactions()
    log.info(json.dumps(top_transactions))
