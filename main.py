from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import joblib
import json
import re
import pandas as pd
import numpy as np
from database import log_prediction
from chat_agent import chat_with_user
from fastapi.middleware.cors import CORSMiddleware


from llm import generate_llm_response  

app = FastAPI()
model = joblib.load("loan_lender_model.pkl")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

chat_memory = []


# ------------ Pydantic Models -------------
class UserInput(BaseModel):
    loan_amount: float
    annual_income: float
    employment_status: str
    credit_score: int
    loan_purpose: str
    gender: str

class LenderOutput(BaseModel):
    name: str
    interest_rate: float
    match_score: float

class PredictionResponse(BaseModel):
    llm_response: str
    top_lenders: List[LenderOutput]

class ChatQuery(BaseModel):
    message: str

# ------------ Lender Info for LLM and output ------------
LENDERS = [
    {"id": 1, "name": "FastCash Inc.", "interestRate": 12.5},
    {"id": 2, "name": "HomeFund Bank", "interestRate": 8.9},
    {"id": 3, "name": "EduFinance", "interestRate": 6.5},
    {"id": 4, "name": "BizGrow Capital", "interestRate": 10.5},
    {"id": 5, "name": "QuickPay Loans", "interestRate": 13.0},
    {"id": 6, "name": "CarCredit Bank", "interestRate": 9.5},
    {"id": 7, "name": "PersonalTrust", "interestRate": 11.2},
    {"id": 8, "name": "StartupFund", "interestRate": 12.0},
    {"id": 9, "name": "StudentLend", "interestRate": 7.0},
    {"id": 10, "name": "HouseEasy", "interestRate": 8.5},
    {"id": 11, "name": "FreelanceFlex", "interestRate": 12.7},
    {"id": 12, "name": "WomenEmpower Finance", "interestRate": 9.8},
    {"id": 13, "name": "GreenLoan Co.", "interestRate": 10.1},
    {"id": 14, "name": "EmergencyFund", "interestRate": 14.5},
    {"id": 15, "name": "GoldSecure Loans", "interestRate": 9.2}
]

# ------------ Prediction Endpoint ------------
@app.post("/predict-lenders", response_model=PredictionResponse)
async def predict_lenders(user: UserInput):
    try:
        df = pd.DataFrame([user.dict()])
        proba_list = model.predict_proba(df)

        lender_scores = []
        for i, lender in enumerate(LENDERS):
            prob_array = proba_list[i]
            if isinstance(prob_array[0], (list, np.ndarray)):
                prob = float(prob_array[0][1])
            else:
                prob = float(prob_array[1])
            lender_scores.append({
                "name": lender["name"],
                "interest_rate": lender["interestRate"],
                "match_score": round(prob, 4)
            })

        top_lenders = sorted(lender_scores, key=lambda x: x["match_score"], reverse=True)[:3]

        # Generate natural response using LLM
        llm_response = generate_llm_response(user.dict(), top_lenders)
        log_prediction(user.dict(), top_lenders, llm_response)


        return {"llm_response": llm_response, "top_lenders": top_lenders}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/chat")
async def chat_route(query: ChatQuery):
    try:
        chat_memory.append({"role": "user", "content": query.message})
        reply = chat_with_user(chat_memory)
        chat_memory.append({"role": "assistant", "content": reply})

        # Check if Claude triggered a prediction
        if "[READY_TO_PREDICT]" in reply:
            try:
                match = re.search(r"\{(.|\s)*\}", reply)
                if match:
                    json_data = json.loads(match.group(0))
                    from main import predict_lenders
                    prediction = await predict_lenders(UserInput(**json_data))
                    llm_response = prediction["llm_response"]
                    chat_memory.append({"role": "assistant", "content": llm_response})
                    return {"reply": llm_response}
                else:
                    return {"reply": "I couldn't extract the prediction input."}
            except Exception as e:
                return {"reply": f"Prediction failed: {str(e)}"}

        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Chat error: {str(e)}"}