# Importando coisas do Flask
from flask import Flask, render_template, request, redirect, url_for
# Importando flask_login pra validar usuários, fazer logout e proteger as rotas
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user #Tenho que vê como eu mexo nisso!
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
    def __init__(self, id, nome, email):
        self.id = id
        self.nome = nome
        self.email = email

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
    conecxao = obter_conecxao()
    user = conecxao.execute("SELECT id, nome, email FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    conecxao.close()
    if user:
        return User(id=user[0], nome=user[1], email=user[2])  # Retorna o usuário com os dados do banco
    return None

# Página inicial
@app.route('/')
def index():
    return render_template('pages/index.html')

# Página de cadastro (Só funciona de o usuário não tiver no banco!)
# Tem que adicionar login_manager aqui
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome_user']
        email = request.form['email_user']
        hash_senha = generate_password_hash(request.form['senha_user']) 
        with obter_conecxao() as conecxao: 
            users = conecxao.execute('SELECT email FROM usuarios').fetchall()
            # Verifica se o usuário não está cadastrado
            for e_user in users:
                if email == e_user[0]:
                    return """
                    <p>Usuário já cadastrado!</p>
                    <p><a href="/">Clique aqui para voltar!</a></p>
                    """
            conecxao.execute("INSERT INTO usuarios (nome, email, hash_senha) VALUES (?, ?, ?)", (nome, email, hash_senha))
            conecxao.commit()
        conecxao = obter_conecxao()
        user = conecxao.execute('SELECT id FROM usuarios WHERE email = ?', (email,)).fetchone()
        user_obj = User(id=user[0], nome=nome, email=email)
        conecxao.close()
        login_user(user_obj)  # Usando login_user para criar a sessão
        return redirect(url_for('home'))
    else:
        return render_template('pages/cadastro.html')

# Página de login (Só vai funcionar se o usuário tiver cadastrado!)
# Colocando o flask-login aqui!
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email_user']
        senha = request.form['senha_user']
        conecxao = obter_conecxao()
        user = conecxao.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()

        if user and check_password_hash(user[3], senha):  # Verificando senha
            conecxao.close()
            user_obj = User(id=user[0], nome=user[1], email=user[2])
            login_user(user_obj)  # Usando login_user para criar a sessão
            return redirect(url_for('home'))
        else:
            conecxao.close()
            return """
            <p>Email ou senha incorretos!</p>
            <p><a href="/login">Click aqui para voltar!</a></p>
            """
    else:
        return render_template('pages/login.html')

# Página Home
# Porteger essa rota!
@app.route('/home')
@login_required
def home():
    nome_usuario = current_user.nome
    return render_template("pages/home.html", nome = nome_usuario) #, nome = User['nome'])

@app.route('/prestou')
@login_required
def prestou():
    return render_template('pages/prestou.html')

# Fazer logout!
# Proteger essa rota
@app.route('/logout')
def logout():
    logout_user()  # Desconecta o usuário
    return redirect(url_for('index'))  # Redireciona para a página inicial após o logout
