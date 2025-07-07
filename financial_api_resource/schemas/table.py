from pydantic import BaseModel, Field
from typing import List, Optional

EXEMPLE_ID = "CRC"
EXEMPLE_DESCRIPTION = "CARTÃO DE CRÉDITO"
EXEMPLE_STATUS = "A"

# Schemas -------------------------------------------------------------------------------------
class ResourcesSchema(BaseModel):
    """ 
    Define como um dado a ser inserido, deve ser representado.
    """

    resource_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)
    resource_description: str = Field(..., max_length=40, example=EXEMPLE_DESCRIPTION)
    resource_status: str = Field(..., min_length=1, max_length=1, example=EXEMPLE_STATUS)

# Views Schemas -------------------------------------------------------------------------------
class ResourcesViewSchema(BaseModel):
    """ 
    Define como um novo dado deve ser representado.
    """

    resource_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)
    resource_description: str = Field(..., max_length=40, example=EXEMPLE_DESCRIPTION)
    resource_status: str = Field(..., min_length=1, max_length=1, example=EXEMPLE_STATUS)

# Listagens Schema ----------------------------------------------------------------------------
class ListResourcesSchema(BaseModel):
    """ 
    Define como uma listagem de dados será retornado. 
    """

    resources:List[ResourcesViewSchema]

# Del Schemas ---------------------------------------------------------------------------------
class ResourcesDelSchema(BaseModel):
    """ 
    Define como deve ser a estrutura do dado retornado após uma requisição de remoção. 
    """
    
    message: str
    resource_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)

# Busca Schemas -------------------------------------------------------------------------------
class ResourcesSearchSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca 
    que será feita apenas com base no ID. 
    """

    resource_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)

# Atualização Schemas ------------------------------------------------------------------------
class ResourcesUpdateSchema(BaseModel):
    """ 
    Define como um novo dado deve ser atualizado. 
    """

    resource_id: str = Field(..., min_length=1, max_length=3, example=EXEMPLE_ID)
    resource_description: Optional[str] = Field(None, max_length=40, example=EXEMPLE_DESCRIPTION)
    resource_status: Optional[str] = Field(None, max_length=1, example=EXEMPLE_STATUS)