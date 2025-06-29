 # Loan Advisor – Backend (FastAPI + ML + Claude)

This is the backend system for the Loan Advisor application – a smart assistant that helps users find the best lender based on their profile. The backend leverages a machine learning model trained on synthetic lender eligibility data and generates human-readable explanations using Claude (Anthropic LLM).

Smart Loan Prediction using ML model

 Conversational Interface with Claude-powered explanations

 Dual Mode Support:

Chatbot-style interaction (/chat)

Structured form input (/predict-lenders)

 Request Logging to SQL Database

 FastAPI backend with modular, extensible design

Setup the venv using the requirements.txt


 Create the .env and add the keys:

 .env {
    
    CLAUDE_API_KEY=your_anthropic_key_here
    DATABASE_URL=mysql+pymysql://user:password@localhost/loan_advisor_db


 }


 Running command:uvicorn main:app --reload


 Developed by Nitheesh Vijayan
