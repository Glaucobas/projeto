from pydantic import BaseModel, Field
from typing import List, Optional

EXEMPLE_ID = 1
EXEMPLE_DESCRIPTION = "BANCO DO BRASIL S.A."
EXAMPLE_ISPB = "00000000"
EXAMPLE_FULLNAME = "Banco do Brasil S.A." 

# Schemas -------------------------------------------------------------------------------------
class BanksSchema(BaseModel):
    """ 
    Define como um dado a ser inserido, deve ser representado.
    """

    bank_id: int = Field(..., example=EXEMPLE_ID)
    bank_description: Optional[str] = Field(None, max_length=40, example=EXEMPLE_DESCRIPTION)
    bank_ispb: Optional[str] = Field(None, max_length=8, example=EXAMPLE_ISPB)
    bank_fullname: Optional[str] = Field(None, max_length=100, example=EXAMPLE_FULLNAME)

# Views Schemas -------------------------------------------------------------------------------
class BanksViewSchema(BaseModel):
    """ 
    Define como um novo dado deve ser representado.  
    """

    bank_id: int = Field(..., example=EXEMPLE_ID)
    bank_description: Optional[str] = Field(None, max_length=40, example=EXEMPLE_DESCRIPTION)
    bank_ispb: Optional[str] = Field(None, max_length=8, example=EXAMPLE_ISPB)
    bank_fullname: Optional[str] = Field(None, max_length=100, example=EXAMPLE_FULLNAME)

# Listagens Schema ----------------------------------------------------------------------------
class ListBanksSchema(BaseModel):
    """ 
    Define como uma listagem de dados será retornado.
    """

    banks:List[BanksViewSchema]

# Del Schemas ---------------------------------------------------------------------------------
class BanksDelSchema(BaseModel):
    """ 
    Define como deve ser a estrutura do dado retornado após uma requisição de remoção.  
    """
    
    message: str
    bank_id: int = Field(..., example=EXEMPLE_ID)

# Busca Schemas -------------------------------------------------------------------------------
class BanksSearchSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca 
    que será feita apenas com base no ID.  
    """

    bank_id: int = Field(..., example=EXEMPLE_ID)

# Atualização Schemas ------------------------------------------------------------------------
class BanksUpdateSchema(BaseModel):
    """ 
    Define como um dado deve ser atualizado.
    """

    bank_id: int = Field(..., example=EXEMPLE_ID)
    bank_description: Optional[str] = Field(None, max_length=40, example=EXEMPLE_DESCRIPTION)
    bank_ispb: Optional[str] = Field(None, max_length=8, example=EXAMPLE_ISPB)
    bank_fullname: Optional[str] = Field(None, max_length=100, example=EXAMPLE_FULLNAME)