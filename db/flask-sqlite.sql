-- Código sqlite 🪶 pra criar a tabelas (Se ela não existir)
create table if not exists usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT, --ID (O banco mesmo que cria)
    nome TEXT NOT NULL, --Nome (É passao pro banco)
    email TEXT NOT NULL UNIQUE, --E-mail (É passao pro banco e tem que ser um valor unico)
    senha TEXT NOT NULL --Senha (É passao pro banco)
);
