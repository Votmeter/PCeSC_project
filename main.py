import pandas as pd
from flask import Flask,request,jsonify, redirect,url_for,render_template
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from secret import secret_key
from google.cloud import firestore
import json

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


class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        self.username = username

app = Flask(__name__, template_folder="static")
app.config['SECRET_KEY'] = secret_key
login = LoginManager(app)
login.login_view = '/static/login.html'

usersdb = { 'mess':'1234' }

db = '(default)'
db = firestore.Client.from_service_account_json('credentials.json', database=db)

@app.route('/')
def root():
    return redirect('/static/index.html')
@app.route('/sequence/<s>', methods=["GET", "POST"])
def proposeswap_db_function(s):
    d2 = json.loads(get_data(s)[0])
    k = int(request.form["jsvar"])+1
    print(k)
    return render_template('graph5animated.html', data=d2[:k], s=s, k=k)

@login.user_loader
def load_user(username):
    if username in usersdb:
        return User(username)
    return None

@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/sensors'))
    username = request.values['u']
    password = request.values['p']
    if username in usersdb and password == usersdb[username]:
        login_user(User(username))
        return redirect('/sensors')
    return redirect('/static/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/')
def main():
    return render_template('graph5base.html')

@app.route('/graph5/<s>')
def graph2(s):
    print('ciao2')
    d2 = json.loads(get_data(s)[0])
    print(d2)
    return render_template('graph5base.html', data=d2)

@app.route('/graph5animated/<s>')
def graph5animated(s):
    print('ciao5')
    S = s.replace(" ", "").split(",")
    d2 = json.loads(get_data(S[0])[0])
    return render_template('graph5animated.html', data=d2[:2],s=S[0], k=2)

@app.route('/multigraph5/<s>')
def multigraph(s):
    print('ciao7')
    S=s.replace(" ","").split(",")
    print(S)
    D=[]
    strn=" "
    for k in S:
        d2 = json.loads(get_data(k)[0])
        D.append(d2)
        strn=strn+"  "+k
    print(D)
    return render_template('multigraph5.html', data=D, s=strn)

@app.route('/trajectory/<s>')
def get_data(s):
    if db.collection(s).stream():
        r=[]
        for doc in db.collection(s).stream():
            w=doc.to_dict()["lat"]
            v=doc.to_dict()["long"]
            r.append([w, v])
        return json.dumps(r),200
    else:
        return 'trajectory not found',404

@app.route('/references')
def get_references():
    if db.collection("references").stream():
        r={}
        for doc in db.collection("references").stream():
            w=doc.to_dict()["mod"]
            v=doc.to_dict()["tras"]
            r[doc.id]=[w, v]
        return json.dumps(r),200
    else:
        return 'references not found',404

@app.route('/graph3')
def root_grafico():
    df={}
    i=0
    for x in db.collections():
        if (i > 127):
            break
        try:
            df[x.id]=json.loads(get_data(x.id)[0])
            #print(x.id)
            i+=1
        except:
            continue
    ref=json.loads(get_references()[0])
    return render_template('graph3.html', data=json.dumps(df),ref=json.dumps(ref))

@app.route('/selgraph')
def getlist():
    l=[]
    for doc in db.collections():
        if doc.id == "references": continue
        l.append(doc.id)
    l=json.dumps(l)
    return render_template('selezionagrafico5.html', l=l)

@app.route('/selgraphanimato')
def getlistanimated():
    l=[]
    for doc in db.collections():
        if doc.id == "references": continue
        l.append(doc.id)
    l=json.dumps(l)
    return render_template('selezionagrafico5animato.html', l=l)


@app.route('/generate_corridor_plot')
def generate_corridor_plot():
    df = {}
    i = 0
    for x in db.collections():
        if (i > 127):
            break
        try:
            df[x.id] = json.loads(get_data(x.id)[0])
            # print(x.id)
            i += 1
        except:
            continue
    ref = json.loads(get_references()[0])

    return render_template('corridoio_migratorio.html', data=json.dumps(df), ref=json.dumps(ref))


# NICO's part
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
    # collection_id = data.get('id').split(',')

    collection_name = data.get('name')
    documents = data.get('data')
    
    collection_ref = db.collection(collection_name)

    # Recupera tutti i documenti nella collezione
    docs = list(collection_ref.stream())

    if not docs:
        # Se la collezione è vuota
        last_doc_id = 1000000
    else:
        # Se ci sono documenti, ordina per ID e prendi l'ultimo
        docs_sorted = sorted(docs, key=lambda x: x.id)
        last_doc_id = int(docs_sorted[-1].id)
        # print(last_doc_id)


    # Estrai le coordinate
    coordinates = documents.get('features')[0].get('geometry').get('coordinates')
    # print(coordinates)
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
