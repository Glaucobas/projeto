from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

# cria uma classe Base para o instanciamento de novos objetos/tabelas
Base = declarative_base()

class Resources(Base):
    """
    Classe que representa a tabela de Recursos no banco de dados.
    """
    __tablename__ = 'resource'

    # Definição das colunas da tabela
    resource_id = Column(String(3), primary_key=True)
    resource_description = Column(String(40),  nullable=False)
    resource_status = Column(String(1),  nullable=False)

    def __init__(self, resource_id:str, resource_description:str, resource_status:str):
        """
        Cria a tabela de categoria

        Arguments:
            resource_id: Código do recurso
            resource_description: Descrição do recurso
            resource_status: Informa se o recurso está ativo ou não
        """
        self.resource_id = resource_id
        self.resource_description = resource_description
        self.resource_status = resource_status

    def to_dict(self):
        """
        Retorna um dicionário com os dados do recurso.
        Útil para serialização em JSON.
        """
        return {
            "resource_id": self.resource_id,
            "resource_description": self.resource_description,
            "resource_status": self.resource_status
        }
