#!/usr/bin/env python3
"""
Delete a STIX object from MongoDB by its ID
"""

import json, sys
from pymongo import MongoClient

# ===========================================================
# CONFIGURATION
# ===========================================================
with open("config.json", "r") as f:
    config = json.load(f)

MONGO_URI = config["mongo_url"]
MONGO_DB = config["mongo_db"]
MONGO_OBJECTS_COLLECTION = config["mongo_objects_collection"]

# ===========================================================
# FUNCTION
# ===========================================================
def delete_from_mongodb(stix_id):
    """Delete object from MongoDB by its STIX id"""
    client = MongoClient(MONGO_URI)
    collection = client[MONGO_DB][MONGO_OBJECTS_COLLECTION]
    result = collection.delete_one({"id": stix_id})
    client.close()
    if result.deleted_count:
        print(f"Deleted {stix_id} from MongoDB")
    else:
        print(f"{stix_id} not found in MongoDB")

# ===========================================================
# MAIN
# ===========================================================
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <stix_id>")
        exit(1)

    stix_id = sys.argv[1]
    delete_from_mongodb(stix_id)
