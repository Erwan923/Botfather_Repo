from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Créez une instance de l'Engine avec la base de données SQLite
engine = create_engine('sqlite:///archivebot.db')

# Liez l'objet MetaData à l'Engine
metadata = MetaData(bind=engine)

# Utilisez le MetaData lié pour créer la base déclarative
base = declarative_base(metadata=metadata)

