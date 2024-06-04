from flask import Flask, redirect, request, render_template_string
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
@login_required
def main():
    return 'Hi ' + current_user.email


@app.route('/main2')
@login_required
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


@app.route('/corridoio_migratorio')
def visualizza_corridoio_migratorio():
    # Chiama la funzione create_corridor_plot per generare il grafico
    create_corridor_plot()
    # Leggi il contenuto del file HTML del grafico
    with open('static/corridoio_migratorio.html', 'r') as f:
        html_content = f.read()
    # Ritorna il contenuto HTML al template
    return render_template_string(html_content)
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
