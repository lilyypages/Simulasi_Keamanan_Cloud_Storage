import json
import hashlib
from datetime import datetime
from pathlib import Path


BLOCKCHAIN_FILE = "blockchain/blockchain.json"


# Create SHA-256 hash for block
def calculate_block_hash(block):

    block_string = json.dumps(
        block,
        sort_keys=True
    ).encode()

    return hashlib.sha256(block_string).hexdigest()


# Load blockchain from JSON
def load_blockchain():

    # Create file if not exists
    if not Path(BLOCKCHAIN_FILE).exists():

        with open(BLOCKCHAIN_FILE, 'w') as f:
            json.dump([], f)

    # Handle empty file
    if Path(BLOCKCHAIN_FILE).stat().st_size == 0:

        with open(BLOCKCHAIN_FILE, 'w') as f:
            json.dump([], f)

    with open(BLOCKCHAIN_FILE, 'r') as f:
        return json.load(f)


# Save blockchain to JSON
def save_blockchain(chain):

    with open(BLOCKCHAIN_FILE, 'w') as f:
        json.dump(chain, f, indent=4)


# Create genesis block
def create_genesis_block():

    chain = load_blockchain()

    # Skip if genesis already exists
    if len(chain) > 0:
        return

    genesis_block = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "file_hash": "GENESIS_BLOCK",
        "previous_hash": "0"
    }

    genesis_block["current_hash"] = calculate_block_hash(
        genesis_block
    )

    chain.append(genesis_block)

    save_blockchain(chain)

    print("[+] Genesis block created")


# Add new block
def add_block(file_hash):

    chain = load_blockchain()

    # Create genesis if blockchain empty
    if len(chain) == 0:
        create_genesis_block()
        chain = load_blockchain()

    previous_block = chain[-1]

    new_block = {
        "index": len(chain),
        "timestamp": str(datetime.now()),
        "file_hash": file_hash,
        "previous_hash": previous_block["current_hash"]
    }

    # Generate current block hash
    new_block["current_hash"] = calculate_block_hash(
        new_block
    )

    chain.append(new_block)

    save_blockchain(chain)

    print("[+] New block added")

    return new_block


# Verify blockchain integrity
def verify_blockchain():

    chain = load_blockchain()

    for i in range(1, len(chain)):

        current_block = chain[i]
        previous_block = chain[i - 1]

        # Recalculate current block hash
        recalculated_hash = calculate_block_hash({
            "index": current_block["index"],
            "timestamp": current_block["timestamp"],
            "file_hash": current_block["file_hash"],
            "previous_hash": current_block["previous_hash"]
        })

        # Check current hash
        if current_block["current_hash"] != recalculated_hash:
            return False

        # Check previous hash linkage
        if current_block["previous_hash"] != previous_block["current_hash"]:
            return False

    return True