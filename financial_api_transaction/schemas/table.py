from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

EXEMPLE_ID = 123
EXEMPLE_DESCRIPTION = "CONTA DE ÁGUA"
EXEMPLE_CATEGORY = "DPI"
EXEMPLE_ACCOUNT = 123456
EXEMPLE_BRANCH = 123456 
EXEMPLE_RESOURCE = "CRD"
EXEMPLE_TYPE = "D"  # D para débito, C para crédito
EXEMPLE_VALUE = 123.45
EXEMPLE_STATUS = "P"  # P para paga, A para agendada, C para cancelada, I para inativa, V para vencida'

# Schemas -------------------------------------------------------------------------------------
class TransactionsSchema(BaseModel):
    """ 
    Define como um dado a ser inserido, deve ser representado.
    """
    
    transaction_id:  int = Field(..., examples=[EXEMPLE_ID])
    transaction_date: datetime = Field(..., examples=[datetime.today().strftime("%d/%m/%Y")])
    transaction_expiration_date: datetime = Field(..., examples=[datetime.today().strftime("%d/%m/%Y")])
    transaction_description: str = Field(..., max_length=200, examples=[EXEMPLE_DESCRIPTION])
    category_id: Optional[str] = Field(None, min_length=1, max_length=3, examples=[EXEMPLE_CATEGORY])
    account_id:  int = Field(..., examples=[EXEMPLE_ACCOUNT])
    branch_id:  int = Field(..., examples=[EXEMPLE_BRANCH])
    resource_id: str = Field(..., min_length=1, max_length=3, examples=[EXEMPLE_RESOURCE])
    transaction_type: str = Field(..., min_length=1, max_length=1, examples=[EXEMPLE_TYPE])
    transaction_value: float = Field(..., examples=[EXEMPLE_VALUE])
    transaction_status: str = Field(..., min_length=1, max_length=1, examples=[EXEMPLE_STATUS])

# Views Schemas -------------------------------------------------------------------------------
class TransactionsViewSchema(BaseModel):
    """ 
    Define como um novo dado deve ser representado. 
    """

    transaction_id:  int = Field(..., examples=[EXEMPLE_ID])
    transaction_date: datetime = Field(..., examples=[datetime.today().strftime("%d/%m/%Y")])
    transaction_expiration_date: datetime = Field(..., examples=[datetime.today().strftime("%d/%m/%Y")])
    transaction_description: str = Field(..., max_length=200, examples=[EXEMPLE_DESCRIPTION])
    category_id: Optional[str] = Field(None, min_length=1, max_length=3, examples=[EXEMPLE_CATEGORY])
    account_id:  int = Field(..., examples=[EXEMPLE_ACCOUNT])
    branch_id:  int = Field(..., examples=[EXEMPLE_BRANCH])
    resource_id: str = Field(..., min_length=1, max_length=3, examples=[EXEMPLE_RESOURCE])
    transaction_type: str = Field(..., min_length=1, max_length=1, examples=[EXEMPLE_TYPE])
    transaction_value: float = Field(..., examples=[EXEMPLE_VALUE])
    transaction_status: str = Field(..., min_length=1, max_length=1, examples=[EXEMPLE_STATUS])

# Listagens Schema ----------------------------------------------------------------------------
class ListTransactionsSchema(BaseModel):
    """ 
    Define como uma listagem de dados será retornado. 
    """

    transactions:List[TransactionsViewSchema]

# Del Schemas ---------------------------------------------------------------------------------
class TransactionsDelSchema(BaseModel):
    """ 
    Define como deve ser a estrutura do dado retornado após uma requisição de remoção. 
    """
    
    message: str
    transaction_id:  int = Field(..., examples=[EXEMPLE_ID])

# Busca Schemas -------------------------------------------------------------------------------
class TransactionsSearchSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca 
    que será feita apenas com base no ID. 
    """

    transaction_id:  int = Field(..., examples=[EXEMPLE_ID])

# Atualização Schemas ------------------------------------------------------------------------
class TransactionsUpdateSchema(BaseModel):
    """ 
    Define como um novo dado deve ser atualizado. 
    """

    transaction_id:  int = Field(..., examples=[EXEMPLE_ID])
    transaction_date: Optional[datetime] = Field(None, examples=[datetime.today().strftime("%d/%m/%Y")])
    transaction_expiration_date:  Optional[datetime] = Field(None, examples=[datetime.today().strftime("%d/%m/%Y")])
    transaction_description:  Optional[str] = Field(None, max_length=200, examples=[EXEMPLE_DESCRIPTION])
    category_id:  Optional[str] = Field(None, min_length=1, max_length=3, examples=[EXEMPLE_CATEGORY])
    account_id:   Optional[int] = Field(None, examples=[EXEMPLE_ACCOUNT])
    branch_id:   Optional[int] = Field(None, examples=[EXEMPLE_BRANCH])
    resource_id:  Optional[str] = Field(None, min_length=1, max_length=3, examples=[EXEMPLE_RESOURCE])
    transaction_type:  Optional[str] = Field(None, min_length=1, max_length=1, examples=[EXEMPLE_TYPE])
    transaction_value:  Optional[float] = Field(None, examples=[EXEMPLE_VALUE])
    transaction_status:  Optional[str] = Field(None, min_length=1, max_length=1, examples=[EXEMPLE_STATUS])

class TransactionsClass(BaseModel):
    """ 
    Define como será tratado o modelo de classificação. 
    """
    transaction_id:  int = Field(..., examples=[EXEMPLE_ID])
    transaction_description: str = Field(..., max_length=200, examples=[EXEMPLE_DESCRIPTION])