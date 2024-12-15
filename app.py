# Importando coisas do Flask
from flask import Flask, render_template, request, redirect, url_for
# Importando biblioteca de hash de senha
from werkzeug.security import generate_password_hash, check_password_hash
# Importando sqlite3
import sqlite3

app = Flask(__name__)
# Definição de sesão no Flask
app.config['SECRET_KEY'] = 'S_U_P_E_R_S_E_C_R_E_T_O_1_2_3'

def obter_conecxao():
    # Conectando o banco
    conn = sqlite3.connect('database.db') 
    # Configuração pra pegar os dados do banco na forma de dicionário
    conn.row_factory = sqlite3.Row
    # Retornando conexão
    return conn

# Página inicial
@app.route('/')
def index():
    return render_template('pages/index.html')

# Página de cadastro (Só funciona de o usuário não tiver no banco!)
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form['nome_user']
        email = request.form['email_user']
        hash_senha = generate_password_hash(request.form['senha_user']) 
        conecxao = obter_conecxao()
        users = conecxao.execute('SELECT email FROM usuarios').fetchall()
        # Verifica se o usuário não está cadastrado!
        for e_user in users:
            if email == e_user[0]:
                conecxao.close()
                return redirect(url_for('index'))
            else:
                conecxao.execute("INSERT INTO usuarios(nome, email, hash_senha) VALUES(?, ?, ?)", (nome, email, hash_senha,))
                conecxao.commit()
                conecxao.close()
                return redirect(url_for("home"))
    else:
        return render_template('pages/cadastro.html')

# Página de login (Só vai funcionar se o usuário tiver cadastrado!)
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return "Opa! Testando!"
