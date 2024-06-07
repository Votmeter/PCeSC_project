
from flask import Flask,redirect,url_for, request, send_from_directory
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from secret import secret_key

class User(UserMixin):
    def __init__(self, email):
        super().__init__()
        self.id = email # id univoco per ogni email
        self.email = email
        #self.par = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
login = LoginManager(app)# LoginManager che gestisce il login della mia applicazione
login.login_view = '/static/accedi.html' #tutte le volte che hai bisogno di far fare il login rimandalo a questa pagina


#database con email e password di quelle autenticati
usersdb = {
    'marco':'mamei'
}

@login.user_loader
def load_user(email):
    if email in usersdb:
        return User(email)
    return None

#pagina iniziale che non è soggetta al login
@app.route('/')
def root():
    return redirect('/static/index.html')
#soggetta al login che accede a:
@app.route('/main')
#funzioni successive a login_REQUIRED necessitano che sia stato realizzato il login per funzionare
@login_required
def index():
    #oggetto del campo user current_user e posso accedere ai campi
    return 'Hi '+current_user.email

@app.route('/main2')
@login_required
def index2():
    return 'Hi2 '+current_user.email
#procedura di login:, end point login riceve le informazioni della form: email e password della form
@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/main'))#main
    email = request.values['e']#email
    password = request.values['p']#password
    next_page = request.values['next']
    #accedere al parametro della form
    #next_page = request.args.get('next')
    #altrimenti login
    #cercare un meccanismo in javascript che prima direttamente il javascript
    if email in usersdb and password == usersdb[email]:
        login_user(User(email))#login_user è una funzione di libreria che serve a lui per tenere traccia se l'utente ha fatto il login
        if not next_page:
            #esistono librerie di flask per gestire le pagine dopo il login
            next_page = '/main'
        return redirect(next_page)
    return redirect('/static/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

#ogni volta che faccio il login lui chiama la funzione login.user_loader: carico l'utente che voglio utilizzare e ogni volta devo rinizializzare il bar che avevo