from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.orm import declarative_base
from datetime import datetime, date
from typing import Optional 

# cria uma classe Base para o instanciamento de novos objetos/tabelas
Base = declarative_base()

class Transactions(Base):
    """
    Classe que representa a tabela de transações no banco de dados.
    """
    __tablename__ = 'transaction'

    # Definição das colunas da tabela
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_date = Column(Date, default=datetime.today, nullable=False)
    transaction_expiration_date = Column(Date, default=datetime.today, nullable=False)
    transaction_description = Column(String(200), nullable=False)
    category_id = Column(String(3), nullable=True)
    account_id = Column(Integer, nullable=False)
    branch_id = Column(Integer, nullable=False)
    resource_id = Column(String(3), nullable=False)
    transaction_type = Column(String(1), nullable=False)
    transaction_value = Column(Float, nullable=False)
    transaction_status = Column(String(1), nullable=False)

    def __init__(self, transaction_id:int, transaction_date:date,  
                 transaction_expiration_date:date, transaction_description:str,
                 account_id: int, branch_id:int, resource_id:str, transaction_type:str, 
                 transaction_value:float, transaction_status:str,  category_id: Optional[str] = None):
        """
        Cria a tabela de categoria

        Arguments:
            transaction_id: ID da transação (chave primária)
            transaction_date: Data da transação
            transaction_expiration_date: Data de expiração da transação
            transaction_description: Descrição da transação
            category_id: ID da categoria associada à transação
            account_id: ID da conta associada à transação
            branch_id: ID da agência associada à transação 
            resource_id: ID do recurso associado à transação
            transaction_type: Tipo da transação (D para débito, C para crédito)
            transaction_value: Valor da transação
            transaction_status: Status da transação (A para ativo, I para inativo)
        """
        self.transaction_id = transaction_id
        self.transaction_date = transaction_date
        self.transaction_expiration_date = transaction_expiration_date
        self.transaction_description = transaction_description
        self.category_id = category_id
        self.account_id = account_id   
        self.branch_id = branch_id
        self.resource_id = resource_id  
        self.transaction_type = transaction_type
        self.transaction_value = transaction_value 
        self.transaction_status = transaction_status 

    def to_dict(self):
        """
        Retorna um dicionário com os dados da categoria.
        Útil para serialização em JSON.
        """
        return {
            'transaction_id': self.transaction_id,
            'transaction_date': self.transaction_date,
            'transaction_expiration_date': self.transaction_expiration_date,
            'transaction_description': self.transaction_description,
            'category_id': self.category_id,
            'account_id': self.account_id,
            'branch_id': self.branch_id,
            'resource_id': self.resource_id,
            'transaction_type': self.transaction_type,
            'transaction_value': self.transaction_value,
            'transaction_status': self.transaction_status
        }