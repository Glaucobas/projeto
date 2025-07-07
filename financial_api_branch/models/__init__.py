import os
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# importando os elementos definidos no modelo
from models.table import Base

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///database/db.sqlite3'

# Verifica se o diretório existe, caso contrário, cria-o
os.makedirs(os.path.dirname(db_url.split('///')[1]), exist_ok=True)

try:
    # cria a engine de conexão com o banco
    engine = create_engine(db_url, echo=False)

    # Instancia um criador de sessão com o banco
    Session = sessionmaker(bind=engine)

    # cria o banco se ele não existir 
    if not database_exists(engine.url):
        create_database(engine.url)

    # cria as tabelas do banco, caso não existam
    Base.metadata.create_all(engine)

except Exception as e:
    print(f"Ocorreu um erro: {e}")
