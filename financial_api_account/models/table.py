from sqlalchemy import Column, Integer, String 
from sqlalchemy.orm import declarative_base

# cria uma classe Base para o instanciamento de novos objetos/tabelas
Base = declarative_base()

class Accounts(Base):
    """
    Classe que representa a tabela de Constas no banco de dados.
    """
    __tablename__ = 'account'

    # Definição das colunas da tabela
    account_id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, primary_key=True)
    resource_id = Column(String, primary_key=True)

    def __init__(self, account_id:int, branch_id:int, resource_id:int):
        """
        Cria a tabela de contas

        Arguments:
            account_id: ID da conta
            branch_id: ID da filial
            resource_id: ID do recurso
        """
        self.account_id = account_id
        self.branch_id = branch_id
        self.resource_id = resource_id

    def to_dict(self):
        """
        Retorna um dicionário com os dados da categoria.
        Útil para serialização em JSON.
        """
        return {
            "account_id": self.account_id,
            "branch_id": self.branch_id,
            "resource_id": self.resource_id
        }
