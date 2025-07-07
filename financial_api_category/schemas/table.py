from pydantic import BaseModel, Field
from typing import List, Optional

EXEMPLE_ID = "DPI"
EXEMPLE_DESCRIPTION = "DESPESAS DE INVESTIMENTO"
EXEMPLE_TYPE = "D"

# Schemas -------------------------------------------------------------------------------------
class CategoriesSchema(BaseModel):
    """ 
    Define como um novo dado a ser inserido, deve ser representado.
    """

    category_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)
    category_description: Optional[str] = Field(None, max_length=40, example=EXEMPLE_DESCRIPTION)
    category_type: Optional[str] = Field(None, max_length=1, example=EXEMPLE_TYPE)

# Views Schemas -------------------------------------------------------------------------------
class CategoriesViewSchema(BaseModel):
    """ 
    Define como um novo dado deve ser representado. 
    """

    category_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)
    category_description: Optional[str] = Field(None, max_length=40, example=EXEMPLE_DESCRIPTION)
    category_type: Optional[str] = Field(None, max_length=1, example=EXEMPLE_TYPE)

# Listagens Schema ----------------------------------------------------------------------------
class ListCategoriesSchema(BaseModel):
    """ 
    Define como uma listagem de dados será retornada. 
    """

    categories:List[CategoriesViewSchema]

# Del Schemas ---------------------------------------------------------------------------------
class CategoriesDelSchema(BaseModel):
    """ 
    Define como deve ser a estrutura do dado retornado após uma requisição de remoção. 
    """
    
    message: str
    category_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)

# Busca Schemas -------------------------------------------------------------------------------
class CategoriesSearchSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca 
    que será feita apenas com base no ID. 
    """

    category_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)

# Atualização Schemas ------------------------------------------------------------------------
class CategoriesUpdateSchema(BaseModel):
    """ 
    Define como um novo dado deve ser atualizado. 
    """
    
    category_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)
    category_description: Optional[str] = Field(None, max_length=40, example=EXEMPLE_DESCRIPTION)
    category_type: Optional[str] = Field(None, max_length=1, example=EXEMPLE_TYPE)