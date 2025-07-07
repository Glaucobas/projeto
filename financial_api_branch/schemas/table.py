from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

EXEMPLE_ID = 1
EXEMPLE_DESCRIPTION = "CENTRO"
EXEMPLE_BANK = 1
EXEMPLE_CEP = 12345678 
EXEMPLE_ADDRESS = "Rua das Flores" 
EXEMPLE_NUMBER = "123"
EXEMPLE_COMPLEMENT = "APTO 101"
EXEMPLE_CITY = "São Paulo"  
EXAMPLE_DISTRICT = "Centro" 
EXEMPLE_STATE = "SP"
EXEMPLE_COUNTRY = "Brasil"
EXEMPLE_PHONE = "11987654321"  
EXEMPLE_EMAIL = "fulanodetal@email.com.br"  
EXEMPLE_WEBSITE = "http://www.exemplo.com.br"

# Schemas -------------------------------------------------------------------------------------
class BranchesSchema(BaseModel):
    """ 
    Define como um dado a ser inserido, deve ser representado.
    """
    
    branch_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)
    branch_description: str = Field(..., max_length=40, example=EXEMPLE_DESCRIPTION)  
    bank_id: int = Field(..., example=EXEMPLE_BANK)
    branch_cep: int = Field(..., example=EXEMPLE_CEP) 
    branch_address: Optional[str] = Field(None, max_length=40, example=EXEMPLE_ADDRESS)
    branch_number: Optional[str] = Field(None, min_length=1, max_length=10, example=EXEMPLE_NUMBER)   
    branch_complement: Optional[str] = Field(None, max_length=20, example=EXEMPLE_COMPLEMENT)
    branch_district: Optional[str] = Field(None, max_length=20, example=EXAMPLE_DISTRICT)
    branch_city: Optional[str] = Field(None, max_length=40, example=EXEMPLE_CITY)
    branch_state: Optional[str] = Field(None, min_length=2, max_length=2, example=EXEMPLE_STATE)   
    branch_country: Optional[str] = Field(None, max_length=40, example=EXEMPLE_COUNTRY)
    branch_phone: Optional[str] = Field(None, min_length=10, max_length=11, example=EXEMPLE_PHONE)
    branch_email: Optional[str] = Field(None, max_length=40, example=EXEMPLE_EMAIL)
    
# Views Schemas -------------------------------------------------------------------------------
class BranchesViewSchema(BaseModel):
    """ 
    Define como um novo dado deve ser representado. 
    """
    branch_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)
    branch_description: str = Field(..., max_length=40, example=EXEMPLE_DESCRIPTION)  
    bank_id: int = Field(..., example=EXEMPLE_BANK)
    branch_cep: int = Field(..., example=EXEMPLE_CEP) 
    branch_address: Optional[str] = Field(None, max_length=40, example=EXEMPLE_ADDRESS)
    branch_number: Optional[str] = Field(None, min_length=1, max_length=10, example=EXEMPLE_NUMBER)   
    branch_complement: Optional[str] = Field(None, max_length=20, example=EXEMPLE_COMPLEMENT)
    branch_district: Optional[str] = Field(None, max_length=20, example=EXAMPLE_DISTRICT)
    branch_city: Optional[str] = Field(None, max_length=40, example=EXEMPLE_CITY)
    branch_state: Optional[str] = Field(None, min_length=2, max_length=2, example=EXEMPLE_STATE)   
    branch_country: Optional[str] = Field(None, max_length=40, example=EXEMPLE_COUNTRY)
    branch_phone: Optional[str] = Field(None, min_length=10, max_length=11, example=EXEMPLE_PHONE)
    branch_email: Optional[str] = Field(None, max_length=40, example=EXEMPLE_EMAIL)

# Listagens Schema ----------------------------------------------------------------------------
class ListBranchesSchema(BaseModel):
    """ 
    Define como uma listagem de dados será retornado. 
    """

    branches:List[BranchesViewSchema]

# Del Schemas ---------------------------------------------------------------------------------
class BranchesDelSchema(BaseModel):
    """ 
    Define como deve ser a estrutura do dado retornado após uma requisição de remoção. 
    """
    
    message: str
    branch_id: int = Field(..., example=EXEMPLE_ID)

# Busca Schemas -------------------------------------------------------------------------------
class BranchesSearchSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca 
    que será feita apenas com base no ID. 
    """

    branch_id: int = Field(..., example=EXEMPLE_ID)

# Atualização Schemas ------------------------------------------------------------------------
class BranchesUpdateSchema(BaseModel):
    """ 
    Define como um novo dado deve ser atualizado.
    """
    branch_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)
    branch_description: Optional[str] = Field(None, max_length=40, example=EXEMPLE_DESCRIPTION)  
    bank_id: Optional[int] = Field(None, example=EXEMPLE_BANK)
    branch_cep: Optional[int] = Field(None, example=EXEMPLE_CEP) 
    branch_address: Optional[str] = Field(None, max_length=40, example=EXEMPLE_ADDRESS)
    branch_number: Optional[str] = Field(None, min_length=1, max_length=10, example=EXEMPLE_NUMBER)   
    branch_complement: Optional[str] = Field(None, max_length=20, example=EXEMPLE_COMPLEMENT)
    branch_district: Optional[str] = Field(None, max_length=20, example=EXAMPLE_DISTRICT)
    branch_city: Optional[str] = Field(None, max_length=40, example=EXEMPLE_CITY)
    branch_state: Optional[str] = Field(None, min_length=2, max_length=2, example=EXEMPLE_STATE)   
    branch_country: Optional[str] = Field(None, max_length=40, example=EXEMPLE_COUNTRY)
    branch_phone: Optional[str] = Field(None, min_length=10, max_length=11, example=EXEMPLE_PHONE)
    branch_email: Optional[str] = Field(None, max_length=40, example=EXEMPLE_EMAIL)
