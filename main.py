
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

    return render_template('corridoio_migratorio.html')  # Renderizza il template HTML

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
