 # **Loan Advisor – Backend (FastAPI + ML + Claude)**

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
    DATABASE_URL=mysql+pymysql://user:password@db/loan_advisor_db


 }


 Running command:uvicorn main:app --reload


## DOCKER yml (Place the yml file mentioned in the root directory of both frontend and backend)

version: '3.8'

services:
  db:
    image: mysql:8.0
    container_name: db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: your password
      MYSQL_DATABASE: loan_advisor_db
    ports:
      - "3307:3306"
    volumes:
      - db_data:/var/lib/mysql

  backend:
    build:
      context: ./Loan_Advisor
    container_name: backend
    restart: always
    depends_on:
      - db
    env_file:
      - ./Loan_Advisor/.env
    command: >
      sh -c "
        echo ' Waiting for MySQL...' &&
        until nc -z db 3306; do
          sleep 1
        done &&
        echo ' MySQL is up. Starting FastAPI...' &&
        uvicorn main:app --host 0.0.0.0 --port 8000
      "
    ports:
      - "8000:8000"
    volumes:
      - ./Loan_Advisor:/app
    working_dir: /app

  frontend:
    build:
      context: ./Loan_Advisor_frontend
      dockerfile: Dockerfile
    container_name: frontend
    restart: always
    ports:
      - "5173:5173"
    volumes:
      - ./Loan_Advisor_frontend:/app
    working_dir: /app
    command: sh -c "npm install && npm run dev -- --host"

volumes:
  db_data:



 Developed by Nitheesh Vijayan
