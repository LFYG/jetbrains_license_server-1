from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    port = Column(Integer, nullable=False, unique=True)

    def __repr__(self):
        return "<{}(name='{}',port='{}')>".format(self.__class__.__name__, self.name, self.port)
