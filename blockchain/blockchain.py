import json
import logging
import hashlib
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Path relative to this file's location, not working directory
BLOCKCHAIN_FILE = Path(__file__).parent / "blockchain.json"


def calculate_block_hash(block):
    """Create SHA-256 hash for block."""
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()


def load_blockchain():
    """Load blockchain from JSON file."""
    if not BLOCKCHAIN_FILE.exists() or BLOCKCHAIN_FILE.stat().st_size == 0:
        with open(BLOCKCHAIN_FILE, 'w') as f:
            json.dump([], f)

    with open(BLOCKCHAIN_FILE, 'r') as f:
        return json.load(f)


def save_blockchain(chain):
    """Save blockchain to JSON file."""
    with open(BLOCKCHAIN_FILE, 'w') as f:
        json.dump(chain, f, indent=4)


def create_genesis_block():
    """Create genesis block if not exists."""
    chain = load_blockchain()

    if len(chain) > 0:
        return

    genesis_block = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "file_hash": "GENESIS_BLOCK",
        "previous_hash": "0"
    }
    genesis_block["current_hash"] = calculate_block_hash(genesis_block)

    chain.append(genesis_block)
    save_blockchain(chain)
    logger.info("Genesis block created")


def add_block(file_hash):
    """Add new block to the blockchain."""
    chain = load_blockchain()

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
    new_block["current_hash"] = calculate_block_hash(new_block)

    chain.append(new_block)
    save_blockchain(chain)
    logger.info(f"New block added (index: {new_block['index']})")

    return new_block


def verify_blockchain():
    """Verify blockchain integrity by checking all hash linkages."""
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

        if current_block["current_hash"] != recalculated_hash:
            return False

        if current_block["previous_hash"] != previous_block["current_hash"]:
            return False

    return True
