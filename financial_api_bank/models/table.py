from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

# cria uma classe Base para o instanciamento de novos objetos/tabelas
Base = declarative_base()

# Cadastro de Bancos
class Banks(Base):
    """
    Classe que representa a tabela de Intituições Financeiras do banco de dados.
    """
    __tablename__ = 'bank'

    bank_id = Column(Integer, primary_key=True)
    bank_description = Column(String(40), nullable=True)
    bank_ispb = Column(String(8), nullable=True)
    bank_fullname = Column(String(100), nullable=True)

    
    def to_dict(self):
        """
        Retorna um dicionário com os dados do banco.
        """
        return {
            'bank_id': self.bank_id,
            'bank_description': self.bank_description,
            'bank_ispb': self.bank_ispb,
            'bank_fullname': self.bank_fullname
        }
