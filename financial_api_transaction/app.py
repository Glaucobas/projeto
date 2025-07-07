import logging, requests
import joblib
import pickle
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from keras.layers import Dense
from functools import wraps
from datetime import date, datetime
from typing import Optional

from flask import Flask, jsonify, request, redirect
from flask_openapi3.blueprint import APIBlueprint 
from flask_openapi3.openapi import OpenAPI
from flask_openapi3.models.info import Info
from flask_openapi3.models.tag import Tag
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy.exc import IntegrityError, DataError

from models import Session
from models.table import Transactions
from schemas.table import (TransactionsViewSchema, 
                           TransactionsDelSchema, 
                           TransactionsSchema, 
                           TransactionsUpdateSchema, 
                           TransactionsSearchSchema, 
                           ListTransactionsSchema,
                           TransactionsClass
)
from schemas.error import ErrorSchema
from collections import Counter

# Cria um logger
logger = logging.getLogger(__name__) 
logger.setLevel(logging.DEBUG)

# Cria um handler para o console 
console_handler = logging.StreamHandler() 
console_handler.setLevel(logging.DEBUG)

# Cria um handler para um arquivo 
file_handler = logging.FileHandler('.\\log\\app.log') 
file_handler.setLevel(logging.WARNING) 

# Define um formatador 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
console_handler.setFormatter(formatter) 
file_handler.setFormatter(formatter) 

# Adiciona os handlers ao logger 
logger.addHandler(console_handler) 
logger.addHandler(file_handler)

# Configuração da aplicação Flask
info = Info(title="API Transaction", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Constantes
ERRO_DE_INTEGRIDADE = "Erro de integridade"
CORS(app)  # Configuração segura do CORS

# Configuração do JWT para autenticação
app.config["JWT_SECRET_KEY"] = "banana"
jwt = JWTManager(app)

# Crie um blueprint para a financial_api_category
transaction_api = APIBlueprint('transaction_api', __name__)

# Modelo de predição
modelo1 = joblib.load('./models/logistic_regression_model.pkl')
modelo2 = joblib.load('./models/random_forest_model.pkl')
modelo3 = joblib.load('./models/naive_bayes_model.pkl')
modelo4 = load_model('./models/cnn_model.h5')
modelo4.compile(
    optimizer ='adam',
    loss = 'categorical_crossentropy', #'binary_crossentropy' dependendo do seu caso
    metrics = ['accuracy']
)
vectorizer1 = joblib.load('./models/logistic_regression_vectorizer.pkl') 
vectorizer2 = joblib.load('./models/random_forest_vectorizer.pkl')
vectorizer3 = joblib.load('./models/naive_bayes_vectorizer.pkl')

with open('./models/cnn_tokenizer.pkl', 'rb') as f:
    vectorizer4 = pickle.load(f)
with open('./models/cnn_label_encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)
        
#define tags
documentation_tag = Tag(name="Documentação", description="Seleção de documentação: Swager")
home_tag          = Tag(name="Inicial", description="Página Inicial")
transaction_tag   = Tag(name="Transações", description="Adição, visualização e remoção de categories da base")

# Registre o blueprint na aplicação principal
app.register_api(transaction_api)

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False, port=5006)

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
#* DECLARATOR SESSION                                                                             *
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
#* DATE                                                                                          *
#**************************************************************************************************
def parse_date(date_str: Optional[str]) -> date:
    """
    Converte string de data no para objeto date.
    - Loga um warning para datas inválidas
    """
    if not date_str:
        return datetime.today().date()
    
    try:
        # Tenta parse com os seguintes formatos
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(date_str.strip(), fmt).date()
            except ValueError:
                continue
        raise ValueError
    except ValueError:
        logger.warning(f"Formato de data inválido: '{date_str}'")
        return datetime.today().date()

#**************************************************************************************************
#* Documentations                                                                                 *
#**************************************************************************************************
@app.get('/', tags=[documentation_tag])
def documentation():
    """ 
    Redireciona para /openapi.
    """
    return redirect('/openapi')
    
#**************************************************************************************************
#* GET                                                                                            *
#**************************************************************************************************
@app.get('/transaction', tags=[transaction_tag],
          responses={"200": ListTransactionsSchema, "404": ErrorSchema})

@with_session
def get_transaction(session):
    """
    Faz a busca por todos os itens cadastrado na base de dado.
    """
    logger.debug(f"Requisição recebida: {request.method} {request.path}")

    try:
        transactions = session.query(Transactions).order_by(Transactions.transaction_id).all()
        
        if not transactions:
            logger.debug(f"Não há transações cadastradas {request.method} {request.path}")
            return jsonify({"transaction": []}), 200

        logger.debug(f"{len(transactions)} transações econtradas {request.method} {request.path}")
        return jsonify({"transaction": [transaction.to_dict() for transaction in transactions]}), 200

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
#* POST                                                                                           *
#**************************************************************************************************
@app.post('/transaction', tags=[transaction_tag],
          responses={"200": TransactionsViewSchema, "409": ErrorSchema, "400": ErrorSchema})

@with_session
def add_transaction(body: TransactionsSchema, session):
    """ 
    Adiciona um item na base de dados a partir de uma requisição externa.
    """
    try:
        # Obtém os dados enviados pela API externa (via JSON no corpo da requisição)
        transaction_data = request.get_json()

        required_fields = [
            "transaction_id", "transaction_description", "account_id", "branch_id", 
            "resource_id", "transaction_type", "transaction_value", "transaction_status"
        ]
        missing_fields = [field for field in required_fields if field not in transaction_data]
        if missing_fields:
            return jsonify({
                "status" : "Falha",
                "message" : f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"
            }), 400
        
        try:
            transaction_date = parse_date(transaction_data.get("transaction_date"))
            transaction_expiration_date = parse_date(transaction_data.get("transaction_expiration_date"))
        except Exception as e:
            return jsonify({
                "status" : "Falha",
                "message" : f"Formato de data inválido: {str(e)}"
            }), 400

        try:
            transaction_value = float(transaction_data["transaction_value"])
        except (ValueError, TypeError):
            return jsonify({
                "status" : "Falha",
                "message" : "transaction_value deve ser numérico"
            }), 400
        
        if not transaction_data or not transaction_data.get("transaction_id"):
            logger.error("Dados inválidos ou ausentes na requisição")
            return jsonify({
                "status": "Falha", 
                "message": "Dados inválidos ou ausentes"
            }), 400

        try:
            desc_text = transaction_data["transaction_description"]
            category_id = vote_category(desc_text)

        except Exception as e:
            logger.error(f"Erro no modelo de predição: {str(e)}")
            return jsonify({
                "status": "Falha", 
                "message": "Erro ao processar descrição com modelo de predição"
            }), 400


        # Cria o objeto da categoria a partir dos dados recebidos
        transaction = Transactions(
            transaction_id = transaction_data["transaction_id"],
            transaction_date = transaction_date,
            transaction_expiration_date = transaction_expiration_date,
            transaction_description = transaction_data["transaction_description"],
            category_id = category_id,
            account_id = transaction_data["account_id"],
            branch_id = transaction_data["branch_id"],
            resource_id = transaction_data["resource_id"],
            transaction_type = transaction_data["transaction_type"],
            transaction_value = transaction_value,
            transaction_status = transaction_data["transaction_status"]
        )
       
        # Adiciona um item ao banco de dados
        session.add(transaction)
        logger.debug(f"Transação adicionada com sucesso: '{transaction}'")
        return jsonify({"status": "Sucesso", "message": "Dados gravados com sucesso"}), 200

    except IntegrityError as e:
        logger.error(f"Erro de integridade: {str(e)} - Erro de duplicidade ou restrição de chave.")
        return jsonify({"status": "Falha", "message": "Erro de duplicidade ou restrição de chave."}), 409

    except DataError as e:
        logger.error(f"Erro de dados: {str(e)}")
        return jsonify({"status": "Falha", "message": "Dados inválidos fornecidos"}), 400

    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return jsonify({"status": "Falha", "message": f"Erro no servidor: {str(e)}"}), 500

def predict_category(description, modelo, vectorizer):
    """Faz a predição da categoria para os modelos regressão logística e Randon Forest"""
    try:
        X = vectorizer.transform([description])
        predicao = modelo.predict(X)
        return predicao[0]
    
    except Exception as e:
        logger.error(f"Erro ao fazer predição com regressão logística/Randon Forest: {str(e)}")
        return None

def predict_category_nb(description, modelo):
    """Faz a predição da categoria para uma descrição usando Naive Bayes"""
    try:
        if not isinstance(description, str):
            description = str(description)
        predicao = modelo.predict([description])
        return predicao[0]
    except Exception as e:
        logger.error(f"Erro ao fazer predição com Naive Bayes: {str(e)}")
        return None
    
def predict_category_cnn(description, modelo, tokenizer, encoder, maxlen=100):
    try:
        seq = tokenizer.texts_to_sequences([description])
        padded = pad_sequences(seq, maxlen=maxlen)
        pred = modelo.predict(padded)
        pred_index = np.argmax(pred)
        pred_label = encoder.inverse_transform([pred_index])[0]
        return pred_label
    except Exception as e:
        logger.error(f"Erro na predição com CNN: {str(e)}")
        return None
    
def vote_category(description):
    """Faz a predição da categoria com votação entre três modelos"""
    try:

        # Obtém as predições dos três modelos
        pred1 = predict_category(description, modelo1, vectorizer1)
        pred2 = predict_category(description, modelo2, vectorizer2)
        pred3 = predict_category_nb(description, modelo3)
        pred4 = predict_category_cnn(description, modelo4, vectorizer4, encoder)

        # Conta quantas vezes cada categoria apareceu
        vote = Counter([pred1, pred2, pred3, pred4])
        category_more_comum, contagem = vote.most_common(1)[0]

        # Verifica se ao menos dois modelos concordaram
        if contagem > 2:
            return category_more_comum
        else:
            return "CND"  # Nenhum consenso
    except Exception as e:
        logger.error(f"Erro de predição: {str(e)}.")
        return "CND"

#**************************************************************************************************
#* DELETE                                                                                         *
#**************************************************************************************************
@app.delete('/transaction', tags=[transaction_tag], 
            responses={"200": TransactionsDelSchema, "404": ErrorSchema})

#@jwt_required()
@with_session
def del_transaction(body: TransactionsSearchSchema, session):#
    """ 
    Apaga um item da base de dados a partir do seu identificador 
    """
    
    transaction_data = request.get_json()
    transaction_id = transaction_data.get("transaction_id")
    logger.debug(f"Apagando dados sobre a tansação#{transaction_id}")
   
    try: 
        count = session.query(Transactions).filter(Transactions.transaction_id == transaction_id).delete()

        if count:
            logger.debug(f"Transação excluida #{transaction_id}")
            return jsonify({"message": "Transação removida", "id": transaction_id}), 200
        
        else: 
            # se a tansação não foi encontrado
            logger.warning(f"Erro ao deletar transação #'{transaction_id}'")
            return jsonify({"message": f"Erro ao deletar transação #'{transaction_id}'"}), 400 
    
    except IntegrityError as e: 
        logger.error(f"Erro de integridade: '{transaction_id}': {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409
    
    except Exception as e:
        logger.error(f"Erro interno do servidor: '{transaction_id}': {str(e)}") 
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 500

#**************************************************************************************************
#* PATCH                                                                                     *
#**************************************************************************************************
@app.patch('/transaction', tags=[transaction_tag],
         responses={"200": TransactionsViewSchema, "404": ErrorSchema, "400": ErrorSchema})

@with_session
def update_transaction(body: TransactionsUpdateSchema, session):
    """ 
    Atualiza os campos de uma categoria específica, identificada pelo ID. 
    """
    def update_field(transaction, transaction_api, field_name):
        """Auxilia na atualização de campos específicos."""
        if hasattr(transaction_api, field_name) and getattr(transaction_api, field_name):
            setattr(transaction, field_name, getattr(transaction_api, field_name))
            
    # Dados enviados pelo cliente
    transaction_data = request.get_json()

    try:
        transaction_date = parse_date(transaction_data.get("transaction_date"))
        transaction_expiration_date = parse_date(transaction_data.get("transaction_expiration_date"))
    except Exception as e:
        return jsonify({
            "status" : "Falha",
            "message" : f"Formato de data inválido: {str(e)}"
        }), 400
    
    try:
        transaction_value = float(transaction_data["transaction_value"])
    except (ValueError, TypeError):
        return jsonify({
            "status" : "Falha",
            "message" : "transaction_value deve ser numérico"
        }), 400
            
    # Cria o objeto da categoria a partir dos dados recebidos
    transaction_api = Transactions(
            transaction_id = transaction_data["transaction_id"],
            transaction_date = transaction_date,
            transaction_expiration_date = transaction_expiration_date,
            transaction_description = transaction_data["transaction_description"],
            category_id = transaction_data["category_id"],
            account_id = transaction_data["account_id"],
            branch_id = transaction_data["branch_id"],
            resource_id = transaction_data["resource_id"],
            transaction_type = transaction_data["transaction_type"],
            transaction_value = transaction_value,
            transaction_status = transaction_data["transaction_status"]
    )    
    logger.debug(f"Tentando atualizar transação com ID {transaction_api.transaction_id}")
   
    try:
        transaction = session.query(Transactions).filter(
            Transactions.transaction_id == transaction_api.transaction_id).first()

        if not transaction:
            logger.debug(f"Transação com ID {transaction_api.transaction_id} não encontrada")
            return {"message": "Transação não encontrada"}, 404

        # Atualizar os campos da transação com os dados recebidos
        fields_to_update = [
            "transaction_date", "transaction_expiration_date", 
            "transaction_description", "category_id", "account_id", 
            "branch_id", "resource_id", "transaction_type",
            "transaction_value"
        ]
        for field in fields_to_update:
            update_field(transaction, transaction_api, field)

        # Persistir as alterações na base de dados
        logger.debug(f"Transação com ID {transaction_api.transaction_id} atualizada com sucesso")

        # Retorna a transaação atualizada
        return jsonify({
            "transaction_id": transaction.transaction_id,
            "transaction_date": transaction.transaction_date,
            "transaction_expiration_date": transaction.transaction_expiration_date,
            "transaction_description": transaction.transaction_description,
            "category_id": transaction.category_id,
            "account_id": transaction.account_id,
            "branch_id": transaction.branch_id,
            "resource_id": transaction.resource_id,
            "transaction_type": transaction.transaction_type,
            "transaction_value": transaction.transaction_value,
            "transaction_status": transaction.transaction_status,
            "status": "Sucesso",
            "message": "Categoria atualizada com sucesso"
        }), 200

    except DataError as e:
        logger.error(f"Erro de dados: {str(e)}")
        return jsonify({"message": "Erro de dados"}), 400
    
    except IntegrityError as e: 
        logger.error(f"Erro de integridade: {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 409

    except Exception as e:
        logger.error(f"Erro ao atualizar categoria: {str(e)}")
        return jsonify({"message": ERRO_DE_INTEGRIDADE}), 500