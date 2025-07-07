```markdown
# API

O objetivo da construção desta API é modularizar o projeto, dividindo a aplicação em microserviços. Cada microserviço é capaz de trabalhar de forma independente com suas requisições. A função principal desta API e de sevi como ponte para a conexão com as outras APIs recebendo as rquisições e as direcionando para o destino.

---

## Estrutura do Projeto

- **app.py**: Arquivo principal para execução da API.
- **constants/**: Contém as definições globais do sistema.
- **logs/**: contem os logs do sistma.
- **requirements.txt**: Lista de dependências necessárias para executar a aplicação.
- **Dockerfile**: Configuração para criar o container Docker da aplicação.
- **README.md**: Documentação completa da API.

---

## Pré-requisitos

1. **Python**: Certifique-se de que você tenha o Python 3.8 ou superior instalado.
2. **Docker**: Para execução em container, é necessário que o Docker esteja instalado e configurado.
3. **Ambiente Virtual**: É recomendado criar um ambiente virtual para evitar conflitos entre bibliotecas.

---

## APIs externas
Foram implemetadas duas APIs externas: 
1. ** Consulta de CEPs **: A API foi implementada para auxiliar no cadastro de agências bancárias onde, caso o usuário digite somente o CEP, a API busca os dados restantes complementando o cadastro. Esta API esta implementada m financial_api_branch.
2. ** Consultas de Instituições Bancárias **: Esta API retornas as informaçõs das instituiçõs financeiras a partir do código junto ao banco central. Esta API esta implementada em financial_api_bank.


## Passo a Passo para Instalação e Uso

### **1. Clonar o Repositório**
Utilize o comando abaixo para clonar o repositório:
```bash
git clone https://github.com/Glaucobas/financial_api_proxy.git
```

### **2. Navegar para o Diretório do Projeto**
Acesse o diretório raiz do projeto:
```bash
cd financial_api_proxy
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
flask run --host 0.0.0.0 --port 5000 --reload
```

Se tudo estiver configurado corretamente, a API será inicializada e estará acessível no endereço:
```
http://127.0.0.1:5000
```

---

## Uso com Docker

### **1. Instalar Docker**
Certifique-se de que o Docker esteja instalado e funcionando em sua máquina. Para instruções, acesse [Instalação do Docker](https://www.docker.com/get-started).

### **2. Construir o Container**
No diretório raiz do projeto, execute o comando:
```bash
docker build -t financial_api_proxy .
```

### **3. Executar o Container**
Para rodar o container criado:
```bash
docker run -d -p 5000:5000 --name financial_api_proxy financial_api_proxy
```

### **4. Verificar o Status do Container**
Certifique-se de que o container está rodando:
```bash
docker ps
```

### **5. Acessar a API no Docker**
Com o container rodando, a API estará disponível no mesmo endereço:
```
http://127.0.0.1:5000
```

---

## Estrutura de Diretórios

Abaixo está a estrutura básica do projeto:
```
financial_api_proxy/
├── app.py                  # Arquivo principal
├── constants /             # Definição das variaveis clobais
│   ├── authentication.py   # Variaveis de autenticação
│   ├── message.py          # Mensagem
│   └── url.py              # arquivo de conexões
├── logs/                   # Arquivos de logs
│   └── app.log             # Logs
├── schemas                 # Dependências do projeto
│   ├── __init__.py         # Inicialização das rotas
│   ├── error.py            # erros 
│   └── schema.py           # esquemas de dados
├── requirements.txt        # Dependências do projeto
├── Dockerfile              # Configuração do container
└── README.md               # Documentação

```

---

## Endpoints Disponíveis

1. **GET /health-check**
   - Verifica o status da API.

2. **POST /create**
   - Cria um novo registro no banco de dados.

3. **PUT /update**
   - Atualiza um registro existente.

4. **DELETE /delete**
   - Remove um registro do banco.

---

## Dicas Adicionais

- **Log de Erros**:
  Certifique-se de verificar os logs de execução na pasta `logs/` caso ocorra algum erro.

- **Ambiente Virtual**:
  Sempre ative o ambiente virtual antes de executar qualquer comando para instalar bibliotecas ou rodar a API.