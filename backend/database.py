# MongoDB Connection and Initialization
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB URI
uri = "mongodb+srv://2023bcs116:2023bcs116@cluster0.fw8lk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    logger.info("Pinged your deployment. Successfully connected to MongoDB!")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise

def import_json_to_mongodb(json_file_path, db_name, collection_name):
    """
    Import data from a JSON file into a MongoDB collection.

    Args:
        json_file_path (str): Path to the JSON file.
        db_name (str): Name of the MongoDB database.
        collection_name (str): Name of the MongoDB collection.
    """
    try:
        # Validate the JSON file path
        if not json_file_path:
            raise ValueError("JSON file path is empty.")

        # Load JSON data
        with open(json_file_path, 'r') as json_file:
            records = json.load(json_file)

        # Validate loaded data
        if not records:
            raise ValueError("JSON file is empty or invalid.")

        # Access the database and collection
        db = client[db_name]
        collection = db[collection_name]

        # Insert data into MongoDB
        if isinstance(records, list):
            result = collection.insert_many(records)
            logger.info(f"Successfully imported {len(result.inserted_ids)} records into the {collection_name} collection.")
        elif isinstance(records, dict):
            result = collection.insert_one(records)
            logger.info(f"Successfully imported 1 record into the {collection_name} collection.")
        else:
            raise ValueError("JSON data is neither a list nor a dictionary.")
    except FileNotFoundError:
        logger.error(f"JSON file not found: {json_file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON file: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to import data into MongoDB: {e}")
        raise

# Example usage
if __name__ == "__main__":
    # Path to your JSON file
    json_file_path = "colleges_data_JSON.json"  # Replace with the actual path

    # MongoDB database and collection names
    db_name = "admissions_db"
    collection_name = "colleges"

    # Import data
    import_json_to_mongodb(json_file_path, db_name, collection_name)
