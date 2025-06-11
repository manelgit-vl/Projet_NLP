from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///questions.db", echo=False)
SessionLocal = sessionmaker(bind=engine)


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    texte = Column(Text)
    reponse = Column(Text)
    type_info = Column(String(50))  # "competence", "mission", "salaire"

# Créer la table si elle n'existe pas
Base.metadata.create_all(bind=engine)
