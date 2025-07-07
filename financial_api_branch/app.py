from flask import Flask, jsonify, redirect, request
from flask_openapi3 import OpenAPI, Info, Tag, APIBlueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import Session
from models.table import Branches
from sqlalchemy.exc import IntegrityError, DataError
from schemas.table import BranchesDelSchema, BranchesViewSchema
from schemas.table import BranchesSchema, BranchesUpdateSchema
from schemas.table import BranchesSearchSchema, ListBranchesSchema
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
info = Info(title="API Branch", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Constantes
ERRO_DE_INTEGRIDADE = "Erro de integridade"
ERRO_DADOS = "Dados inválidos fornecidos"
CORS(app)  # Configuração segura do CORS

# Configuração do JWT para autenticação
app.config["JWT_SECRET_KEY"] = "banana"
jwt = JWTManager(app)

# Crie um blueprint para a financial_api_branch
branch_api = APIBlueprint('branch_api', __name__)

#define tags
documentation_tag = Tag(name="Documentação", description="Seleção de documentação: Swager")
home_tag = Tag(name="Inicial", description="Página Inicial")
branch_tag = Tag(name="Agência", description="Adição, visualização e remoção de Agências da base")

# Registre o blueprint na aplicação principal
app.register_api(branch_api)

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
#* DECORATOR SESSON                                                                               *
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
#* EXTERNAL API                                                                                   *
#**************************************************************************************************  
def get_address_by_cep(cep):
    """
    Consulta um endereço em uma API externa utilizando o CEP informado.
    """
    try:
        # URL da API externa para consulta de CEP
        api_url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(api_url)

        if response.status_code == 200:
            address_data = response.json()
            if "erro" in address_data:
                logger.warning(f"CEP {cep} não encontrado na API externa.")
                return jsonify({"message": "CEP não encontrado"}), 404
            
            logger.debug(f"Endereço encontrado para o CEP {cep}: {address_data}")
            return address_data, 200
        else:
            logger.error(f"Erro ao consultar o CEP {cep}: {response.status_code}")
            return jsonify({"message": "Erro ao consultar o CEP"}), response.status_code

    except requests.RequestException as e:
        logger.error(f"Erro ao realizar a requisição para o CEP {cep}: {str(e)}")
        return jsonify({"message": "Erro ao consultar o CEP"}), 500

#**************************************************************************************************
#* GET                                                                                            *
#************************************************************************************************** 
@app.get('/branch', tags=[branch_tag],
          responses={"200": ListBranchesSchema, "404": ErrorSchema})

@with_session
def get_branch(session):
    """
    Faz a busca por todos os itens cadastrado na base de dado.
    """
    logger.debug(f"Requisição recebida: {request.method} {request.path}")

    try:
        branches = session.query(Branches).order_by(Branches.branch_id).all()
        
        if not branches:
            # se não há Agencias cadastradas
            logger.debug(f"Não há Agências cadastradas {request.method} {request.path}")
            return jsonify({"branch": []}), 200

        logger.debug(f"{len(branches)} Agências econtradas {request.method} {request.path}")
        return jsonify({"branch": [branch.to_dict() for branch in branches]}), 200

    except DataError as e:
        logger.error(f"Dados inválidos fornecidos: {str(e)}")
        return jsonify({"message": ERRO_DADOS}), 400
    
    except IntegrityError as e:
        logger.error(f"Erro de integridade: {str(e)}")  
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409
    
    except Exception as e:
        logger.error(f"Erro no servidor: {str(e)}") 
        return jsonify({"message": f"Erro no servidor: {str(e)}"}), 500

#**************************************************************************************************
#* POST                                                                                           *
#************************************************************************************************** 
@app.post('/branch', tags=[branch_tag],
          responses={"200": BranchesViewSchema, "409": ErrorSchema, "400": ErrorSchema})

@with_session
def add_branch(body: BranchesSchema, session):
    """ 
    Adiciona um item na base de dados a partir de uma requisição externa.
    """
    try:
        # Obtém os dados enviados pela API externa (via JSON no corpo da requisição)
        branch_data = request.get_json()
        
        if not branch_data or not branch_data.get("branch_id"):
            logger.error("Dados inválidos ou ausentes na requisição")
            return jsonify({"status": "falha", "mensagem": "Dados inválidos ou ausentes"}), 400
        
        # Verifica se o campo de endereço está vazio e tenta completar usando o CEP
        if not branch_data.get("branch_address") and branch_data.get("branch_cep"):
            address_data, status_code = get_address_by_cep(branch_data.get("branch_cep"))
            if status_code == 200:
                branch_data["branch_address"] = address_data.get("logradouro", "")
                branch_data["branch_district"] = address_data.get("bairro", "")
                branch_data["branch_city"] = address_data.get("localidade", "")
                branch_data["branch_state"] = address_data.get("uf", "")
                branch_data["branch_country"] = "Brasil"
            else:
                logger.warning(f"Não foi possível completar o endereço para o CEP {branch_data.get('branch_cep')}")

        # Cria o objeto da agências a partir dos dados recebidos
        branch = Branches(
            branch_id=branch_data.get("branch_id"),
            branch_description=branch_data.get("branch_description"),  
            bank_id=branch_data.get("bank_id"),
            branch_cep=branch_data.get("branch_cep"),
            branch_address=branch_data.get("branch_address"),
            branch_number=branch_data.get("branch_number"),
            branch_complement=branch_data.get("branch_complement"),
            branch_district=branch_data.get("branch_district"),
            branch_city=branch_data.get("branch_city"),
            branch_state=branch_data.get("branch_state"),
            branch_country=branch_data.get("branch_country"),
            branch_phone=branch_data.get("branch_phone"),
            branch_email=branch_data.get("branch_email"),
        )
        
        # Adiciona a agências no banco de dados
        session.add(branch)
        logger.debug(f"Agência adicionada com sucesso: '{branch}'")
        return jsonify({
            "bank_id": branch.bank_id,
            "branch_address": branch.branch_address,
            "branch_cep": branch.branch_cep,
            "branch_city": branch.branch_city,
            "branch_complement": branch.branch_complement,
            "branch_country": branch.branch_country,
            "branch_description": branch.branch_description,
            "branch_email": branch.branch_email,
            "branch_id": branch.branch_id,
            "branch_number": branch.branch_number,
            "branch_phone": branch.branch_phone,
            "branch_state": branch.branch_state,
            "status": "sucesso", 
            "mensagem": "Dados gravados com sucesso"}), 200

    except IntegrityError as e:
        logger.error(f"Erro de integridade: {str(e)} - Erro de duplicidade ou restrição de chave.")
        return jsonify({"status": "falha", "mensagem": "Erro de duplicidade ou restrição de chave."}), 409

    except DataError as e:
        logger.error(f"Dados inválidos fornecidos: {str(e)}")
        return jsonify({"status": "falha", "mensagem": ERRO_DADOS}), 400

    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return jsonify({"status": "falha", "mensagem": f"Erro no servidor: {str(e)}"}), 500
    
#**************************************************************************************************
#* DELETE                                                                                          *
#************************************************************************************************** 
@app.delete('/branch', tags=[branch_tag], 
            responses={"200": BranchesDelSchema, "404": ErrorSchema})

@with_session
def del_branch(body: BranchesSearchSchema, session):
    """ 
    Apaga um item da base de dados a partir do seu identificador 
    """
    
    branch_data = request.get_json()
    branch_id = branch_data.get("branch_id")
    logger.debug(f"Apagando dados sobre a branch #{branch_id}")
   
    try: 
        count = session.query(Branches).filter(Branches.branch_id == branch_id).delete()

        if count:
            logger.debug(f"Deletada Agências #{branch_id}")
            return jsonify({"message": "Agências removida", "id": branch_id}), 200
        
        else: 
            # se a agências não foi encontrado
            logger.warning(f"Erro ao deletar Agências #'{branch_id}'")
            return jsonify({"message": f"Erro ao deletar Agências #'{branch_id}'"}), 400 
    
    except IntegrityError as e: 
        logger.error(f"Erro de integridade: '{branch_id}': {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409
    
    except Exception as e:
        logger.error(f"Erro interno do servidor: '{branch_id}': {str(e)}") 
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 500

#**************************************************************************************************
#* PATCH                                                                                          *
#************************************************************************************************** 
@app.put('/branch', tags=[branch_tag],
         responses={"200": BranchesViewSchema, "404": ErrorSchema, "400": ErrorSchema})

@with_session
def put_branch(body: BranchesUpdateSchema, session):
    """ 
    Atualiza os campos de uma categoria específica, identificada pelo ID. 
    """

    branch_data = request.get_json()
    branch_id = branch_data.get("branch_id")
    logger.debug(f"Tentando atualizar a Agência com ID {branch_id}")

    try:
        branch = session.query(Branches).filter(Branches.branch_id == branch_id).first()

        if not branch:
            logger.debug(f"Agência com ID {branch_id} não encontrada")
            return jsonify({"message": "Agência não encontrada"}), 404

        update_fields(branch, branch_data)

        logger.debug(f"Agência com ID {branch_id} atualizada com sucesso")
        return jsonify({
            "bank_id": branch.bank_id,
            "branch_address": branch.branch_address,
            "branch_cep": branch.branch_cep,
            "branch_city": branch.branch_city,
            "branch_complement": branch.branch_complement,
            "branch_country": branch.branch_country,
            "branch_description": branch.branch_description,
            "branch_email": branch.branch_email,
            "branch_id": branch.branch_id,
            "branch_number": branch.branch_number,
            "branch_phone": branch.branch_phone,
            "branch_state": branch.branch_state,
            "status": "Sucesso",
            "message": "Recurso atualizado com sucesso"
        }), 200

    except DataError as e:
        logger.error(f"Dados inválidos fornecidos: {str(e)}")
        return jsonify({"message": ERRO_DADOS}), 400

    except IntegrityError as e:
        logger.error(f"Erro de integridade: {str(e)}")
        return jsonify({"message": "ERRO_DE_INTEGRIDADE"}), 409

    except Exception as e:
        logger.error(f"Erro ao atualizar categoria: {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 500


def update_fields(branch, branch_data):
    """
    Função auxiliar para atualizar os campos de uma agência.
    """
    updatable_fields = [
        "branch_description", "bank_id", "branch_cep", "branch_address",
        "branch_number", "branch_complement", "branch_district", "branch_city",
        "branch_state", "branch_country", "branch_phone", "branch_email"
    ]
    for field in updatable_fields:
        if field in branch_data and branch_data[field]:
            setattr(branch, field, branch_data[field])

#**************************************************************************************************
#* PATCH                                                                                            *
#************************************************************************************************** 
@app.patch('/branch', tags=[branch_tag],
         responses={"200": BranchesViewSchema, "404": ErrorSchema, "400": ErrorSchema})

@with_session
def patch_branch(body: BranchesUpdateSchema, session):
    """ 
    Atualiza os campos de uma categoria específica, identificada pelo ID. 
    """

    branch_data = request.get_json()
    branch_id = branch_data.get("branch_id")
    logger.debug(f"Tentando atualizar a Agência com ID {branch_id}")

    try:
        branch = session.query(Branches).filter(Branches.branch_id == branch_id).first()

        if not branch:
            logger.debug(f"Agência com ID {branch_id} não encontrada")
            return {"message": "Agência não encontrada"}, 404

        update_fields(branch, branch_data)

        logger.debug(f"Agência com ID {branch_id} atualizada com sucesso")
        
        return jsonify({
            "bank_id": branch.bank_id,
            "branch_address": branch.branch_address,
            "branch_cep": branch.branch_cep,
            "branch_city": branch.branch_city,
            "branch_complement": branch.branch_complement,
            "branch_country": branch.branch_country,
            "branch_description": branch.branch_description,
            "branch_email": branch.branch_email,
            "branch_id": branch.branch_id,
            "branch_number": branch.branch_number,
            "branch_phone": branch.branch_phone,
            "branch_state": branch.branch_state,
            "status": "Sucesso",
            "message": "Recurso atualizado com sucesso"
        }), 200
    
    except DataError as e:
        logger.error(f"Dados inválidos fornecidos: {str(e)}")
        return {"message": ERRO_DADOS}, 400

    except IntegrityError as e:
        logger.error(f"Erro de integridade: {str(e)}")
        return {"message": ERRO_DE_INTEGRIDADE}, 409

    except Exception as e:
        logger.error(f"Erro ao atualizar categoria: {str(e)}")
        return {"message": ERRO_DE_INTEGRIDADE}, 500


def update_fields(branch, branch_data):
    """
    Função auxiliar para atualizar os campos de uma agência.
    """
    updatable_fields = [
        "branch_description", "bank_id", "branch_cep", "branch_address",
        "branch_number", "branch_complement", "branch_district", "branch_city",
        "branch_state", "branch_country", "branch_phone", "branch_email"
    ]
    for field in updatable_fields:
        if field in branch_data and branch_data[field]:
            setattr(branch, field, branch_data[field])