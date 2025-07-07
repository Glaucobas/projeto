from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

# cria uma classe Base para o instanciamento de novos objetos/tabelas
Base = declarative_base()

class Categories(Base):
    """
    Classe que representa a tabela de categorias no banco de dados.
    """
    __tablename__ = 'category'

    # Definição das colunas da tabela
    category_id = Column(String(3), primary_key=True)
    category_description = Column(String(40),  nullable=False)
    category_type = Column(String(1),  nullable=False)

    def __init__(self, category_id:str, category_description:str, category_type:str):
        """
        Cria a tabela de categoria

        Arguments:
            id_category: Código da categoria de lançamento
            type: Informa se a conta é um débito ou crédito
        """
        self.category_id = category_id
        self.category_description = category_description
        self.category_type = category_type

    def to_dict(self):
        """
        Retorna um dicionário com os dados da categoria.
        Útil para serialização em JSON.
        """
        return {
            "category_id": self.category_id,
            "category_description": self.category_description,
            "category_type": self.category_type
        }
