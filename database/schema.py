"""
Esquema do banco de dados
"""

SCHEMA_DEFINITIONS = {
    'wallets': '''
        CREATE TABLE IF NOT EXISTS wallets (
            address TEXT PRIMARY KEY,
            balance REAL,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''',
    'transactions': '''
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            from_address TEXT,
            to_address TEXT,
            amount REAL,
            timestamp REAL,
            block_hash TEXT,
            status TEXT,
            FOREIGN KEY(from_address) REFERENCES wallets(address),
            FOREIGN KEY(to_address) REFERENCES wallets(address)
        )
    ''',
    'blocks': '''
        CREATE TABLE IF NOT EXISTS blocks (
            hash TEXT PRIMARY KEY,
            previous_hash TEXT,
            timestamp REAL,
            nonce INTEGER,
            difficulty INTEGER,
            miner_address TEXT,
            reward REAL,
            FOREIGN KEY(miner_address) REFERENCES wallets(address)
        )
    ''',
    'compute_tasks': '''
        CREATE TABLE IF NOT EXISTS compute_tasks (
            id TEXT PRIMARY KEY,
            requester_address TEXT,
            status TEXT,
            input_data TEXT,
            result TEXT,
            created_at TIMESTAMP,
            completed_at TIMESTAMP,
            cost REAL,
            FOREIGN KEY(requester_address) REFERENCES wallets(address)
        )
    '''
}