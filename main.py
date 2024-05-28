from flask import Flask, redirect, url_for, request, render_template
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
#from secret import secret_key
#inserisco file secret e la nostra chiave
#dobbiamo decidere la pagina iniziale

# For more advanced features: email confirmation, password reset, roles, etc.
# use Flask-Security https://pythonhosted.org/Flask-Security/quickstart.html


# From: https://stackoverflow.com/questions/63231163/what-is-the-usermixin-in-flask
# Flask-login requires a User model with the following properties:
# -- has an is_authenticated() method that returns True if the user has provided valid credentials
# -- has an is_active() method that returns True if the user’s account is active
# -- has an is_anonymous() method that returns True if the current user is an anonymous user
# --has a get_id() method which, given a User instance, returns the unique ID for that object
# UserMixin class provides the implementation of this properties.
# Its the reason you can call for example is_authenticated to check
# if login credentials provide is correct or not instead of having to write a
# method to do that yourself.



#devo definire una classe utente alla quale devo passargli, id univoco per un determinato username
#classe nasconde l'utilizzo delle session, utente
import grafici


class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        self.username = username
        #self.par = {}

app = Flask(__name__, template_folder="static")
app.config['SECRET_KEY'] = 'secret_key'

# The login manager contains the code that lets your application and Flask-Login work together,
# such as how to load a user from an ID, where to send users when they need to log in, and the like.
#creami il LoginManager che gestisce il login della mia applicazione
login = LoginManager(app)
#tutte le volte che hai bisogno di far fare il login rimandalo a questa pagina

login.login_view = '/static/login.html'


#database con username e password di quelle autenticati
usersdb = {
    'marco':'mamei'
}

@login.user_loader
def load_user(username):
    if username in usersdb:
        return User(username)
    return None

#pagina iniziale che non è soggetta al login
@app.route('/')
def root():
    return redirect('/static/index.html')
    #return render_template('index.html',plot = grafici.create_plot())

#pagina grafico 1
@app.route('/static/grafico uno.html')
def root_grafico():
    #return redirect('/static/index.html')
    return render_template('grafico uno.html', plot = grafici.create_plot())

#pagina grafico 2
@app.route('/static/grafico due.html')
def root_grafico2():
    #return redirect('/static/index.html')
    return render_template('grafico due.html', plot = grafici.create_plot2())

#soggetta al login che accede a:
@app.route('/main')
#funzioni successive a login_REQUIRED necessitano che sia stato realizzato il login per funzionare
@login_required
def index():
    #oggetto del campo user current_user e posso accedere ai campi in questo esempio username
    return 'Hi '+current_user.username

@app.route('/main2')
@login_required
def index2():
    return 'Hi2 '+current_user.username
#procedura di login:, end point login riceve le informazioni della form, username e password della form
@app.route('/login', methods=['POST'])

def login():
    if current_user.is_authenticated:
        return redirect(url_for('/main'))#main
    username = request.values['u']#username
    password = request.values['p']#password
    next_page = request.values['next']
    #accedere al parametro della form
    #next_page = request.args.get('next')
    #altrimenti login
    #cercare un meccanismo in javascript che prima direttamente il javascript
    if username in usersdb and password == usersdb[username]:
        login_user(User(username))#login_user è una funzione di libreria che serve a lui per tenere traccia se l'utente ha fatto il login
        if not next_page:
            #esistono librerie di flask per gestire le pagine dopo il login
            next_page = '/main'
        return redirect(next_page)
    return redirect('/static/login.html')

@app.route('/logout')
def logout():
    logout_user()#funzione di libreria
    return redirect('/')
#codice di copia in colla e dopo tutte le volte che richiedono il login inserisco @login_required
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

#ogni volta che faccio il login lui chiama la funzione login.user_loader: carico l'utente che voglio utilizzare e ogni volta devo rinizializzare il bar che avevo
