from flask import Flask, redirect, request, render_template_string, jsonify,render_template
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from secret import secret_key
from prova_grafico4 import create_corridor_plot

class User(UserMixin):
    def __init__(self, email):
        super().__init__()
        self.id = email
        self.email = email

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
login = LoginManager(app)
login.login_view = '/static/accedi.html'

usersdb = {
    'marco': 'mamei'
}

@login.user_loader
def load_user(email):
    if email in usersdb:
        return User(email)
    return None

@app.route('/')
def root():
    return redirect('/static/index.html')

@app.route('/main')

def main():
    return 'Hi ' + current_user.email

@app.route('/main2')

def main2():
    return 'Hi2 ' + current_user.email

@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    email = request.form.get('e')
    password = request.form.get('p')
    next_page = request.form.get('next', '/main')

    if email in usersdb and password == usersdb[email]:
        login_user(User(email))
        return redirect(next_page)

    return redirect('/static/login.html')

@app.route('/corridor_plot')

def corridor_plot():
    create_corridor_plot()
    with open('static/grafico_due.html', 'r') as f:
        html_content = f.read()
    return render_template_string(html_content)

@app.route('/corridor_plot_data')

def corridor_plot_data():
    create_corridor_plot()
    with open('static/grafico_due.html', 'r') as f:
        return jsonify(json.load(f))

#pagina grafico 1
@app.route('/static/traiettorie.html')
def root_grafico():
    return render_template('traiettorie.html', plot = grafici.create_plot())


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
'''

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
#db = firestore.Client.from_service_account_json('credentials.json', database=db)

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

@app.route('/',methods=['GET'])
def main():
    return render_template('graph5base.html')

@app.route('/graph5/<s>', methods=['GET'])
def graph2(s):
    print('ciao2')
    d2 = json.loads(get_data(s)[0])
    print(d2)
    return render_template('graph5base.html', data=d2)

@app.route('/graph5animated/<s>', methods=['GET'])
def graph5animated(s):
    print('ciao5')
    S = s.replace(" ", "").split(",")
    d2 = json.loads(get_data(S[0])[0])
    return render_template('graph5animated.html', data=d2[:2],s=S[0], k=2)

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
    return render_template('multigraph5.html', data=D, s=S)

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

@app.route('/selgraph5',methods=['GET'])
def getlist():
    l=[]
    for doc in db.collections():
        l.append(doc.id)
    l=json.dumps(l)
    return render_template('selezionagrafico5.html', l=l)

@app.route('/selgraph5animated',methods=['GET'])
def getlistanimated():
    l=[]
    for doc in db.collections():
        l.append(doc.id)
    l=json.dumps(l)
    return render_template('selezionagrafico5animato.html', l=l)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)'''