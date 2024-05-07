from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

username = 'root'
password = 'Thanhhuyen2002'
host = 'localhost'
port = 3306

engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:3306/checkin')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
