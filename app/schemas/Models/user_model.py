from app.db.connection import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f'<User(id={self.id}, name={self.name}>'
