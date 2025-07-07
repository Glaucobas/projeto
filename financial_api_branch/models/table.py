from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

# cria uma classe Base para o instanciamento de novos objetos/tabelas
Base = declarative_base()

class Branches(Base):
    """
    Classe que representa a tabela de Agencias no banco de dados.
    """
    __tablename__ = 'branch'

    # Definição das colunas da tabela
    branch_id = Column(Integer, primary_key=True)
    branch_description = Column(String(40), nullable=False)
    bank_id = Column(Integer, nullable=False)
    branch_cep = Column(Integer, nullable=True)
    branch_address = Column(String(40), nullable=True) 
    branch_number = Column(String(10), nullable=True)
    branch_complement = Column(String(20), nullable=True)
    branch_district = Column(String(20), nullable=True)
    branch_city = Column(String(20), nullable=True)   
    branch_state = Column(String(2), nullable=True)
    branch_country = Column(String(20), nullable=True)
    branch_phone = Column(String(20), nullable=True)  
    branch_email = Column(String(40), nullable=True)  
    
    def __init__(self, branch_id: int, branch_description: str, bank_id: int, 
                 branch_cep: int, branch_address: str, branch_number: str, 
                 branch_complement: str, branch_district: str, branch_city: str,
                 branch_state: str, branch_country: str, branch_phone: str, 
                 branch_email: str):
        """
        Cria a tabela de Agencias.

        Arguments:
            branch_id: Código da categoria de lançamento
            branch_description: Descrição da Agencia
            bank_id: Código do Intituição Financeira
            branch_cep: CEP da Agencia
            branch_address: Endereço da Agencia
            branch_number: Número da Agencia
            branch_complement: Complemento do Endereço da Agencia
            branch_district: Bairro da Agencia
            branch_city: Cidade da Agencia
            branch_state: Estado da Agencia
            branch_country: País da Agencia
            branch_phone: Telefone da Agencia
            branch_email: E-mail da Agencia

        """
        self.branch_id = branch_id
        self.branch_description = branch_description
        self.bank_id = bank_id 
        self.branch_cep = branch_cep
        self.branch_address = branch_address   
        self.branch_number = branch_number
        self.branch_complement = branch_complement
        self.branch_district = branch_district
        self.branch_city = branch_city
        self.branch_state = branch_state
        self.branch_country = branch_country
        self.branch_phone = branch_phone
        self.branch_email = branch_email

    def to_dict(self):
        """
        Retorna um dicionário com os dados da categoria.
        Útil para serialização em JSON.
        """
        return {
            'branch_id': self.branch_id,
            'branch_description': self.branch_description,
            'bank_id': self.bank_id,
            'branch_cep': self.branch_cep,
            'branch_address': self.branch_address,
            'branch_number': self.branch_number,
            'branch_complement': self.branch_complement,
            'branch_city': self.branch_city,
            'branch_state': self.branch_state,
            'branch_country': self.branch_country,
            'branch_phone': self.branch_phone,
            'branch_email': self.branch_email,
        }