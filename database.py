from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base = declarative_base()
engine = create_engine("postgresql://darkroom9282:v2mzt67cZYDdAq@168.138.150.79:49154/ecologicDEV")
session = sessionmaker(bind=engine)

