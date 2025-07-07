from flask import Flask, jsonify, request
from flask_openapi3.openapi import OpenAPI
from flask_openapi3.models.info import Info
from flask_openapi3.models.tag import Tag 
from flask_openapi3.blueprint import APIBlueprint
from flask_cors import CORS
from models import Session
from models.table import Categories
from flask_jwt_extended import JWTManager
from sqlalchemy.exc import IntegrityError, DataError
from urllib.parse import unquote
from schemas.table import CategoriesViewSchema, CategoriesDelSchema
from schemas.table import CategoriesSchema, CategoriesUpdateSchema
from schemas.table import CategoriesSearchSchema, ListCategoriesSchema
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
info = Info(title="API Category", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Constantes
ERRO_DE_INTEGRIDADE = "Erro de integridade"
ERRO_DE_DADOS = "Erro de dados"

# Configuração do JWT para autenticação
app.config["JWT_SECRET_KEY"] = "banana"
jwt = JWTManager(app)

# Crie um blueprint para a financial_api_category
category_api = APIBlueprint('category_api', __name__)

#define tags
#documentation_tag = Tag(name="Documentação", description="Seleção de documentação: Swager")
#home_tag = Tag(name="Inicial", description="Página Inicial")
category_tag = Tag(name="categoria", description="Adição, visualização e remoção de categories da base")

# Registre o blueprint na aplicação principal
app.register_api(category_api)

#**************************************************************************************************
#* Middleware para validar o token recebido da API principal                                      *
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
#* Decorador para gerenciamento de sessão                                                         *
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
#* Consulta o cadastro                                                                            *
#**************************************************************************************************
@app.get('/category', tags=[category_tag],
          responses={"200": ListCategoriesSchema, "404": ErrorSchema})

@with_session
def get_category(session):
    """
    Faz a busca por todos os itens cadastrado na base de dado.
    """
    logger.debug(f"Requisição recebida: {request.method} {request.path}")

    try:
        categories = session.query(Categories).order_by(Categories.category_id).all()
        
        if not categories:
            # se não há categories cadastrados
            logger.debug(f"Não há categorias cadastradas {request.method} {request.path}")
            return jsonify({"category": []}), 200

        logger.debug(f"{len(categories)} categorias econtradas {request.method} {request.path}")
        return jsonify({"category": [category.to_dict() for category in categories]}), 200

    except DataError as e:
        return jsonify({"message": ERRO_DE_DADOS}), 400
    
    except IntegrityError as e:
        logger.error(f"Erro de integridade: {str(e)}")  
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409
    
    except Exception as e:
        logger.error(f"Erro no servidor: {str(e)}") 
        return jsonify({"message": f"Erro no servidor: {str(e)}"}), 500
        
    finally:
        session.close() # Fechar a sessão 

#**************************************************************************************************
#* Gravação dos dados                                                                             *
#**************************************************************************************************
@app.post('/category', tags=[category_tag],
          responses={"200": CategoriesViewSchema, "409": ErrorSchema, "400": ErrorSchema})

@with_session
def add_category(body: CategoriesSchema, session):
    """ 
    Adiciona um item na base de dados a partir de uma requisição externa.
    """
    try:
        # Obtém os dados enviados pela API externa (via JSON no corpo da requisição)
        category_data = request.get_json()
        
        if not category_data or not category_data.get("category_id"):
            logger.error("Dados inválidos ou ausentes na requisição")
            return jsonify({"status": "falha", "mensagem": "Dados inválidos ou ausentes"}), 400

        # Cria o objeto da categoria a partir dos dados recebidos
        category = Categories(
            category_id=category_data.get("category_id"),
            category_description=category_data.get("category_description"),
            category_type=category_data.get("category_type")
        )

        # Adiciona a categoria no banco de dados
        session.add(category)
        logger.debug(f"Categoria adicionada com sucesso: '{category}'")
        return jsonify({"status": "sucesso", "mensagem": "Dados gravados com sucesso"}), 200

    except IntegrityError as e:
        logger.error(f"Erro de integridade: {str(e)} - Erro de duplicidade ou restrição de chave.")
        return jsonify({"status": "falha", "mensagem": "Erro de duplicidade ou restrição de chave."}), 409

    except DataError as e:
        logger.error(f"{ERRO_DE_DADOS}: {str(e)}")
        return jsonify({"status": "falha", "mensagem": ERRO_DE_DADOS}), 400

    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return jsonify({"status": "falha", "mensagem": f"Erro no servidor: {str(e)}"}), 500
    
#**************************************************************************************************
#* Delete                                                                                         *
#**************************************************************************************************
@app.delete('/category', tags=[category_tag], 
            responses={"200": CategoriesDelSchema, "404": ErrorSchema})

#@jwt_required()
@with_session
def del_category(body: CategoriesSearchSchema, session):
    """ 
    Apaga um item da base de dados a partir do seu identificador 
    """
    
    category_data = request.get_json()
    category_id = category_data.get("category_id")
    logger.debug(f"Apagando dados sobre a category #{category_id}")
   
    try: 
        count = session.query(Categories).filter(Categories.category_id == category_id).delete()

        if count:
            logger.debug(f"Deletada categoria #{category_id}")
            return jsonify({"message": "categoria removida", "id": category_id}), 200
        
        else: 
            # se a categoria não foi encontrado
            logger.warning(f"Erro ao deletar categoria #'{category_id}'")
            return jsonify({"message": f"Erro ao deletar categoria #'{category_id}'"}), 400 
    
    except IntegrityError as e: 
        logger.error(f"Erro de integridade: '{category_id}': {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409
    
    except Exception as e:
        logger.error(f"Erro interno do servidor: '{category_id}': {str(e)}") 
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 500

#**************************************************************************************************
#* Atualiza todos os campos                                                                       *
#**************************************************************************************************
@app.put('/category', tags=[category_tag],
         responses={"200": CategoriesViewSchema, "404": ErrorSchema, "400": ErrorSchema})

@with_session
def update_category(body: CategoriesUpdateSchema, session):
    """ 
    Atualiza os campos de uma categoria específica, identificada pelo ID. 
    """

    # Dados enviados pelo cliente
    category_data = request.get_json()

    # Cria o objeto da categoria a partir dos dados recebidos
    category_api = Categories(
        category_id=category_data.get("category_id"),
        category_description=category_data.get("category_description"),
        category_type=category_data.get("category_type")
    )
    logger.debug(f"Tentando atualizar categoria com ID {category_api.category_id}")
   
    try:
        category = session.query(Categories).filter(
            Categories.category_id == category_api.category_id).first()

        if not category:
            logger.debug(f"Categoria com ID {category_api.category_id} não encontrada")
            return jsonify({"message": "Categoria não encontrada"}), 404

        # Atualizar os campos da categoria
        desc = getattr(category_api, "category_description", None)
        if desc:
            category.category_description = desc

        tp = getattr(category_api, "category_type", None)
        if tp:
            category.category_type = tp

        # Persistir as alterações na base de dados
        logger.debug(f"Categoria com ID {category_api.category_id} atualizada com sucesso")

        # Retorna a categoria atualizada
        return jsonify({
            "category_id": category.category_id,
            "category_description": category.category_description,
            "category_type": category.category_type,
            "message": "Categoria atualizada com sucesso"
        }), 200

    except DataError as e:
        logger.error(f"{ERRO_DE_DADOS}: {str(e)}")
        return jsonify({"message": ERRO_DE_DADOS}), 400
    
    except IntegrityError as e: 
        logger.error(f"Erro de integridade: {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409

    except Exception as e:
        logger.error(f"Erro ao atualizar categoria: {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 500
    
#**************************************************************************************************
#* Atuaiza parcial                                                                                *
#**************************************************************************************************
@app.patch('/category', tags=[category_tag])

@with_session
def patch_category(body: CategoriesUpdateSchema, session):
    """
    Atualiza parcialmente os campos de uma categoria específica, identificada pelo ID.
    """

   # Dados enviados pelo cliente
    category_data = request.get_json()
    category_id = category_data.get("category_id")

    if not category_id:
        logger.error("O campo 'category_id' é obrigatório e não foi fornecido.")
        return jsonify({"message": "O campo 'category_id' é obrigatório."}), 400
    
    logger.debug(f"Tentando atualizar parcialmente a categoria com o ID {category_id}")
       
    try:
        category = session.query(Categories).filter(
            Categories.category_id == category_id).first()

        if not category:
            logger.debug(f"Categoria com ID {category_id} não encontrada")
            return jsonify({"message": "Categoria não encontrada"}), 404

        # Atualizar apenas os campos fornecidos
        if "category_description" in category_data:
            category.category_description = category_data["category_description"]
        if "category_type" in category_data:
            category.category_type = category_data["category_type"]

        logger.debug(f"Categoria com ID {category_id} atualizada parcialmente com sucesso")

        # Retorna a categoria atualizada
        return jsonify({
            "category_id": category.category_id,
            "category_description": category.category_description,
            "category_type": category.category_type,
            "message": "Categoria atualizada parcialmente com sucesso"
        }), 200

    except DataError as e:
        logger.error(f"Erro de dados: {str(e)}")
        return jsonify({"message": "Erro de dados"}), 400

    except IntegrityError as e:
        logger.error(f"Erro de integridade: {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409

    except Exception as e:
        logger.error(f"Erro ao atualizar parcialmente categoria: {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 500
