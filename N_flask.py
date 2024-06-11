from flask import Flask, jsonify, send_from_directory, request, redirect, render_template
import json

import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore

# # Inizializza l'app Firebase
# cred = credentials.Certificate('keys/nico_pk.json')
# firebase_admin.initialize_app(cred)

# # Connettiti a Firestore usando le stesse credenziali
# db = firestore.Client(credentials=cred, project=cred.project_id)

db = '(default)'
db = firestore.Client.from_service_account_json('keys/nico_pk.json', database=db)

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
    return send_from_directory('static', 'inserisci_dati.html')

@app.route('/get_collections', methods=['GET'])
def get_collections():
    collections = db.collections()
    collection_names = [collection.id for collection in collections]
    return jsonify(collection_names)

@app.route('/get_documents/<collection_name>', methods=['GET'])
def det_documents(collection_name):
    documents = db.collection(collection_name).get()
    document_names = [document.id for document in documents]
    return jsonify(document_names)


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


    last_doc_id = None
    for doc in db.collection(collection_name).stream():
        last_doc_id = int(doc.id)    

    # Estrai le coordinate
    coordinates = documents.get('features')[0].get('geometry').get('coordinates')

    # Converti in lista di tuple (latitudine, longitudine)
    locoords = [[coord[1], coord[0]] for coord in coordinates]

        
    # Loop through each document in the current collection
    for coord in range(len(locoords)):
        # Create a reference to the current document in Firestore
        doc_ref = db.collection(collection_name).document(str(last_doc_id))
        
        # Prepare the data to be stored in Firestore
        x = {
            "lat": locoords[coord][0],
            "long": locoords[coord][1]
        }
        
        # Set the data in Firestore for the current document
        doc_ref.set(x)
        last_doc_id = last_doc_id + 1

    return 'Collection added', 200

@app.route('/<collection_name>/<document_id>', methods=['GET'])
def single_document(collection_name, document_id):
    # Ottieni il riferimento al documento
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()

    # Verifica se il documento esiste
    if doc.exists:
        doc_dict = doc.to_dict()
        return jsonify(doc_dict)
    else:
        return jsonify({"error": "Document not found"}), 404

@app.route('/<collection_name>/<document_id>', methods=['POST'])
def update_document(collection_name, document_id):
    # Ottieni i dati JSON dalla richiesta
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Ottieni il riferimento al documento
    doc_ref = db.collection(collection_name).document(document_id)

    # Aggiorna il documento
    doc_ref.set(data, merge=True)

    return jsonify({"success": True}), 200

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)




