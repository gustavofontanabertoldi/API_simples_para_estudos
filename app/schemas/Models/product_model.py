from app.db.connection import Base
from sqlalchemy import Column, Integer, String

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    def __repr__(self):
        return f'<Item(id={self.id}, name={self.name}>'

