import pandas as pd
from flask import Flask,request,redirect,url_for,render_template
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from secret import secret_key
from google.cloud import firestore
import json


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

db = '(default)'
db = firestore.Client.from_service_account_json('credentials.json', database=db)

#pagina iniziale che non è soggetta al login
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
    for k in S:
        d2 = json.loads(get_data(k)[0])
        D.append(d2)
    print(D)
    return render_template('multigraph5.html', data=D, s=S)

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
        l.append(doc.id)
    l=json.dumps(l)
    return render_template('selezionagrafico5.html', l=l)

@app.route('/selgraphanimato')
def getlistanimated():
    l=[]
    for doc in db.collections():
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
