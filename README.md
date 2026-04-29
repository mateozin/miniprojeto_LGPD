# miniprojeto_LGPD
Um algoritimo que lista 5 Usuários de um banco de dados, os usuarios listados no começo tem seus dados escondidos, ele também cria um .csv por ano e inclui todos os usuários do banco de dados, utilizando os dados anônimos, em seus respectivos anos. Agora o código cria um outro .csv que inclui todos os usuários do banco de dados, utilizando os dados reais, chamado todos.csv. É criado também um .log listando o tempo que leva para cada função ser realizada.
# Como Usar? (Windows)
Crie um ambiente virtual na pasta do arquivo e ative-o
```
python -m venv .venv
.venv\Scripts\activate
```
*O Python 3.13+ pode apresentar problemas ao instalar os requirements.txt, caso esse seja o caso crie um .venv usando o Python 3.11* *
Instale os "requirements.txt"
```
pip install -r requirements.txt
```
Execute o algoritimo estando na pasta correta no terminal utilizando o comando 
```
python LGPD.py
```
As pastas serão criadas no caminho do código e os 5 usuários serão listados no console. 

* Caso tenha problemas ao baixar o 'requirements.txt', utilize esses comandos:
/Comando para instalar o Python 3.11 (Windows)
```
winget install Python.Python.3.11 
```
Comando para criar o venv com a versão desejada e ativar
```
py -3.11 -m venv .venv
.venv\Scripts\activate
```
Agora instale os 'requirements.txt' e execute o código.
```
pip install -r requirements.txt
python LGPD.py
```
\Comando para instalar o Python 3.11 (Linux)
```
sudo apt update
sudo apt install python3.11
```
Comando para criar o venv com a versão desejada e ativar
```
python3.11 -m venv .venv
source .venv/bin/activate
```
Baixar os 'requirements.txt' e executar o código
```
pip install -r requirements.txt
python3 LGPD.py
```
Agora o código deve executar apropriadamente.
