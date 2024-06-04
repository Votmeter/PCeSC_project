from flask import Flask, jsonify, send_from_directory, request, redirect, render_template
from google.cloud import firestore
import json


db = 'tesinapcesc'
db = firestore.Client.from_service_account_json("keys/nico_pk.json",
                                                 database = db)

# Funzione per verificare se una collezione esiste
def collection_exists(collection_name):
    collections = db.collections()
    for collection in collections:
        if collection.id == collection_name:
            return True
    return False

# Funzione per verificare se un documento esiste in una collezione
def document_exists(collection_name, document_name):
    doc_ref = db.collection(collection_name).document(document_name)
    doc = doc_ref.get()
    return doc.exists

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main():
    return redirect('/collections')


@app.route('/collections')
def serve_html():
    return send_from_directory('static', 'mockpage.html')

@app.route('/get_collections', methods=['GET'])
def get_collections():
    collections = db.collections()
    collection_names = [collection.id for collection in collections]
    return jsonify(collection_names)

# Endpoint per ottenere tutti i documenti di una collezione specifica
@app.route('/get_documents/<collection_name>', methods=['GET'])
def get_documents(collection_name):
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()
    documents = {doc.id: doc.to_dict() for doc in docs}
    return jsonify(documents)

@app.route('/collections/<coll>', methods=['GET'])
def get_all_documents(coll):
    collection_ref = db.collection(coll)
    docs = collection_ref.stream()
    documents = {}
    for doc in docs:
        documents[doc.id] = doc.to_dict()
    return documents


# Endpoint per aggiungere una nuova collezione
@app.route('/add_collection', methods=['POST'])
def add_collection():
    data = request.json
    collection_id = data.get('id').split(',')

    collection_name = data.get('name')
    documents = data.get('data')
    
    if not collection_name or not documents or len(documents.get('features')) !=  len(collection_id):
        if document_exists(collection_name, id):
            return 'Invalid data', 400


    # collection_ref = db.collection(collection_name)
    for iter in range(len(collection_id)):
        coordinates =  documents.get('features')[0].get('geometry').get('coordinates')

        doc = {
            str(index): coord for index, coord in enumerate(coordinates)
        }

        db.collection(collection_name).document(collection_id[iter]).set(doc)

    return 'Collection added', 200

# Route to get documents for a specific collection
@app.route('/edit_database/<collection_name>', methods=['GET'])
def db_edit(collection_name):    
    docs = db.collection(collection_name).stream()
    
    documents = {doc.id: doc.to_dict() for doc in docs}
    print(collection_name)
    # Render the template with the document list
    return send_from_directory('static','mockedit.html'),documents



    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)




