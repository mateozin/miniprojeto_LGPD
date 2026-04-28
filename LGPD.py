from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, insert, text
from datetime import datetime

import time
import csv
from functools import wraps
from collections import defaultdict

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
def anon_nome(row):
    r = row._mapping
    nome=r['nome']
    nomeS=nome.split()
    nomeS[0]=nomeS[0][0] + '*' * (len(nomeS[0]) - 1)
    return nome
def anon_cpf(row):
    r = row._mapping
    cpf=r['cpf']
    cpf = cpf[:3] + '.***.***-**'
    return cpf
def anon_email(row):
    r = row._mapping
    email=r['email']
    local,dominio=email.split('@', 1)
    email = local[0] + '*' * (len(local)-1) + '@' + dominio
    return email
def anon_telefone(row):
    r = row._mapping
    telefone=r['telefone']
    digitos=''.join(c for c in telefone if c.isdigit())
    telefone = digitos[-4:]
    return telefone
def LGPD(row):
    r = row._mapping
    id= r['id']
    data_nascimento = r['data_nascimento']
    created_on = r['created_on']
    updated_on = r['updated_on']
    return (id, anon_nome(row), anon_cpf(row), anon_email(row), anon_telefone(row), data_nascimento, created_on, updated_on)
def LGPD_ALL(row):
    return row

@medir_tempo
def gerar_por_ano(users):
    por_ano = defaultdict(list)
    for u in users:
        ano = u[5].year #indice 5 (data_nascimento)
        por_ano[ano].append(u)

    for ano, registros in por_ano.items():
        nome_arquivo = f'{ano}.csv'
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'nome', 'cpf', 'email', 'telefone', 'data_nascimento', 'created_on', 'updated_on'])
            writer.writerows(registros)
        print(f"'{nome_arquivo}' gerado com {len(registros)} usuários.")
@medir_tempo
def gerar_todos(users):
        nome_arquivo = f'todos.csv'
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'nome', 'cpf', 'email', 'telefone', 'data_nascimento', 'created_on', 'updated_on'])
            writer.writerows(users)
        print(f"'{nome_arquivo}' gerado com {len(users)} usuários.")
all_users_anon = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios;"))
    for row in result:
        all_users_anon.append(LGPD(row))
gerar_por_ano(all_users_anon)
all_users = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * from usuarios;"))
    for row in result:
        all_users.append(LGPD_ALL(row))
gerar_todos(all_users)
users=[]
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 5;"))
    for row in result:
        row = LGPD(row)
        users.append(row)
for user in users:
    print(user)