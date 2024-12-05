"""
Repositório para operações no MongoDB
"""
from .mongodb_config import get_database, get_collections
from .models.wallet import WalletModel
from .models.transaction import TransactionModel
from .models.block import BlockModel
from .models.miner import MinerModel
from .models.developer import DeveloperModel

class BlockchainRepository:
    def __init__(self):
        self.db = get_database()
        self.collections = get_collections(self.db)

    # Operações de Wallet
    def create_wallet(self, address: str, name: str):
        wallet = WalletModel.create(address, name)
        return self.collections['wallets'].insert_one(wallet)

    def get_wallet(self, address: str):
        return self.collections['wallets'].find_one({'address': address})

    def update_wallet_balance(self, address: str, amount: float):
        wallet = self.get_wallet(address)
        if wallet:
            updated_wallet = WalletModel.update_balance(wallet, amount)
            self.collections['wallets'].update_one(
                {'address': address},
                {'$set': updated_wallet}
            )
            return True
        return False

    # Operações de Transação
    def add_transaction(self, from_address: str, to_address: str, amount: float):
        transaction = TransactionModel.create(from_address, to_address, amount)
        return self.collections['transactions'].insert_one(transaction)

    def get_pending_transactions(self):
        return list(self.collections['transactions'].find({'status': 'pending'}))

    # Operações de Bloco
    def add_block(self, block_data: dict):
        block = BlockModel.create(**block_data)
        return self.collections['blocks'].insert_one(block)

    def get_latest_block(self):
        return self.collections['blocks'].find_one(
            sort=[('timestamp', -1)]
        )

    # Operações de Minerador
    def register_miner(self, wallet_address: str):
        miner = MinerModel.create(wallet_address)
        return self.collections['miners'].insert_one(miner)

    def update_miner_activity(self, wallet_address: str, reward: float):
        miner = self.collections['miners'].find_one({'wallet_address': wallet_address})
        if miner:
            updated_miner = MinerModel.update_mining(miner, reward)
            self.collections['miners'].update_one(
                {'wallet_address': wallet_address},
                {'$set': updated_miner}
            )
            return True
        return False

    # Operações de Desenvolvedor
    def register_developer(self, wallet_address: str, api_key: str):
        developer = DeveloperModel.create(wallet_address, api_key)
        return self.collections['developers'].insert_one(developer)

    def get_developer(self, api_key: str):
        return self.collections['developers'].find_one({'api_key': api_key})