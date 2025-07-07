from flask import Flask, jsonify, redirect, request, make_response
from flask_openapi3 import OpenAPI, Info, Tag, APIBlueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required
from models import Session
from models.table import Resources
from sqlalchemy.exc import IntegrityError, DataError
from urllib.parse import unquote
from schemas.table import ResourcesViewSchema, ResourcesDelSchema
from schemas.table import ResourcesSchema, ResourcesUpdateSchema
from schemas.table import ResourcesSearchSchema, ListResourcesSchema
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
info = Info(title="API Resource", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Constantes
ERRO_DE_INTEGRIDADE = "Erro de integridade"
ERRO_DADOS = "Erro de dados"
CORS(app)  # Configuração segura do CORS

# Configuração do JWT para autenticação
app.config["JWT_SECRET_KEY"] = "banana"
jwt = JWTManager(app)

# Crie um blueprint para a financial_api_resource
resource_api = APIBlueprint('resource_api', __name__)

#define tags
documentation_tag = Tag(name="Documentação", description="Seleção de documentação: Swager")
home_tag = Tag(name="Inicial", description="Página Inicial")
resource_tag = Tag(name="Recursos", description="Adição, visualização e remoção de recursos da base")

# Registre o blueprint na aplicação principal
app.register_api(resource_api)

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
@app.get('/resource', tags=[resource_tag],
          responses={"200": ResourcesViewSchema, "409": ErrorSchema, "400": ErrorSchema})
@with_session
def get_resource(session):
    """
    Faz a busca por todos os itens cadastrado na base de dado.
    """
    logger.debug(f"Requisição recebida: {request.method} {request.path}")

    try:
        resources = session.query(Resources).order_by(Resources.resource_id).all()
        
        if not resources:
            logger.debug(f"Não há Recursos cadastradas {request.method} {request.path}")
            return jsonify({"resource": []}), 200

        logger.debug(f"{len(resources)} Recursos econtrados {request.method} {request.path}")
        return jsonify({"resource": [resource.to_dict() for resource in resources]}), 200

    except DataError as e:
        logger.error(f"Erro de dados: {str(e)}")
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
@app.post('/resource', tags=[resource_tag],
          responses={"200": ResourcesViewSchema, "409": ErrorSchema, "400": ErrorSchema})

@with_session
def add_resource(body: ResourcesSchema, session):
    """ 
    Adiciona um item na base de dados a partir de uma requisição externa.
    """
    try:
        # Obtém os dados enviados pela API externa (via JSON no corpo da requisição)
        resource_data = request.get_json()
        
        if not resource_data or not resource_data.get("resource_id"):
            logger.error("Dados inválidos ou ausentes na requisição")
            return jsonify({"status": "falha", "mensagem": "Dados inválidos ou ausentes"}), 400

        # Cria o objeto da categoria a partir dos dados recebidos
        resource = Resources(
            resource_id=resource_data.get("resource_id"),
            resource_description=resource_data.get("resource_description"),
            resource_status=resource_data.get("resource_status")
        )

        # Adiciona a categoria no banco de dados
        session.add(resource)
        logger.debug(f"Recurso adicionado com sucesso: '{resource}'")
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
#* DELETE                                                                                         *
#**************************************************************************************************
@app.delete('/resource', tags=[resource_tag], 
            responses={"200": ResourcesDelSchema, "404": ErrorSchema})

#@jwt_required()
@with_session
def del_resource(body: ResourcesSearchSchema, session):
    """ 
    Apaga um item da base de dados a partir do seu identificador 
    """
    
    resource_data = request.get_json()
    resource_id = resource_data.get("resource_id")
    logger.debug(f"Apagando dados sobre a resource #{resource_id}")
   
    try: 
        count = session.query(Resources).filter(Resources.resource_id == resource_id).delete()

        if count:
            logger.debug(f"Deletado o Recurso #{resource_id}")
            return jsonify({"message": "Recurso removido", "id": resource_id}), 200
        
        else: 
            # se a categoria não foi encontrado
            logger.warning(f"Erro ao deletar recurso #'{resource_id}'")
            return jsonify({"message": f"Erro ao deletar recurso #'{resource_id}'"}), 400 
    
    except IntegrityError as e: 
        logger.error(f"Erro de integridade: '{resource_id}': {str(e)}")
        return jsonify({"message": ERRO_DADOS}), 409
    
    except Exception as e:
        logger.error(f"Erro interno do servidor: '{resource_id}': {str(e)}") 
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 500

#**************************************************************************************************
#* PUT                                                                                            *
#**************************************************************************************************
@app.put('/resource', tags=[resource_tag],
         responses={"200": ResourcesViewSchema, "404": ErrorSchema, "400": ErrorSchema})

@with_session
def update_resource(body: ResourcesUpdateSchema, session):
    """ 
    Atualiza os campos de um recurso específico, identificado pelo ID. 
    """

    # Dados enviados pelo cliente
    resource_data = request.get_json()

    # Cria o objeto da categoria a partir dos dados recebidos
    resource_api = Resources(
        resource_id=resource_data.get("resource_id"),
        resource_description=resource_data.get("resource_description"),
        resource_status=resource_data.get("resource_status")
    )
    logger.debug(f"Tentando atualizar recursos com ID {resource_api.resource_id}")
   
    try:
        resource = session.query(Resources).filter(
            Resources.resource_id == resource_api.resource_id).first()

        if not resource:
            logger.debug(f"Recurso com ID {resource_api.resource_id} não encontrado")
            return jsonify({"message": "Recurso não encontrado"}), 404

        # Atualizar os campos da categoria
        if hasattr(resource_api, "resource_description") and resource_api.resource_description:
            resource.resource_description = resource_api.resource_description
        if hasattr(resource_api, "resource_status") and resource_api.resource_status:
            resource.resource_status = resource_api.resource_status

        # Persistir as alterações na base de dados
        logger.debug(f"Recurso com ID {resource_api.resource_id} atualizado com sucesso")

        # Retorna a categoria atualizada
        return jsonify({
            "resource_id": resource.resource_id,
            "resource_description": resource.resource_description,
            "resource_status": resource.resource_status,
            "message": "Recurso atualizado com sucesso",
            "Status": "Sucesso"
        }), 200

    except DataError as e:
        logger.error(f"Erro de dados: {str(e)}")
        return jsonify({"message": ERRO_DADOS}), 400
    
    except IntegrityError as e: 
        logger.error(f"Erro de integridade: {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409

    except Exception as e:
        logger.error(f"Erro ao atualizar Recurso: {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 500
    
#**************************************************************************************************
#* PUT                                                                                            *
#**************************************************************************************************
@app.patch('/resource', tags=[resource_tag],
            responses={"200": ResourcesViewSchema, "404": ErrorSchema, "400": ErrorSchema})
@with_session
def patch_resource(body: ResourcesUpdateSchema, session):
    """
    Atualiza parcialmente os campos de um recurso específico, identificado pelo ID.
    """
    resource_data = request.get_json()

    resource_id = resource_data.get("resource_id")
    logger.debug(f"Tentando atualizar parcialmente o recurso com ID {resource_id}")

    try:
        resource = session.query(Resources).filter(Resources.resource_id == resource_id).first()

        if not resource:
            logger.debug(f"Recurso com ID {resource_id} não encontrado")
            return jsonify({"message": "Recurso não encontrado"}), 404

        # Atualizar apenas os campos fornecidos
        if "resource_description" in resource_data:
            resource.resource_description = resource_data["resource_description"]
        if "resource_status" in resource_data:
            resource.resource_status = resource_data["resource_status"]

        logger.debug(f"Recurso com ID {resource_id} atualizado com sucesso")

        return jsonify({
            "resource_id": resource.resource_id,
            "resource_description": resource.resource_description,
            "resource_status": resource.resource_status,
            "message": "Recurso atualizado parcialmente com sucesso",
            "Status": "Sucesso"
        }), 200

    except DataError as e:
        logger.error(f"Erro de dados: {str(e)}")
        return jsonify({"message": ERRO_DADOS}), 400

    except IntegrityError as e:
        logger.error(f"Erro de integridade: {str(e)}")
        return jsonify({"message": ERRO_DADOS}), 409

    except Exception as e:
        logger.error(f"Erro ao atualizar parcialmente o recurso: {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 500