# Importando coisas do Flask
from flask import Flask, render_template, request, redirect, url_for
# Importando flask_login pra validar usuários, fazer logout e proteger as rotas
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required #Tenho que vê como eu mexo nisso!
# Importando biblioteca de hash de senha
from werkzeug.security import generate_password_hash, check_password_hash
# Importando sqlite3
import sqlite3

app = Flask(__name__)
# Definição de sesão no Flask
app.config['SECRET_KEY'] = 'S_U_P_E_R_S_E_C_R_E_T_O_1_2_3'

# Configurações do flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Nome da rota para a página de login

# Classe do usuário
class User(UserMixin):
    def __init__(self, id_user, nome_user, email_user, hash_user):
        self.id = id_user
        self.nome = nome_user
        self.email = email_user
        self.hash = hash_user

# Conexão com o banco
def obter_conecxao():
    # Conectando o banco
    conn = sqlite3.connect('database.db') 
    # Configuração pra pegar os dados do banco na forma de dicionário
    conn.row_factory = sqlite3.Row
    # Retornando conexão
    return conn

# Validação de usuários
@login_manager.user_loader
def load_user(user_id):
    db = obter_conecxao()
    user = db.execute("SELECT id, nome FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    if user:
        # Retorna o ID e nome da pessoa
        return User(id=user[0], nome=user[1])
    return None

# Página inicial
@app.route('/')
def index():
    return render_template('pages/index.html')

# Página de cadastro (Só funciona de o usuário não tiver no banco!)
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome_user']
        email = request.form['email_user']
        hash_senha = generate_password_hash(request.form['senha_user']) 
        conecxao = obter_conecxao()
        users = conecxao.execute('SELECT email FROM usuarios').fetchall()
        # Verifica se o usuário não está cadastrado!
        for e_user in users:
            if email == e_user[0]:
                conecxao.close()
                return """
                <p>Uusário já cadstrado!</p>
                <p><a href="/">Click aqui para voltar!</a></p>
                """
        conecxao.execute("INSERT INTO usuarios (nome, email, hash_senha) VALUES (?, ?, ?)", (nome, email, hash_senha))
        conecxao.commit()
        conecxao.close()
        return redirect(url_for('home'))
    else:
        return render_template('pages/cadastro.html')

# Página de login (Só vai funcionar se o usuário tiver cadastrado!)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email_user']
        senha = request.form['senha_user']
        conecxao = obter_conecxao()
        user = conecxao.execute('SELECT hash_senha FROM usuarios WHERE email = ?', (email,)).fetchone()
        if user and check_password_hash(user[0], senha):
            conecxao.close()
            return redirect(url_for('home'))
        else:
            conecxao.close()
            return "Email ou senha incorretos!"
    else:
        return render_template('pages/login.html')

# Página Home
# Porteger essa rota!
@app.route('/home', methods=['GET', 'POST'])
# @login_required
def home():
    return render_template("home.html")

# Fazer logout!
# Proteger essa rota
@app.route('/logout')
def logout():
    # Acho que isso já faz logout, mas primeiro temos que criar a sessão do usuário!
    # logout_user() 
    # return render_template('index.html')
    pass
