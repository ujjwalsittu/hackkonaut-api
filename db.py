from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DATABASE_URL = "mysql+pymysql://hackonaut:admin123@165.232.189.107/hackonaut?charset=utf8mb4"
engine = create_engine(SQL_DATABASE_URL)

SessionDb = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
