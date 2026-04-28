from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, insert, text
from datetime import datetime

import time
from functools import wraps
def medir_tempo(func):
    """Decorator que mede o tempo de execução de uma função."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  # tempo inicial (mais preciso que time.time)
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()     # tempo final
        duracao = fim - inicio
        print(f"⏱ Função '{func.__name__}' executada em {duracao:.6f} segundos.")
        return resultado
    return wrapper

engine = create_engine("postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2", echo=False)
metadata = MetaData()

usuarios = Table(
    'usuarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50), nullable=False, index=True),
    Column('cpf', String(14), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('telefone', String(20), nullable=False),
    Column('data_nascimento', Date, nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)

@medir_tempo
def LGPD(row):
    r = row._mapping
    id= r['id']
    nome = r['nome']
    cpf= r['cpf']
    email= r['email']
    telefone = r['telefone']
    data_nascimento = r['data_nascimento']
    created_on = r['created_on']
    updated_on = r['updated_on']

    nomeS = nome.split()
    nomeS[0] = nomeS[0][0] + '*' * (len(nomeS[0]) - 1)
    nome = ' '.join(nomeS)

    cpf = cpf[:3] + '.***.***-**'

    local, dominio = email.split('@', 1)
    email = local[0] + '*' * (len(local) - 1) + '@' + dominio

    digitos = ''.join(c for c in telefone if c.isdigit())
    telefone = digitos[-4:]

    return (id, nome, cpf, email, telefone, data_nascimento, created_on, updated_on)

users = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 5;"))
    for row in result:
        row = LGPD(row)
        users.append(row)

for user in users:
    print(user)
