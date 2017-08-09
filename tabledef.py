from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('postgresql://postgres:postgres@localhost/tutorial', echo=True)
Base = declarative_base()

class User(Base):
    """"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        """"""
        self.username = username
        self.password = password

class OTP(Base):
    """"""
    __tablename__ = "otp"

    id = Column(Integer, primary_key=True)
    otp = Column(String)

# create tables
Base.metadata.create_all(engine)
