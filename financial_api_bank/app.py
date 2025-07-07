from flask import Flask, jsonify, redirect, request
from flask_openapi3 import OpenAPI, Info, Tag, APIBlueprint
from flask_cors import CORS
from models import Session
from flask_jwt_extended import JWTManager
from models.table import Banks
from sqlalchemy.exc import IntegrityError, DataError
from schemas.table import BanksViewSchema, BanksDelSchema
from schemas.table import BanksSchema, BanksUpdateSchema
from schemas.table import BanksSearchSchema, ListBanksSchema
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
info = Info(title="API Bank", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Constantes
ERRO_DE_INTEGRIDADE = "Erro de integridade"
ERRO_DE_DADOS = "Erro de dados"
CORS(app)  # Configuração segura do CORS

# Configuração do JWT para autenticação
app.config["JWT_SECRET_KEY"] = "banana"
jwt = JWTManager(app)

# Crie um blueprint para a financial_api_bank
bank_api = APIBlueprint('bank_api', __name__)

#define tags
documentation_tag = Tag(name="Documentação", description="Seleção de documentação: Swager")
home_tag = Tag(name="Inicial", description="Página Inicial")
bank_tag = Tag(name="Instituição Finaneira", 
               description="Adição, visualização e remoção de Intituições Financeiras da base")

# Registre o blueprint na aplicação principal
app.register_api(bank_api)

# Middleware para validar o token recebido da API principal
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

# Decorador para gerenciamento de sessão
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
            return {"message": f"Erro ao executar a função {f.__name__}: {str(e)}"}, 500
        finally:
            session.close()
    return wrapper

# Decorador para encapsular mensagens de erro
def handle_errors(f):
    @wraps(f)
    def wrapper_error(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except IntegrityError as e:
            logger.error(f"Erro de integridade: {str(e)}")
            return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409
        except DataError as e:
            return jsonify({"message": ERRO_DE_DADOS}), 400
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            return jsonify({"message": f"Erro no servidor: {str(e)}"}), 500
        return wrapper_error

def get_bank_by_code(code):
    """
    Consulta uma instituição financeira em uma API externa utilizando o código informado.
    Retorna quatro campos em JSON: name, ispb, code, e fullname.
    """
    try:
        # URL da API externa para consulta de instituição financeira
        api_url = f"https://brasilapi.com.br/api/banks/v1/{code}"
        response = requests.get(api_url)

        if response.status_code == 200:
            external_data = response.json()
            if "erro" in external_data:
                logger.warning(f"Código {code} não encontrado na API externa.")
                return jsonify({"message": "Código não encontrado"}), 404
            
            # Verifica se os campos esperados estão presentes no JSON retornado
            required_fields = ['ispb', 'name', 'code', 'fullName']
            if all(field in external_data for field in required_fields):
                logger.debug(f"Código encontrado {code}: {external_data}")
                return external_data, 200
            else:
                logger.error(f"Resposta incompleta da API externa para o código {code}: {external_data}")
                return jsonify({"message": "Resposta incompleta da API externa"}), 500
        else:
            logger.error(f"Erro ao consultar a instituição financeira {code}: {response.status_code}")
            return jsonify({"message": "Erro ao consultar a instituição financeira"}), response.status_code

    except requests.RequestException as e:
        logger.error(f"Erro ao realizar a requisição {code}: {str(e)}")
        return jsonify({"message": "Erro ao consultar o código"}), 500
# Metodos GET -----------------------------------------------------------------------------

# Consulta a Documentação 
@app.get('/', tags=[bank_tag],)
def documentation(): 
    """
    Documentação da API: Swagger
    """
    return redirect('/openapi')

# Consulta o cadastro de Banks
@app.get('/bank', tags=[bank_tag],
          responses={"200": ListBanksSchema, "404": ErrorSchema})

@with_session
def get_bank(session):
    """
    Faz a busca por todos os itens cadastrado na base de dados.
    """
    logger.debug(f"Requisição recebida: {request.method} {request.path}")

    try:

        banks = session.query(Banks).order_by(Banks.bank_id).all()
        
        if not banks:
            # se não há Intituição Financeira cadastrados
            logger.debug(f"Não há Instituição Financeira cadastrada {request.method} {request.path}")
            return jsonify({"bank": []}), 200

        logger.debug(f"{len(banks)} Instituição Financeira encontrada {request.method} {request.path}")
        return jsonify({"bank": [bank.to_dict() for bank in banks]}), 200

    except DataError as e:
        logger.error(f"Erro de dados: {str(e)}")
        return jsonify({"message": ERRO_DE_DADOS}), 400
    
    except IntegrityError as e:
        logger.error(f"Erro de integridade: {str(e)}")  
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409
    
    except Exception as e:
        logger.error(f"Erro no servidor: {str(e)}") 
        return jsonify({"message": f"Erro no servidor: {str(e)}"}), 500
        
    finally:
        session.close() # Fechar a sessão 

# Metodos POST -----------------------------------------------------------------------------
# Grava no cadastro de Intitnuição Financeira
@app.post('/bank', tags=[bank_tag],
          responses={"200": BanksViewSchema, "409": ErrorSchema, "400": ErrorSchema})

@with_session
def add_bank(body: BanksSchema, session):
    """ 
    Adiciona um item na base de dados a partir de uma requisição externa.
    """
    bank_data = request.get_json()
    bank_id = bank_data.get("bank_id")

    if not bank_data:
            return jsonify({"Dados inválidos ou ausentes"}), 400
    
    # Verifica se o campo 'bank_id' está presente e válido no JSON
    if not bank_id:
        return jsonify({"message": "O campo 'bank_id' é obrigatório e não pode estar ausente ou vazio"}), 400
        
    # Verifica se algum dos campos obrigatórios está vazio e tenta completar com a API externa
    if not bank_data.get("bank_description") or not bank_data.get("bank_ispb") or not bank_data.get("bank_fullName"):
        external_data, status_code = get_bank_by_code(bank_id)
        if status_code == 200:
            bank_data["bank_description"] = bank_data.get("bank_description") or external_data.get("name")
            bank_data["bank_ispb"] = bank_data.get("bank_ispb") or external_data.get("ispb")
            bank_data["bank_fullName"] = bank_data.get("bank_fullName") or external_data.get("fullName")
        else:
            return jsonify({"message": f"Não foi possível completar os registros para o código {bank_id}"}), status_code

    # Cria o objeto da Instituição Financeira a partir dos dados recebidos
    bank = Banks(
        bank_id=bank_id,
        bank_description=bank_data["bank_description"],
        bank_ispb=bank_data["bank_ispb"],
        bank_fullname=bank_data["bank_fullName"]
    )

    try:
        # Adiciona a Instituição Financeira no banco de dados
        session.add(bank)
        logger.debug(f"Instituição Financeira adicionada com sucesso: '{bank}'")
        return jsonify({"status": "sucesso", "mensagem": "Dados gravados com sucesso"}), 200
    except IntegrityError as e:
        logger.error(f"Erro de integridade ao adicionar Instituição Financeira: {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409
    except Exception as e:
        logger.error(f"Erro inesperado ao adicionar Instituição Financeira: {str(e)}")
        return jsonify({"message": f"Erro no servidor: {str(e)}"}), 500
    
# Metodos DELETE -----------------------------------------------------------------------------

# Apaga uma Instituição Financeira cadastrada
@app.delete('/bank', tags=[bank_tag], 
            responses={"200": BanksDelSchema, "404": ErrorSchema})

#@jwt_required()

@with_session
def del_bank(body: BanksSearchSchema, session):
    """ 
    Apaga um item da base de dados a partir do seu identificador 
    """
    
    bank_data = request.get_json()
    bank_id = bank_data.get("bank_id")
    logger.debug(f"Apagando dados sobre a Instituição Financeira #{bank_id}")
   
    try: 
        count = session.query(Banks).filter(Banks.bank_id == bank_id).delete()

        if count:
            logger.debug(f"Deletada Instituição Financeira #{bank_id}")
            return jsonify({"message": "Instituição Financeira removida", "id": bank_id}), 200
        
        else: 
            # se a Instituição Financeira não foi encontrado
            logger.warning(f"Erro ao deletar Instituição Financeira #'{bank_id}'")
            return jsonify({"message": f"Erro ao deletar Instituição Financeira #'{bank_id}'"}), 400 
    
    except IntegrityError as e: 
        logger.error(f"Erro de integridade: '{bank_id}': {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409
    
    except Exception as e:
        logger.error(f"Erro interno do servidor: '{bank_id}': {str(e)}") 
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 500

# Metodo PUT --------------------------------------------------------------------------------
@app.put('/bank', tags=[bank_tag],
         responses={"200": BanksViewSchema, "404": ErrorSchema, "400": ErrorSchema})

@with_session
def update_bank(body: BanksUpdateSchema, session):
    """ 
    Atualiza os campos de uma Instituição Financeira específica, identificada pelo ID. 
    """
    bank_data = request.get_json()
    bank_id = bank_data.get("bank_id")

    if not bank_id:
        logger.error("O campo 'bank_id' é obrigatório e não foi fornecido.")
        return jsonify({"message": "O campo 'bank_id' é obrigatório."}), 400

    logger.debug(f"Tentando atualizar Instituição Financeira com ID {bank_id}")

    try:
        bank = session.query(Banks).filter(Banks.bank_id == bank_id).first()

        if not bank:
            logger.debug(f"Instituição Financeira com ID {bank_id} não encontrada.")
            return jsonify({"message": "Instituição Financeira não encontrada."}), 404

        # Atualizar os campos fornecidos no corpo da requisição
        bank.bank_description = bank_data.get("bank_description", bank.bank_description)
        bank.bank_ispb = bank_data.get("bank_ispb", bank.bank_ispb)
        bank.bank_fullname = bank_data.get("bank_fullName", bank.bank_fullname)

        logger.debug(f"Instituição Financeira com ID {bank_id} atualizada com sucesso.")

        return jsonify({
            "bank_id": bank.bank_id,
            "bank_description": bank.bank_description,
            "bank_ispb": bank.bank_ispb,
            "bank_fullname": bank.bank_fullname,
            "message": "Instituição Financeira atualizada com sucesso."
        }), 200

    except DataError as e:
        logger.error(f"Erro de dados: {str(e)}")
        return jsonify({"message": "Erro de dados."}), 400

    except IntegrityError as e:
        logger.error(f"Erro de integridade: {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409

    except Exception as e:
        logger.error(f"Erro ao atualizar Instituição Financeira: {str(e)}")
        return jsonify({"message": "Erro no servidor."}), 500
        
# Metodo PATCH --------------------------------------------------------------------------------
@app.patch('/bank', tags=[bank_tag],
            responses={"200": BanksViewSchema, "404": ErrorSchema, "400": ErrorSchema})

@with_session
def partial_update_bank(body: BanksUpdateSchema, session):
    """
    Atualiza parcialmente os campos de uma Instituição Financeira específica, identificada pelo ID.
    """
    bank_data = request.get_json()
    bank_id = bank_data.get("bank_id")

    if not bank_id:
        logger.error("O campo 'bank_id' é obrigatório e não foi fornecido.")
        return jsonify({"message": "O campo 'bank_id' é obrigatório."}), 400

    logger.debug(f"Tentando atualizar parcialmente Instituição Financeira com ID {bank_id}")

    try:
        bank = session.query(Banks).filter(Banks.bank_id == bank_id).first()

        if not bank:
            logger.debug(f"Instituição Financeira com ID {bank_id} não encontrada.")
            return jsonify({"message": "Instituição Financeira não encontrada."}), 404

    # Atualizar apenas os campos fornecidos no corpo da requisição
        if "bank_description" in bank_data:
            bank.bank_description = bank_data["bank_description"]
        if "bank_ispb" in bank_data:
            bank.bank_ispb = bank_data["bank_ispb"]
        if "bank_fullName" in bank_data:
            bank.bank_fullname = bank_data["bank_fullName"]

        logger.debug(f"Instituição Financeira com ID {bank_id} atualizada parcialmente com sucesso.")

        return jsonify({
            "bank_id": bank.bank_id,
            "bank_description": bank.bank_description,
            "bank_ispb": bank.bank_ispb,
            "bank_fullname": bank.bank_fullname,
            "message": "Instituição Financeira atualizada parcialmente com sucesso."
        }), 200

    except DataError as e:
        logger.error(f"Erro de dados: {str(e)}")
        return jsonify({"message": "Erro de dados."}), 400

    except IntegrityError as e:
            logger.error(f"Erro de integridade: {str(e)}")
            return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409

    except Exception as e:
        logger.error(f"Erro ao atualizar parcialmente Instituição Financeira: {str(e)}")
        return jsonify({"message": "Erro no servidor."}), 500