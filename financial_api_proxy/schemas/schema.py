from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

#**************************************************************************************************
#* categories                                                                                     *
#**************************************************************************************************
EXEMPLE_ID = "DPI"
EXEMPLE_DESCRIPTION ="DESPESAS DE INVESTIMENTO"
EXEMPLE_TYPE = "D"

class CategoriesSchema(BaseModel):
    """ 
    Define como uma nova Categoria a ser inserida deve ser representada.
    """

    category_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)
    category_description: str = Field(..., max_length=40, example=EXEMPLE_DESCRIPTION)
    category_type: str = Field(..., min_length=1, max_length=1, example=EXEMPLE_TYPE)

class CategoriesSearchSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca que será feita apenas com 
    base no nome da Categoria. 
    """

    category_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)

class CategoriesUpdateSchema(BaseModel):
    """ 
    Define como uma nova Categoria deve ser representada 
    """

    category_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)
    category_description: Optional[str] = Field(None, max_length=40, example=EXEMPLE_DESCRIPTION)
    category_type: Optional[str] = Field(None, min_length=1, max_length=1, example=EXEMPLE_TYPE)

#**************************************************************************************************
#* Banks                                                                                          *
#**************************************************************************************************
EXEMPLE_ID = 1
EXEMPLE_DESCRIPTION = "BANCO DO BRASIL S.A."
EXAMPLE_ISPB = "00000000"
EXAMPLE_FULLNAME = "Banco do Brasil S.A." 

class BanksSchema(BaseModel):
    """ 
    Define como um dado a ser inserido, deve ser representado.
    """
    bank_id: int = Field(..., example=EXEMPLE_ID)
    bank_description: Optional[str] = Field(None, max_length=40, example=EXEMPLE_DESCRIPTION)
    bank_ispb: Optional[str] = Field(None, max_length=8, example=EXAMPLE_ISPB)
    bank_fullname: Optional[str] = Field(None, max_length=100, example=EXAMPLE_FULLNAME)

class BanksSearchSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca 
    que será feita apenas com base no ID.  
    """

    bank_id: int = Field(..., example=EXEMPLE_ID)

class BanksUpdateSchema(BaseModel):
    """ 
    Define como um novo dado deve ser atualizado.
    """

    bank_id: int = Field(..., example=EXEMPLE_ID)
    bank_description: Optional[str] = Field(None, max_length=40, example=EXEMPLE_DESCRIPTION)
    bank_ispb: Optional[str] = Field(None, max_length=8, example=EXAMPLE_ISPB)
    bank_fullname: Optional[str] = Field(None, max_length=100, example=EXAMPLE_FULLNAME)

#**************************************************************************************************
#* Resurces                                                                                       *
#**************************************************************************************************
EXEMPLE_ID = "CRC"
EXEMPLE_DESCRIPTION = "CARTÃO DE CRÉDITO"
EXEMPLE_STATUS = "A"

class ResourcesSchema(BaseModel):
    """ 
    Define como um dado a ser inserido, deve ser representado.
    """

    resource_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)
    resource_description: str = Field(..., max_length=40, example=EXEMPLE_DESCRIPTION)
    resource_status: str = Field(..., min_length=1, max_length=1, example=EXEMPLE_STATUS)

class ResourcesSearchSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca 
    que será feita apenas com base no ID. 
    """

    resource_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)

class ResourcesUpdateSchema(BaseModel):
    """ 
    Define como um novo dado deve ser atualizado. 
    """

    resource_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)
    resource_description: Optional[str] = Field(None, max_length=40, example=EXEMPLE_DESCRIPTION)
    resource_status: Optional[str] = Field(None, max_length=1, example=EXEMPLE_STATUS)

#**************************************************************************************************
#* branches                                                                                       *
#**************************************************************************************************
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

class BranchesSchema(BaseModel):
    """ 
    Define como um dado a ser inserido, deve ser representado.
    """
    
    branch_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)
    branch_description: str = Field(None, max_length=40, example=EXEMPLE_DESCRIPTION)  
    bank_id: int = Field(None, example=EXEMPLE_BANK)
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
    
class BranchesSearchSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca 
    que será feita apenas com base no ID. 
    """

    branch_id: int = Field(..., example=EXEMPLE_ID)

class BranchesUpdateSchema(BaseModel):
    """ 
    Define como um novo dado deve ser atualizado.
    """
    branch_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)
    branch_description: Optional[str] = Field(None, max_length=40, example=EXEMPLE_DESCRIPTION)  
    bank_id: Optional[int] = Field(None, example=EXEMPLE_BANK)
    branch_cep: Optional[int] = Field(None,  example=EXEMPLE_CEP) 
    branch_address: Optional[str] = Field(None, max_length=40, example=EXEMPLE_ADDRESS)
    branch_number: Optional[str] = Field(None, min_length=1, max_length=10, example=EXEMPLE_NUMBER)   
    branch_complement: Optional[str] = Field(None, max_length=20, example=EXEMPLE_COMPLEMENT)
    branch_district: Optional[str] = Field(None, max_length=20, example=EXAMPLE_DISTRICT)
    branch_city: Optional[str] = Field(None, max_length=40, example=EXEMPLE_CITY)
    branch_state: Optional[str] = Field(None, min_length=2, max_length=2, example=EXEMPLE_STATE)   
    branch_country: Optional[str] = Field(None, max_length=40, example=EXEMPLE_COUNTRY)
    branch_phone: Optional[str] = Field(None, min_length=10, max_length=11, example=EXEMPLE_PHONE)
    branch_email: Optional[str] = Field(None, max_length=40, example=EXEMPLE_EMAIL)

#**************************************************************************************************
#* Acccount                                                                                       *
#**************************************************************************************************
EXEMPLE = 123
EXEMPLE_RESOURCE = "CRC"

class AccountsSchema(BaseModel):
    """ 
    Define como um dado a ser inserido, deve ser representado.
    """

    account_id: int = Field(..., example=EXEMPLE)
    branch_id: int = Field(...,  example=EXEMPLE)
    resource_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_RESOURCE)
 
class AccountsSearchSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca 
    que será feita apenas com base no ID.
    """

    account_id: int = Field(..., example=EXEMPLE)
    branch_id: int = Field(...,  example=EXEMPLE)
    resource_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_RESOURCE)

class AccountsUpdateSchema(BaseModel):
    """ 
    Define como uma nova Conta deve ser atualizada. 
    """

    account_id: int = Field(..., example=EXEMPLE)
    branch_id: Optional[int] = Field(None, example=EXEMPLE)
    resource_id: Optional[str] = Field(None, min_length=1, max_length=3, example=EXEMPLE_RESOURCE)

#**************************************************************************************************
#* Transaction                                                                                    *
#**************************************************************************************************
EXEMPLE_ID = 123
EXEMPLE_DESCRIPTION = "CONTA DE ÁGUA"
EXEMPLE_CATEGORY = "DPI"
EXEMPLE_ACCOUNT = 123456
EXEMPLE_BRANCH = 123456 
EXEMPLE_RESOURCE = "CRD"
EXEMPLE_TYPE = "D"  # D para débito, C para crédito
EXEMPLE_VALUE = 123.45
EXEMPLE_STATUS = "P"  # P para paga, A para agendada, C para cancelada, I para inativa, V para vencida'

class TransactionsSchema(BaseModel):
    """ 
    Define como um dado a ser inserido, deve ser representado.
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

class TransactionsSearchSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca 
    que será feita apenas com base no ID. 
    """

    transaction_id:  int = Field(..., example=EXEMPLE_ID)

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