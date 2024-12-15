# Importando coisas do Flask
from flask import Flask, render_template
# Importando sqlite3
import sqlite3

app = Flask(__name__)

def obter_conexao():
    # Conectando o banco
    conn = sqlite3.connect('Redes/projetos_flask/database.db') # Editar esse caminho, porque ele é referente a meu repositório
    # Configuração pra pegar os dados do banco na forma de dicionário
    conn.row_factory = sqlite3.Row
    # Retornando conexão
    return conn

@app.route('/')
def index():
    return render_template('index.html')