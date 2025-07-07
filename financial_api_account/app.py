from flask import Flask, jsonify, redirect, request
from flask_openapi3 import OpenAPI, Info, Tag, APIBlueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import Session
from models.table import Accounts
from sqlalchemy.exc import IntegrityError, DataError
from schemas.table import AccountsViewSchema, AccountsDelSchema, AccountsSchema
from schemas.table import AccountsSearchSchema, ListAccountsSchema
from schemas.error import ErrorSchema
from functools import wraps

import logging, requests

# Cria um logger
logger = logging.getLogger(__name__) 
logger.setLevel(logging.DEBUG)

# Cria um handler para o console 
console_handler = logging.StreamHandler() 
console_handler.setLevel(logging.DEBUG)

# Cria um handler para um arquivo 
file_handler = logging.FileHandler('./log/app.log') 
file_handler.setLevel(logging.WARNING) 

# Define um formatador 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
console_handler.setFormatter(formatter) 
file_handler.setFormatter(formatter) 

# Adiciona os handlers ao logger 
logger.addHandler(console_handler) 
logger.addHandler(file_handler)

# Configuração da aplicação Flask
info = Info(title="Financeiro", version="2.0.0")
app = OpenAPI(__name__, info=info)

# Constantes
ERRO_DE_INTEGRIDADE = "Erro de integridade"
ERRO_DADOS = "Dados fornecidos inválidos"
CORS(app)  # Configuração segura do CORS

# Configuração do JWT para autenticação
app.config["JWT_SECRET_KEY"] = "banana"
jwt = JWTManager(app)

# Crie um blueprint para a financial_api_account
account_api = APIBlueprint('financial_api_account', __name__)

#define tags
documentation_tag = Tag(name="Documentação", description="Seleção de documentação: Swager")
home_tag = Tag(name="Inicial", description="Página Inicial")
account_tag = Tag(name="Contas", description="Adição, visualização e remoção de Accounts da base")

# Registre o blueprint na aplicação principal
app.register_api(account_api)

#**************************************************************************************************
#* MIDDLEWARE                                                                                     *
#**************************************************************************************************
@app.before_request
def validate_token():
    if request.endpoint in ['documentation', 'static']:  # Exclui rotas públicas
        return
    
    try:
        # Busca o token no cabeçalho da requisição
        token = request.headers.get("Authorization")
        if not token or token != f"Bearer {app.config['JWT_SECRET_KEY']}":
            logger.warning("Token inválido ou não corresponde à secret-key.")
            return jsonify({"message": "Token inválido ou não autorizado."}), 401
        
    except requests.RequestException as e:
        logger.error(f"Erro ao validar o token: {str(e)}")
        return jsonify({"message": "Erro ao validar o token."}), 500
    
#**************************************************************************************************
#* DECORATOR SESSION                                                                              *
#**************************************************************************************************
def with_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        session = Session()
        try:
            result = f(*args, session=session, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao executar a função {f.__name__}: {str(e)}")
            return jsonify({"message": f"Erro ao executar a função {f.__name__}: {str(e)}"}), 500
        finally:
            session.close()
    return wrapper

#**************************************************************************************************
#* GET                                                                                            *
#**************************************************************************************************
@app.get('/account', tags=[account_tag],
          responses={"200": ListAccountsSchema, "404": ErrorSchema})

@with_session
def get_account(session):
    """
    Faz a busca por todos os itens cadastrado na base de dado.
    """
    logger.debug(f"Requisição recebida: {request.method} {request.path}")

    try:
        accounts = session.query(Accounts).order_by(
            Accounts.account_id,Accounts.branch_id,Accounts.resource_id).all()
        
        if not accounts:
            logger.debug(f"Não há Contas cadastradas {request.method} {request.path}")
            return jsonify({"accounts": []}), 200

        logger.debug(f"{len(accounts)} Contas econtradas {request.method} {request.path}")
        return jsonify({"account": [account.to_dict() for account in accounts]}), 200

    except DataError as e:
        logger.error(f"Erro de dados: {str(e)}")
        return jsonify({"message": "Erro de dados"}), 400
    
    except IntegrityError as e:
        logger.error(f"Erro de integridade: {str(e)}")  
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409
    
    except Exception as e:
        logger.error(f"Erro no servidor: {str(e)}") 
        return jsonify({"message": f"Erro no servidor: {str(e)}"}), 500

#**************************************************************************************************
#* POST                                                                                     *
#**************************************************************************************************
@app.post('/account', tags=[account_tag],
          responses={"200": AccountsViewSchema, "409": ErrorSchema, "400": ErrorSchema})

@with_session
def add_account(body: AccountsSchema, session):
    """ 
    Adiciona um item na base de dados a partir de uma requisição externa.
    """
    try:
        # Obtém os dados enviados pela API externa (via JSON no corpo da requisição)
        account_data = request.get_json()
        
        if not account_data or not account_data.get("account_id"):
            logger.error("Dados inválidos ou ausentes na requisição")
            return jsonify({"status": "falha", "mensagem": "Dados inválidos ou ausentes"}), 400

        # Cria o objeto da categoria a partir dos dados recebidos
        account = Accounts(
            account_id=account_data.get("account_id"),
            branch_id=account_data.get("branch_id"),
            resource_id=account_data.get("resource_id")
        )

        # Adiciona a categoria no banco de dados
        session.add(account)
        logger.debug(f"Conta adicionada com sucesso: '{account}'")
        return jsonify({"status": "sucesso", "mensagem": "Dados gravados com sucesso"}), 200

    except IntegrityError as e:
        logger.error(f"Erro de integridade: {str(e)} - Erro de duplicidade ou restrição de chave.")
        return jsonify({"status": "falha", "mensagem": "Erro de duplicidade ou restrição de chave."}), 409

    except DataError as e:
        logger.error(f"Erro de dados: {str(e)}")
        return jsonify({"status": "falha", "mensagem": "Dados inválidos fornecidos"}), 400

    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return jsonify({"status": "falha", "mensagem": f"Erro no servidor: {str(e)}"}), 500
    
#**************************************************************************************************
#* DELETE                                                                                     *
#**************************************************************************************************
@app.delete('/account', tags=[account_tag], 
            responses={"200": AccountsDelSchema, "404": ErrorSchema})

#@jwt_required()
@with_session
def del_account(body: AccountsSearchSchema, session):
    """ 
    Apaga um item da base de dados a partir do seu identificador 
    """
    
    account_data = request.get_json()
    account_id = account_data.get("account_id")
    resource_id = account_data.get("resource_id")
    branch_id = account_data.get("branch_id")
    logger.debug(f"Apagando dados sobre a Conta #{account_id}")
   
    try: 
        count = session.query(Accounts).filter(
                Accounts.account_id == account_id,
                Accounts.branch_id == branch_id,
                Accounts.resource_id == resource_id).delete()

        if count:
            logger.debug(f"Conta removida #{account_id}")
            return jsonify({"message": "Conta removida", "id": account_id}), 200
        
        else: 
            # se a categoria não foi encontrado
            logger.warning(f"Erro ao deletar Contas #'{account_id}'")
            return {"message": f"Erro ao deletar Contas #'{account_id}'"}, 400 
    
    except IntegrityError as e: 
        logger.error(f"Erro de integridade: '{account_id}': {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409
    
    except Exception as e:
        logger.error(f"Erro interno do servidor: '{account_id}': {str(e)}") 
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 500
