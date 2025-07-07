# API Category

O objetivo da construção desta API é modularizar o projeto, dividindo a aplicação em microserviços. Cada microserviço é capaz de trabalhar de forma independente com suas requisições. A API possui um banco de dados próprio (SQLite) e gerencia todas as operações de gravação, atualização e remoção de dados.

---

## Estrutura do Projeto

- **app.py**: Arquivo principal para execução da API.
- **models/**: Contém as definições das tabelas e a configuração do banco de dados.
- **schema/**: Define os esquema dos dados.
- **requirements.txt**: Lista de dependências necessárias para executar a aplicação.
- **Dockerfile**: Configuração para criar o container Docker da aplicação.
- **README.md**: Documentação completa da API.

---

## Pré-requisitos

1. **Python**: Certifique-se de que você tenha o Python 3.8 ou superior instalado.
2. **SQLite**: O SQLite já vem integrado com o Python e será utilizado como banco de dados.
3. **Docker**: Para execução em container, é necessário que o Docker esteja instalado e configurado.
4. **Ambiente Virtual**: É recomendado criar um ambiente virtual para evitar conflitos entre bibliotecas.

---

## Passo a Passo para Instalação e Uso

### **1. Clonar o Repositório**
Utilize o comando abaixo para clonar o repositório:
```bash
git clone https://github.com/Glaucobas/financial_api_category.git
```

### **2. Navegar para o Diretório do Projeto**
Acesse o diretório raiz do projeto:
```bash
cd financial_api_category
```

### **3. Criar e Ativar Ambiente Virtual**
Crie um ambiente virtual usando o comando:
```bash
python -m venv env
```
Ative o ambiente virtual:
- **Windows**:
  ```bash
  env\Scripts\activate
  ```
- **Linux/Mac**:
  ```bash
  source env/bin/activate
  ```

### **4. Atualizar o `pip` (Recomendado)**
Atualize o gerenciador de pacotes pip:
```bash
python -m pip install --upgrade pip
```

### **5. Instalar Dependências**
Instale as bibliotecas necessárias com o seguinte comando:
```bash
pip install -r requirements.txt
```

### **6. Executar a API**
Após instalar as dependências, execute a aplicação:
```bash
flask run --host 0.0.0.0 --port 5001 --reload
```

Se tudo estiver configurado corretamente, a API será inicializada e estará acessível no endereço:
```
http://127.0.0.1:5001
```

---

## Uso com Docker

### **1. Instalar Docker**
Certifique-se de que o Docker esteja instalado e funcionando em sua máquina. Para instruções, acesse [Instalação do Docker](https://www.docker.com/get-started).

### **2. Construir o Container**
No diretório raiz do projeto, execute o comando:
```bash
docker build -t financial_api_category .
```

### **3. Executar o Container**
Para rodar o container criado:
```bash
docker run -d -p 5001:5001 --name financial_api_category financial_api_category
```

### **4. Verificar o Status do Container**
Certifique-se de que o container está rodando:
```bash
docker ps
```

### **5. Acessar a API no Docker**
Com o container rodando, a API estará disponível no mesmo endereço:
```
http://127.0.0.1:5001
```

---

## Estrutura de Diretórios

Abaixo está a estrutura básica do projeto:
```
financial_api_bank /
├── app.py               # Arquivo principal
├── database/            # Pasta do Banco de dados
│   └── db.sqlite3       # Banco de dados
├── log/                 # Pasta de logs
│   └── app.log          # logs
├── models/              # Definições do banco de dados
│   ├── __init__.py      # Inicialização do banco
│   └── table.py         # Definição das tabelas
├── schemas/             # Definição dos endpoints
│   ├── __init__.py      # Inicialização dos endpoints
│   └── table.py         # Definição das tabelas
├── requirements.txt     # Dependências do projeto
├── Dockerfile           # Configuração do container
└── README.md            # Documentação
```

---

## Endpoints Disponíveis

1. **GET /category**
   - Lista todos os registros do banco de dados.

2. **POST /category**
   - Cria um novo registro no banco de dados.

3. **PUT /category**
   - Atualiza um registro existente.

4. **DELETE /category**
   - Remove um registro do banco.

---

## Dicas Adicionais

- **Log de Erros**:
  Certifique-se de verificar os logs de execução na pasta `logs/` caso ocorra algum erro.

- **Ambiente Virtual**:
  Sempre ative o ambiente virtual antes de executar qualquer comando para instalar bibliotecas ou rodar a API.