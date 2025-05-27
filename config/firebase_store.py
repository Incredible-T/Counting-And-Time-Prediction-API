import firebase_admin
from firebase_admin import credentials, firestore
import json

# Load the service account key from the JSON file
with open(".env/traffic-data.json", "r") as key_file:
    service_account_key = json.load(key_file)

# Initialize Firebase Admin SDK
cred = credentials.Certificate(service_account_key)
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()


# Example function to store data in Firestore
def store_data(collection_name, document_id, data):
    try:
        doc_ref = db.collection(collection_name).document(document_id)
        doc_ref.set(data)
        print(
            f"Document {document_id} successfully written to {collection_name} collection."
        )
    except Exception as e:
        print(f"An error occurred: {e}")
