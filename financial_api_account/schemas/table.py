from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

EXEMPLE = 123
EXEMPLE_RESOURCE = "CRC"

# Schemas -------------------------------------------------------------------------------------
class AccountsSchema(BaseModel):
    """ 
    Define como um dado a ser inserido, deve ser representado.
    """

    account_id: int = Field(..., example=EXEMPLE)
    branch_id: int = Field(...,  example=EXEMPLE)
    resource_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_RESOURCE)

# Views Schemas -------------------------------------------------------------------------------
class AccountsViewSchema(BaseModel):
    """ 
    Define como um novo dado deve ser representado.
    """

    account_id: int = Field(..., example=EXEMPLE)
    branch_id: int = Field(...,  example=EXEMPLE)
    resource_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_RESOURCE)

# Listagens Schema ----------------------------------------------------------------------------
class ListAccountsSchema(BaseModel):
    """ 
    Define como uma listagem de dados será retornado.  
    """

    accounts:List[AccountsViewSchema]

# Del Schemas ---------------------------------------------------------------------------------
class AccountsDelSchema(BaseModel):
    """ 
    Define como deve ser a estrutura do dado retornado após uma requisição de remoção.
    """
    
    message: str
    account_id: str = Field(..., example=EXEMPLE)
    branch_id: int = Field(...,  example=EXEMPLE)
    resource_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_RESOURCE)
    
# Busca Schemas -------------------------------------------------------------------------------
class AccountsSearchSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca 
    que será feita apenas com base no ID.
    """

    account_id: int = Field(..., example=EXEMPLE)
    branch_id: int = Field(...,  example=EXEMPLE)
    resource_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_RESOURCE)