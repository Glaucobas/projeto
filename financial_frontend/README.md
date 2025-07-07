# FRONTEND

## Estrutura Básica
- HTML:- Serve como a base do frontend, definindo a estrutura dos elementos da interface.
- Exemplo: Criação de botões, caixas de texto, e áreas onde os dados das APIs serão exibidos, como tabelas ou seções dinâmicas.

- CSS:- Responsável pela estilização, adicionando cores, fontes, margens e layouts.
- Exemplo: Tornar o frontend visualmente atrativo e responsivo para diferentes dispositivos.

- JavaScript:- Realiza a lógica principal, conectando o frontend às APIs externas.
- É usado para fazer requisições HTTP (fetch ou XMLHttpRequest) e tratar os dados retornados das APIs.
- Atualiza dinamicamente a interface com base nos dados recebidos.

## Funcionamento
- Requisições simultâneas: Usando JavaScript, o frontend faz chamadas simultâneas para várias APIs usando Promise.all().
- Manipulação de dados: Os dados retornados são processados e exibidos dinamicamente em seções específicas da interface.
- Estilização simples: O CSS básico garante que os elementos sejam organizados e esteticamente agradáveis.

---

## Estrutura do Projeto

- **index.html**: Arquivo principal para execução da página.
- **ccs/**: Contém as páginas de estilo.
- **js/**: Contém as regras para coneção com as Apis e tratamento dos dados.
- **Dockerfile**: Configuração para criar o container Docker da aplicação.
- **README.md**: Documentação completa da API.

---

## Pré-requisitos

1. **Python**: Certifique-se de que você tenha o Python 3.8 ou superior instalado.
2. **Docker**: Para execução em container, é necessário que o Docker esteja instalado e configurado.
3. **Ambiente Virtual**: É recomendado criar um ambiente virtual para evitar conflitos entre bibliotecas.

---

## Passo a Passo para Instalação e Uso

### **1. Clonar o Repositório**
Utilize o comando abaixo para clonar o repositório:
```bash
git clone https://github.com/Glaucobas/financial_frontend.git
```

### **2. Navegar para o Diretório do Projeto**
Acesse o diretório raiz do projeto:
```bash
cd financial_frontend
```

## Uso com Docker

### **1. Instalar Docker**
Certifique-se de que o Docker esteja instalado e funcionando em sua máquina. Para instruções, acesse [Instalação do Docker](https://www.docker.com/get-started).

### **2. Construir o Container**
No diretório raiz do projeto, execute o comando:
```bash
docker build -t aplicacao-web-nginx .
```

### **3. Executar o Container**
Para rodar o container criado:
```bash
docker run -d -p 8080:80 aplicacao-web-nginx
```

### **4. Verificar o Status do Container**
Certifique-se de que o container está rodando:
```bash
docker ps
```

### **5. Acessar a API no Docker**
Com o container rodando, a API estará disponível no mesmo endereço:
```
http://127.0.0.1:8080
```

---

## Estrutura de Diretórios

Abaixo está a estrutura básica do projeto:
```
finfinancial_frontend /
├── index.html              # Arquivo principal
├── css /                   # Definição de estilos
│   └── style.css           # arquivo de estilos
├── imagens /               # imagens
│   └──trash.png            # arquivo de imagem
├── js /                    # pasta de regras
│   └── script.js           # automação, conexão com as apis
├── Dockerfile              # Configuração do container
└── README.md               # Documentação

```

## Dicas Adicionais

- **Log de Erros**:
  Certifique-se de verificar os logs de execução na pasta `logs/` caso ocorra algum erro.

- **Ambiente Virtual**:
  Sempre ative o ambiente virtual antes de executar qualquer comando para instalar bibliotecas ou rodar a API.