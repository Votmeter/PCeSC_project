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