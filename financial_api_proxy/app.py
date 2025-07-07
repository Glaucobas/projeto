from flask import Flask, request, jsonify, redirect
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from functools import wraps

from schemas.schema import (
    CategoriesSchema, 
    CategoriesSearchSchema, 
    CategoriesUpdateSchema,
    BanksSchema, 
    BanksSearchSchema, 
    BanksUpdateSchema, 
    ResourcesSchema, 
    ResourcesSearchSchema, 
    ResourcesUpdateSchema, 
    BranchesSchema, 
    BranchesSearchSchema,
    AccountsSchema, 
    AccountsSearchSchema,
    TransactionsSchema, 
    TransactionsSearchSchema, 
    TransactionsUpdateSchema,
    TransactionsClass
) 


from constants.message import CONNECTION_ERROR_LOG, API_TIMEOUT_MSG
from constants.message import CONNECTION_ERROR_MSG, CONTENT_TYPE_JSON
from constants.url import CATEGORY_API_URL, BANK_API_URL, RESOURCE_API_URL
from constants.url import BRANCH_API_URL, ACCOUNT_API_URL, TRANSACTION_API_URL
from constants.authentication import API2_TOKEN

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

info = Info(title = "Financeiro", version="2.0.0")
app  = OpenAPI(__name__, info=info)
CORS(app)

#define tags
documentation_tag = Tag(
    name="Documentação", 
    description="Seleção de documentação: Swager")

home_tag = Tag(
    name="Inicial", 
    description="Página Inicial")

category_tag = Tag(
    name="categoria", 
    description="Operações relacionadas a categorias."
                "As requisições são redirecionadas para a API.",
    externalDocs={
        "description": "Documentação completa da API Category",
        "url": CATEGORY_API_URL
    }
)

bank_tag = Tag(
    name="Instituição Financeira", 
description="Operações relacionadas a Instituições Financeira. " 
            "As requisições são redirecionadas para a API.",
    externalDocs={
        "description": "Documentação completa da API Bank",
        "url": BANK_API_URL})

resource_tag = Tag(
    name="Recursos", 
description="Operações relacionadas a Instituições Financeira. " 
            "As requisições são redirecionadas para a API.",
    externalDocs={
        "description": "Documentação completa da API Resource",
        "url": RESOURCE_API_URL})

branch_tag = Tag(
    name="Agências Bancárias", 
description="Operações relacionadas a Agências Bancárias. " 
            "As requisições são redirecionadas para a API.",
    externalDocs={
        "description": "Documentação completa da API",
        "url": BRANCH_API_URL})

account_tag = Tag(
    name="Contas", 
description="Operações relacionadas a Contas. " 
            "As requisições são redirecionadas para a API.",
    externalDocs={
        "description": "Documentação completa da API Account",
        "url": ACCOUNT_API_URL})

transaction_tag = Tag(
    name="Transações", 
description="Operações relacionadas a Transações." 
            "As requisições são redirecionadas para a API.",
    externalDocs={
        "description": "Documentação completa da API Transaction",
        "url": TRANSACTION_API_URL})

#**************************************************************************************************
#* Decorator for errors                                                                           *
#**************************************************************************************************
def error_handling(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        
        except requests.exceptions.Timeout:
            logger.error(CONNECTION_ERROR_LOG)
            return jsonify({"error": API_TIMEOUT_MSG}), 504
        
        except requests.exceptions.ConnectionError:
            logger.error(CONNECTION_ERROR_LOG)
            return jsonify({"error": CONNECTION_ERROR_MSG}), 502
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao conectar com a API externa: {str(e)}")
            return jsonify({"error": f"Falha na comunicação com API externa: {str(e)}"}), 500
        
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            return jsonify({"status": "falha", "erro": str(e)}), 500
    return decorated_function

#**************************************************************************************************
#* Helper function for API redirection                                                            *
#**************************************************************************************************
def redirect_to_api(method, url, headers=None):
    """
    Auxilia a função no redirecionamento para diferentes métodos.
    """
    data = None
    if method in ['POST', 'PUT', 'PATCH', 'DELETE']:
        data = request.get_json()
        logger.debug(f"Dados recebidos: {data}")
     
    # Define os cabeçalhos, incluindo o cabeçalho de autenticação
    headers = headers or {}
    headers["Authorization"] = f"Bearer {API2_TOKEN}"
    headers["Content-Type"] = CONTENT_TYPE_JSON

    logger.debug(f"Cabeçalhos enviados: {headers}")
    
    response = requests.request(
        method=method,
        url=url,
        json=data,
        headers=headers, 
        timeout=10
    )
    response.raise_for_status()
    logger.debug(f"Resposta da API externa: {response.json()}")
    return jsonify({"status": "sucesso", "detalhes": response.json()}), response.status_code

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
#* categories                                                                                     *
#**************************************************************************************************
@app.get('/category', tags=[category_tag])
@error_handling
def category():
    """
    Redireciona as requisições GET para a API Category.
    """
    return redirect_to_api('GET', CATEGORY_API_URL)

@app.post('/category', tags=[category_tag])
@error_handling
def post_category(body: CategoriesSchema):
    """
    Redireciona as requisições POST para a API Category.
    """
    return redirect_to_api('POST', CATEGORY_API_URL)

@app.delete('/category', tags=[category_tag])
@error_handling
def delete_category(body: CategoriesSearchSchema):
    """
    Redireciona requisições DELETE para a API Category.
    """
    return redirect_to_api('DELETE', CATEGORY_API_URL)

@app.put('/category', tags=[category_tag])
@error_handling
def put_category(body: CategoriesSchema):
    """
    Redireciona as requisições PUT para a API Category.
    """
    return redirect_to_api('PUT', CATEGORY_API_URL)

@app.patch('/category', tags=[category_tag])
@error_handling
def patch_category(body: CategoriesUpdateSchema):
    """
    Redireciona as requisições PATCH para a API Category.
    """
    return redirect_to_api('PATCH', CATEGORY_API_URL)

#**************************************************************************************************
#* banks                                                                                          *
#**************************************************************************************************
@app.get('/bank', tags=[bank_tag])
@error_handling
def bank():
    """
    Redireciona as requisições GET para a API Bank.
    """
    return redirect_to_api('GET', BANK_API_URL)

@app.post('/bank', tags=[bank_tag])
@error_handling
def post_bank(body: BanksSchema):
    """
    Redireciona as requisições POST para a API Bank.
    """
    return redirect_to_api('POST', BANK_API_URL)

@app.delete('/bank', tags=[bank_tag])
@error_handling
def delete_bank(body: BanksSearchSchema):
    """
    Redireciona requisições DELETE para a API Bank.
    """
    return redirect_to_api('DELETE', BANK_API_URL)

@app.put('/bank', tags=[bank_tag])
@error_handling
def put_bank(body: BanksUpdateSchema):
    """
    Redireciona as requisições PUT para a API Bank.
    """
    return redirect_to_api('PUT', BANK_API_URL)

@app.patch('/bank', tags=[bank_tag])
@error_handling
def patch_bank(body: BanksSchema):
    """
    Redireciona as requisições PUT para a API Bank.
    """
    return redirect_to_api('PUT', BANK_API_URL)

#**************************************************************************************************
#* resources                                                                                      *
#**************************************************************************************************
@app.get('/resource', tags=[resource_tag])
@error_handling
def resource():
    """
    Redireciona as requisições GET para a API resource.
    """
    return redirect_to_api('GET', RESOURCE_API_URL)

@app.post('/resource', tags=[resource_tag])
@error_handling
def post_resource(body: ResourcesSchema):
    """
    Redireciona as requisições POST para a API resource.
    """
    return redirect_to_api('POST', RESOURCE_API_URL)

@app.delete('/resource', tags=[resource_tag])
@error_handling
def delete_resource(body: ResourcesSearchSchema):
    """
    Redireciona requisições DELETE para a API Resource.
    """
    return redirect_to_api('DELETE', RESOURCE_API_URL)

@app.put('/resource', tags=[resource_tag])
@error_handling
def put_resource(body: ResourcesSchema):
    """
    Redireciona as requisições PUT para a API Resource.
    """
    return redirect_to_api('PUT', RESOURCE_API_URL)

@app.patch('/resource', tags=[resource_tag])
@error_handling
def patch_resource(body: ResourcesUpdateSchema):
    """
    Redireciona as requisições PATCH para a API Resource.
    """
    return redirect_to_api('PATCH', RESOURCE_API_URL)

#**************************************************************************************************
#* branch                                                                                         *
#**************************************************************************************************
@app.get('/branch', tags=[branch_tag])
@error_handling
def branch():
    """
    Redireciona as requisições GET para a API Branch.
    """
    return redirect_to_api('GET', BRANCH_API_URL)

@app.post('/branch', tags=[branch_tag])
@error_handling
def post_branch(body: BranchesSchema):
    """
    Redireciona as requisições POST para a API branch.
    """
    return redirect_to_api('POST', BRANCH_API_URL)

@app.delete('/branch', tags=[branch_tag])
@error_handling
def delete_branch(body: BranchesSearchSchema):
    """
    Redireciona requisições DELETE para a API Branch.
    """
    return redirect_to_api('DELETE', BRANCH_API_URL)

@app.put('/branch', tags=[branch_tag])
@error_handling
def put_branch(body: BranchesSchema):
    """
    Redireciona as requisições PUT para a API Branch.
    """
    return redirect_to_api('PUT', BRANCH_API_URL)

@app.patch('/branch', tags=[branch_tag])
@error_handling
def patch_branch(body: BranchesSchema):
    """
    Redireciona as requisições PUT para a API Branch.
    """
    return redirect_to_api('PUT', BRANCH_API_URL)

#**************************************************************************************************
#* account                                                                                        *
#**************************************************************************************************
@app.get('/account', tags=[account_tag])
@error_handling
def account():
    """
    Redireciona as requisições GET para a API Account.
    """
    return redirect_to_api('GET', ACCOUNT_API_URL)

@app.post('/account', tags=[account_tag])
@error_handling
def post_account(body: AccountsSchema):
    """
    Redireciona as requisições POST para a API Account.
    """
    return redirect_to_api('POST', ACCOUNT_API_URL)

@app.delete('/account', tags=[account_tag])
@error_handling
def delete_account(body: AccountsSearchSchema):
    """
    Redireciona requisições DELETE para a API Account.
    """
    return redirect_to_api('DELETE', ACCOUNT_API_URL)

#**************************************************************************************************
#* transaction                                                                                    *
#**************************************************************************************************
@app.get('/transaction', tags=[transaction_tag])
@error_handling
def transaction():
    """
    Redireciona as requisições GET para a API Transaction.
    """
    return redirect_to_api('GET', TRANSACTION_API_URL)

@app.post('/transaction', tags=[transaction_tag])
@error_handling
def post_transaction(body: TransactionsSchema):
    """
    Redireciona as requisições POST para a API Transaction.
    """
    return redirect_to_api('POST', TRANSACTION_API_URL)

@app.delete('/transaction', tags=[transaction_tag])
@error_handling
def delete_transaction(body: TransactionsSearchSchema):
    """
    Redireciona requisições DELETE para a API Transaction.
    """
    return redirect_to_api('DELETE', TRANSACTION_API_URL)

@app.put('/transaction', tags=[transaction_tag])
@error_handling
def update_transaction(body: TransactionsSchema):
    """
    Redireciona as requisições PUT para a API Transaction.
    """
    return redirect_to_api('PUT', TRANSACTION_API_URL)