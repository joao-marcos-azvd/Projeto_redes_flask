# Código usado pra criar/iniciar o banco 
# Tem que rodar no terminal python ( python <nome_do_arquivo> )
import sqlite3

# Cria uma conexão com o banco e cria o banco "database.bd"
conn = sqlite3.connect('database/database.db')   
# Pega o códifo dentro de 'db/flask-sqlite.sql' e executa, criando as tabelas
with open('db/flask-sqlite.sql') as arquivo:
    conn.executescript(arquivo.read())
    # Fecha o banco
    conn.close()
