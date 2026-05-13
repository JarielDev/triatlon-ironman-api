from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Creamos el archivo de la base de datos local
SQLALCHEMY_DATABASE_URL = "sqlite:///./triatlon_ironman.db"

# El engine es el puente entre Python y SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para nuestros modelos de base de datos
Base = declarative_base()