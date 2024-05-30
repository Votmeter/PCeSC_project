from flask import Flask,request,redirect,url_for,render_template
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from secret import secret_key
from google.cloud import firestore
#from turbo_flask import Turbo
import json
import time
from joblib import load
from google.cloud import storage
from google.cloud import pubsub_v1
from google.auth import jwt

class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        self.username = username

app = Flask(__name__, template_folder="static")
app.config['SECRET_KEY'] = secret_key
login = LoginManager(app)
login.login_view = '/static/login.html'

usersdb = { 'mess':'1234'}

db = 'tesinapcesc'
coll = 'trajectories'
db = firestore.Client.from_service_account_json('credentials.json', database=db)

@app.route('/sequence/<s>', methods=["GET", "POST"])
def proposeswap_db_function(s):
    d2 = json.loads(get_data(s)[0])
    k = int(request.form["jsvar"])+1
    print(k)
    return render_template('graph2.html', data=d2[:k], s=s, k=k)

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

@app.route('/',methods=['GET'])
def main():
    return render_template('graph.html')

@app.route('/fire',methods=['GET'])
def fire():
    db = firestore.Client.from_service_account_json('credentials.json', database=db)
    result = ''
    for doc in db.collection('persone').stream():
        result += (f'{doc.id} --> {doc.to_dict()}<br>')
    return result

@app.route('/graph5/<s>', methods=['GET'])
def graph2(s):
    print('ciao2')
    d2 = json.loads(get_data(s)[0])
    print(d2)
    return render_template('graph1.html', data=d2)

@app.route('/graph5animated/<s>', methods=['GET'])
def graph5animated(s):
    print('ciao5')
    d2 = json.loads(get_data(s)[0])
    return render_template('graph2.html', data=d2[:2],s=s, k=2)

@app.route('/multigraph5/<s>', methods=['GET'])
def multigraph(s):
    print('ciao7')
    S=s.replace(" ","").split(",")
    print(S)
    D=[]
    for k in S:
        d2 = json.loads(get_data(k)[0])
        D.append(d2)
    print(D)
    return render_template('multigraph1.html', data=D)

@app.route('/trajectory/<s>',methods=['GET'])
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



@app.route('/selgraph',methods=['GET'])
def getlist():
    l=[]
    for doc in db.collections():
        l.append(doc.id)
    l=json.dumps(l)
    return render_template('selgraph.html', l=l)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
