import os
from sqlalchemy import create_engine, Column, Integer, Float, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    loan_amount = Column(Float)
    annual_income = Column(Float)
    employment_status = Column(String(50))
    credit_score = Column(Integer)
    loan_purpose = Column(String(50))
    gender = Column(String(10))
    lenders = Column(Text)
    llm_response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def log_prediction(user_input: dict, lenders: list, llm_response: str):
    from sqlalchemy.orm import Session
    import json

    session: Session = SessionLocal()
    try:
        entry = PredictionLog(
            loan_amount=user_input["loan_amount"],
            annual_income=user_input["annual_income"],
            employment_status=user_input["employment_status"],
            credit_score=user_input["credit_score"],
            loan_purpose=user_input["loan_purpose"],
            gender=user_input["gender"],
            lenders=json.dumps(lenders),
            llm_response=llm_response
        )
        session.add(entry)
        session.commit()
    except Exception as e:
        session.rollback()
        print("DB Logging Error:", str(e))
    finally:
        session.close()
