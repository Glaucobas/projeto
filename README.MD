# Projeto financial_3

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