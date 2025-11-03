#!/usr/bin/env python3
"""
MISP to MongoDB/TAXII Exporter
Exports IP indicators from MISP and stores them directly in MongoDB for Medallion TAXII server
"""

import requests
import time
from datetime import datetime, timezone
from pymongo import MongoClient, UpdateOne, ASCENDING
from urllib3.exceptions import InsecureRequestWarning
import sys, json

# Disable SSL warnings if using self-signed certificates
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# ============================================================================
# CONFIGURATION
# ============================================================================

with open("config.json", "r") as f:
    config = json.load(f)   # access information with config[key]

# MISP Configuration
MISP_URL = config['misp_url']
MISP_API_KEY = config['misp_key']
MISP_VERIFY_SSL = True  # Set to False for self-signed certificates

# MongoDB Configuration
MONGO_URI = config["mongo_url"]
MONGO_DB = config["mongo_db"]
MONGO_OBJECTS_COLLECTION = config["mongo_objects_collection"]
MONGO_MANIFESTS_COLLECTION = config["mongo_manifests_collection"]

# TAXII Configuration
TAXII_COLLECTION_ID = "misp-indicators"  # Your TAXII collection ID

# Query Configuration
MAX_IOC = 10000  # Maximum number of IOCs to fetch
BATCH_SIZE = 100  # Number of documents to insert per batch

# ============================================================================
# MONGODB SETUP
# ============================================================================

def setup_mongodb():
    """Initialize MongoDB connection and create indexes"""
    try:
        print("Connecting to MongoDB...")
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.server_info()
        print(f"✓ Connected to MongoDB at {MONGO_URI}")
        
        db = client[MONGO_DB]
        objects_collection = db[MONGO_OBJECTS_COLLECTION]
        manifests_collection = db[MONGO_MANIFESTS_COLLECTION]
        
        # Create indexes for performance
        print("Creating indexes...")
        objects_collection.create_index([("id", ASCENDING)], unique=True)
        objects_collection.create_index([("type", ASCENDING)])
        objects_collection.create_index([("_collection_id", ASCENDING)])
        objects_collection.create_index([("created", ASCENDING)])
        manifests_collection.create_index([("id", ASCENDING), ("_collection_id", ASCENDING)], unique=True)
        print("✓ Indexes created successfully")
        
        return client, objects_collection, manifests_collection
        
    except Exception as e:
        print(f"✗ Error connecting to MongoDB: {str(e)}")
        sys.exit(1)

# ============================================================================
# MISP DATA FETCHING
# ============================================================================

def fetch_misp_indicators():
    """Fetch IP indicators from MISP"""
    print(f"\nFetching IP indicators from MISP ({MISP_URL})...")
    
    # MISP query parameters
    misp_data = {
        "controller": "attributes",
        "type": ["ip-src"],
        "to_ids": True,  # Only indicators with IDS flag
        "deleted": False,
        "published": True,
        "order": "timestamp desc",
        "limit": MAX_IOC
    }
    
    try:
        response = requests.post(
            f"{MISP_URL}/attributes/restSearch",
            json=misp_data,
            headers={
                "Authorization": MISP_API_KEY,
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            verify=MISP_VERIFY_SSL,
            timeout=60
        )
        response.raise_for_status()
        
        data = response.json()
        
        if "response" in data and "Attribute" in data["response"]:
            indicators = data["response"]["Attribute"]
            print(f"✓ Fetched {len(indicators)} IP indicators from MISP")
            return indicators
        else:
            print("✗ No indicators found in MISP response")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching data from MISP: {str(e)}")
        return []

# ============================================================================
# STIX CONVERSION AND MONGODB INSERTION
# ============================================================================

def create_stix_indicator(ip, collection_id):
    """Convert MISP IP to STIX 2.1 indicator format"""
    timestamp = datetime.fromtimestamp(int(ip['timestamp']), timezone.utc)
    timestamp_str = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
    date_added = datetime.now(timezone.utc)
    misp_event_url = f"{MISP_URL}/events/view/{ip['event_id']}"
    
    stix_indicator = {
        "type": "indicator",
        "spec_version": "2.1",
        "id": f"indicator--{ip['uuid']}",
        "created": timestamp_str,
        "modified": timestamp_str,
        "name": f"MISP IP Address {ip['value']}",
        "description": ip.get('comment', '') or 'Imported from MISP',
        "pattern": f"[ipv4-addr:value = '{ip['value']}']",
        "pattern_type": "stix",
        "valid_from": timestamp_str,
        "external_references": [
            {
                "source_name": "MISP",
                "description": f"MISP Event {ip['event_id']}",
                "url": misp_event_url,
                "external_id": str(ip['event_id'])
            }
        ],
        # Medallion/TAXII metadata
        "_collection_id": collection_id,
        "_date_added": date_added.isoformat(),
        "_misp_event_id": str(ip['event_id']),
        "_misp_attribute_id": str(ip['id']),
        "_misp_value": ip['value']
    }
    
    return stix_indicator, timestamp_str, date_added

def create_manifest_entry(indicator_id, collection_id, version, date_added):
    """Create manifest entry for TAXII"""
    return {
        "id": indicator_id,
        "_collection_id": collection_id,
        "date_added": date_added.isoformat(),
        "version": version,
        "media_type": "application/stix+json;version=2.1"
    }

def batch_insert_indicators(ip_list, objects_collection, manifests_collection, collection_id, batch_size=100):
    """Insert indicators in batches to MongoDB"""
    total_inserted = 0
    total_updated = 0
    total_unchanged = 0
    total_errors = 0
    
    total_batches = (len(ip_list) - 1) // batch_size + 1
    
    print(f"\nStarting batch insertion ({total_batches} batches of max {batch_size} items)...")
    print("=" * 80)
    
    for i in range(0, len(ip_list), batch_size):
        batch = ip_list[i:i+batch_size]
        bulk_operations_objects = []
        bulk_operations_manifests = []
        
        for ip in batch:
            try:
                # Create STIX indicator
                stix_indicator, version, date_added = create_stix_indicator(ip, collection_id)
                
                # Prepare bulk operation for objects collection
                bulk_operations_objects.append(
                    UpdateOne(
                        {"id": stix_indicator["id"]},
                        {"$set": stix_indicator},
                        upsert=True
                    )
                )
                
                # Prepare bulk operation for manifests collection
                manifest_entry = create_manifest_entry(
                    stix_indicator["id"], 
                    collection_id, 
                    version, 
                    date_added
                )
                bulk_operations_manifests.append(
                    UpdateOne(
                        {"id": manifest_entry["id"], "_collection_id": collection_id},
                        {"$set": manifest_entry},
                        upsert=True
                    )
                )
                
            except Exception as e:
                print(f"  ✗ Error preparing IP {ip.get('value', 'unknown')}: {str(e)}")
                total_errors += 1
        
        # Execute bulk operations
        if bulk_operations_objects:
            try:
                # Insert objects
                result_objects = objects_collection.bulk_write(bulk_operations_objects, ordered=False)
                
                # Insert manifests
                result_manifests = manifests_collection.bulk_write(bulk_operations_manifests, ordered=False)
                
                batch_num = i // batch_size + 1
                inserted = result_objects.upserted_count
                updated = result_objects.modified_count
                unchanged = result_objects.matched_count - result_objects.modified_count
                
                total_inserted += inserted
                total_updated += updated
                total_unchanged += unchanged
                
                print(f"Batch {batch_num}/{total_batches}: "
                      f"✓ {inserted} new | "
                      f"↻ {updated} updated | "
                      f"○ {unchanged} unchanged")
                
            except Exception as e:
                print(f"  ✗ Error in batch {batch_num}: {str(e)}")
                total_errors += len(bulk_operations_objects)
    
    print("=" * 80)
    print(f"\nSUMMARY:")
    print(f"  Total processed: {len(ip_list)}")
    print(f"  ✓ Inserted (new): {total_inserted}")
    print(f"  ↻ Updated (modified): {total_updated}")
    print(f"  ○ Unchanged (already up-to-date): {total_unchanged}")
    if total_errors > 0:
        print(f"  ✗ Errors: {total_errors}")
    print("=" * 80)
    
    return {
        "inserted": total_inserted,
        "updated": total_updated,
        "unchanged": total_unchanged,
        "errors": total_errors,
        "total": len(ip_list)
    }

# ============================================================================
# STATISTICS
# ============================================================================

def print_mongodb_stats(objects_collection, collection_id):
    """Print MongoDB collection statistics"""
    try:
        total_objects = objects_collection.count_documents({"_collection_id": collection_id})
        total_indicators = objects_collection.count_documents({
            "_collection_id": collection_id,
            "type": "indicator"
        })
        
        print(f"\nMongoDB Statistics:")
        print(f"  Total objects in collection '{collection_id}': {total_objects}")
        print(f"  Total indicators: {total_indicators}")
        
        # Get some sample data
        sample = objects_collection.find_one({"_collection_id": collection_id})
        if sample:
            print(f"\nSample indicator:")
            print(f"  ID: {sample.get('id')}")
            print(f"  Name: {sample.get('name')}")
            print(f"  Pattern: {sample.get('pattern')}")
            print(f"  Created: {sample.get('created')}")
            
    except Exception as e:
        print(f"✗ Error fetching statistics: {str(e)}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print("=" * 80)
    print("MISP to MongoDB/TAXII Exporter")
    print("=" * 80)
    
    start_time = time.time()
    
    # Setup MongoDB
    mongo_client, objects_collection, manifests_collection = setup_mongodb()
    
    try:
        # Fetch indicators from MISP
        indicators = fetch_misp_indicators()
        
        if not indicators:
            print("\n⚠ No indicators to process. Exiting.")
            return
        
        # Insert indicators into MongoDB
        results = batch_insert_indicators(
            indicators,
            objects_collection,
            manifests_collection,
            TAXII_COLLECTION_ID,
            BATCH_SIZE
        )
        
        # Print statistics
        print_mongodb_stats(objects_collection, TAXII_COLLECTION_ID)
        
        # Final summary
        elapsed_time = time.time() - start_time
        print(f"\n✓ Export completed in {elapsed_time:.2f} seconds")
        print(f"  Average speed: {len(indicators)/elapsed_time:.2f} indicators/second")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Process interrupted by user")
        
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Close MongoDB connection
        mongo_client.close()
        print("\n✓ MongoDB connection closed")
        print("=" * 80)

if __name__ == "__main__":
    main()