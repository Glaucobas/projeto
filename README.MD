# Projeto financial 3

## dicas de uso

### **1. Clonar o Repositório**
Utilize o comando abaixo para clonar o repositório:
```bash
git clone https://github.com/Glaucobas/projeto.git
```

### **2. docker**
Acesse o diretório raiz do projeto:
Na pasta principal do projeto foi disponibilizado um arquivo docker-compose.yml.

### **3. Para testar o funcionamento **
O projeto tem três pastas principais.
financial_frontend - com os arquivos do frontend.

financial_api_proxy - serve como ponte entre o frontend e o restante do projeto. Sem essa API o frontend não consegue se comunicar com as outras APIs.

financial_api_transaction - responsavel pelo tratamento dos dados e pela comunicação com o banco.

### **3. Preenchimento automatizado **
A coluna "Categoria" é quem receberá os dados vindos dos modelos. Ao inserir e salvar os dados a descrição da transação é enviada para os 4 modelos que irão fazer a classificação independente um do outro. Um sistema de votção recebe os quatro resultados e veririca qual foi a categoria mais votada. Se ao menos dois modelos estiverem de acordo com a classificação, ela será enviada para ser salva no banco. Se não houver um concenso e os quatro modelos não chegarem a um acordo, a categoria gravada será "CND".

### **4. Preenchimento automatizado **
A pasta "financial_api_transaction" possui dois testes um automatizado e outro semiautomatizado.
test_app.py - Este teste é um pytest e verifica o retorno dos quatro modelos.

Para rodar o teste:
Acesse o diretório raiz do projeto:
```bash
cd financial_api_transaction
```
e uso o comando:
```bash
pytest test_app.py
```
test_modelo - Este teste roda o teste dos modelos onde é verificado se os arquivos estão sendo carregados, a resposta dos modelos a uma lista simples de classificação e um teste interativo onde é possível escrever a descrição e verificar como os quatro modelos e o sistema de votação estão reagindo.
Para rodar o teste:
Acesse o diretório raiz do projeto:
```bash
cd financial_api_transaction
```
e uso o comando:
```bash
python test_modelo.py
```

### **4. Considerações **
As APIs são independente e não precisam estar todas rodando para que o sistema funcione.
Os modelos foram implementados somente na API financial_api_transaction que possui banco de dados proprio.

## Estrutura de pastas

Abaixo está a estrutura básica do projeto:
```
financial_3/
├──finfinancial_frontend /
│  ├── index.html              # Arquivo principal
│  ├── css /                   # Definição de estilos
│  │   └── style.css           # arquivo de estilos
│  ├── imagens /               # imagens
│  │   └──trash.png            # arquivo de imagem
│  ├── js /                    # pasta de regras
│  │   └── script.js           # automação, conexão com as apis
│  ├── Dockerfile              # Configuração do container
│  └── README.md               # Documentação
│
├──Financial_api_proxy/
│  ├── app.py                  # Arquivo principal
│  ├── constants /             # Definição das variaveis globais
│  │   ├── authentication.py   # Variaveis de autenticação
│  │   ├── message.py          # Mensagem
│  │   └── url.py              # arquivo de conexões
│  ├── logs/                   # Arquivos de logs
│  │   └── app.log             # Logs
│  ├── schemas                 # Dependências do projeto
│  │   ├── __init__.py         # Inicialização das rotas
│  │   ├── error.py            # erros 
│  │   └── schema.py           # esquemas de dados
│  ├── requirements.txt        # Dependências do projeto
│  ├── Dockerfile              # Configuração do container
│  └── README.md               # Documentação
│
├──financial_api_account /
│  ├── app.py                   # Arquivo principal
│  ├── database/                # Pasta do Banco de dados
│  │   └── db.sqlite3           # Banco de dados
│  ├── log/                     # Pasta de logs
│  │   └── app.log              # logs
│  ├── models/                  # Definições do banco de dados
│  │   ├── __init__.py          # Inicialização do banco
│  │   └── table.py             # Definição das tabelas
│  ├── schemas/                 # Definição dos endpoints
│  │   ├── __init__.py          # Inicialização dos endpoints
│  │   └── table.py             # Definição das tabelas
│  ├── requirements.txt         # Dependências do projeto
│  ├── Dockerfile               # Configuração do container
│  └── README.md                # Documentação
│                               
├──financial_api_bank /         
│  ├── app.py                   # Arquivo principal
│  ├── database/                # Pasta do Banco de dados
│  │   └── db.sqlite3           # Banco de dados
│  ├── log/                     # Pasta de logs
│  │   └── app.log              # logs
│  ├── models/                  # Definições do banco de dados
│  │   ├── __init__.py          # Inicialização do banco
│  │   └── table.py             # Definição das tabelas
│  ├── schemas/                 # Definição dos endpoints
│  │   ├── __init__.py          # Inicialização dos endpoints
│  │   └── table.py             # Definição das tabelas
│  ├── requirements.txt         # Dependências do projeto
│  ├── Dockerfile               # Configuração do container
│  └── README.md                # Documentação
│                               
├──financial_api_branch /       
│  ├── app.py                   # Arquivo principal
│  ├── database/                # Pasta do Banco de dados
│  │   └── db.sqlite3           # Banco de dados
│  ├── log/                     # Pasta de logs
│  │   └── app.log              # logs
│  ├── models/                  # Definições do banco de dados
│  │   ├── __init__.py          # Inicialização do banco
│  │   └── table.py             # Definição das tabelas
│  ├── schemas/                 # Definição dos endpoints
│  │   ├── __init__.py          # Inicialização dos endpoints
│  │   └── table.py             # Definição das tabelas
│  ├── requirements.txt         # Dependências do projeto
│  ├── Dockerfile               # Configuração do container
│  └── README.md                # Documentação
│                               
├──financial_api_bank /         
│  ├── app.py                   # Arquivo principal
│  ├── database/                # Pasta do Banco de dados
│  │   └── db.sqlite3           # Banco de dados
│  ├── log/                     # Pasta de logs
│  │   └── app.log              # logs
│  ├── models/                  # Definições do banco de dados
│  │   ├── __init__.py          # Inicialização do banco
│  │   └── table.py             # Definição das tabelas
│  ├── schemas/                 # Definição dos endpoints
│  │   ├── __init__.py          # Inicialização dos endpoints
│  │   └── table.py             # Definição das tabelas
│  ├── requirements.txt         # Dependências do projeto
│  ├── Dockerfile               # Configuração do container
│  └── README.md                # Documentação
│                               
├──financial_api_resource /     
│  ├── app.py                   # Arquivo principal
│  ├── database/                # Pasta do Banco de dados
│  │   └── db.sqlite3           # Banco de dados
│  ├── log/                     # Pasta de logs
│  │   └── app.log              # logs
│  ├── models/                  # Definições do banco de dados
│  │   ├── __init__.py          # Inicialização do banco
│  │   └── table.py             # Definição das tabelas
│  ├── schemas/                 # Definição dos endpoints
│  │   ├── __init__.py          # Inicialização dos endpoints
│  │   └── table.py             # Definição das tabelas
│  ├── requirements.txt         # Dependências do projeto
│  ├── Dockerfile               # Configuração do container
│  └── README.md                # Documentação
│                               
└──financial_api_transaction /
   ├── app.py                   # Arquivo principal
   ├── database/                # Pasta do Banco de dados
   │   └── db.sqlite3           # Banco de dados
   ├── log/                     # Pasta de logs
   │   └── app.log              # logs
   ├── models/                  # Definições do banco de dados
   │   ├── __init__.py          # Inicialização do banco
   │   └── table.py             # Definição das tabelas
   ├── schemas/                 # Definição dos endpoints
   │   ├── __init__.py          # Inicialização dos endpoints
   │   └── table.py             # Definição das tabelas
   ├── requirements.txt         # Dependências do projeto
   ├── Dockerfile               # Configuração do container
   └── README.md                # Documentação
```
