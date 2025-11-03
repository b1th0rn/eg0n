#!/usr/bin/env python3
"""
MongoDB → TAXII2 Exporter
Reads STIX 2.1 objects from MongoDB and pushes them to an external TAXII2 server
"""

import json, requests, urllib3, time, sys
from pymongo import MongoClient
from datetime import datetime

# ===========================================================
# CONFIGURATION
# ===========================================================

with open("config.json", "r") as f:
    config = json.load(f)

# MongoDB
MONGO_URI = config["mongo_url"]
MONGO_DB = config["mongo_db"]
MONGO_OBJECTS_COLLECTION = config["mongo_objects_collection"]

# TAXII2
TAXII_URL = config["taxii_url"].rstrip("/")
TAXII_APIROOT = config["taxii_apiroot"].strip("/")
TAXII_COLLECTION_ID = config["taxii_collection_id"]
TAXII_USERNAME = config["taxii_username"]
TAXII_PASSWORD = config["taxii_password"]
VERIFY_CERT = config.get("verify_cert", True)

if not VERIFY_CERT:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Settings
BATCH_SIZE = 100
TIMEOUT = 30

# ===========================================================
# FUNCTIONS
# ===========================================================

def connect_mongodb():
    """Connect to MongoDB and return collection handle"""
    print(f"Connecting to MongoDB at {MONGO_URI} ...")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[MONGO_DB]
    collection = db[MONGO_OBJECTS_COLLECTION]
    print(f"Connected to {MONGO_DB}.{MONGO_OBJECTS_COLLECTION}")
    return client, collection


def fetch_stix_objects(collection, collection_id=None):
    """Fetch STIX indicator objects from MongoDB"""
    query = {}
    if collection_id:
        query["_collection_id"] = collection_id
    print(f"Fetching STIX indicators from MongoDB (filter: {query}) ...")
    docs = list(collection.find(query))
    print(f"Retrieved {len(docs)} objects from MongoDB.")
    return docs


def send_to_taxii(objects):
    """Send each STIX object individually to TAXII2 server via requests"""
    endpoint = f"{TAXII_URL}/{TAXII_APIROOT}/collections/{TAXII_COLLECTION_ID}/objects/"
    print(f"\nSending to TAXII collection: {endpoint}")

    total_sent = 0

    for idx, obj in enumerate(objects, start=1):
        # rimuovi _id MongoDB
        obj_copy = obj.copy()
        if "_id" in obj_copy:
            del obj_copy["_id"]

        payload = {"objects": [obj_copy]}
        payload_json = json.dumps(payload)

        # costruzione della riga curl per debug
        curl_cmd = (
            f"curl -u {TAXII_USERNAME}:<password> "
            f"-X POST {endpoint} "
            f"-H 'Accept: application/taxii+json;version=2.1' "
            f"-H 'Content-Type: application/taxii+json;version=2.1' "
            f"-d '{payload_json}'"
        )

        try:
            response = requests.post(
                endpoint,
                json=payload,
                auth=(TAXII_USERNAME, TAXII_PASSWORD),
                headers={
                    "Accept": "application/taxii+json;version=2.1",
                    "Content-Type": "application/taxii+json;version=2.1"
                },
                verify=VERIFY_CERT,
                timeout=TIMEOUT
            )

            response.raise_for_status()
            print(f"Sent object {idx}/{len(objects)}: {obj_copy.get('id')} (HTTP {response.status_code})")
            time.sleep(1)

        except Exception as e:
            print(f"Error sending object {idx}: {e}")
            print(f"Payload JSON:\n{payload_json}")
            print(f"Equivalent cURL:\n{curl_cmd}\n")

    print(f"\nDone. Total sent: {total_sent}/{len(objects)}")

def main():
    start_time = datetime.now()
    try:
        client, collection = connect_mongodb()
        stix_objects = fetch_stix_objects(collection, TAXII_COLLECTION_ID)

        if not stix_objects:
            print("No STIX objects found to send.")
            return

        send_to_taxii(stix_objects)

    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            client.close()
            print("MongoDB connection closed.")
        except:
            pass
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"Completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()
