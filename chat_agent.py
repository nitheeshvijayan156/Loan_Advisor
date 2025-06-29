import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """
You are LoanBot, a helpful assistant that helps users apply for loans and get matched to lenders.
You must collect the following fields step by step from the user:
- loan_amount
- annual_income
- employment_status
- credit_score
- loan_purpose
- gender

Always speak conversationally.

Once you have **all 6 fields**, respond with:
[READY_TO_PREDICT]
{{
  "loan_amount": <number>,
  "annual_income": <number>,
  "employment_status": "<string>",
  "credit_score": <int>,
  "loan_purpose": "<string>",
  "gender": "<string>"
}}

Then stop talking and wait for backend to process prediction and reply.
"""

def chat_with_user(history: list) -> str:
    response = client.messages.create(
        model="claude-3-opus-20240229",
        system=SYSTEM_PROMPT,
        max_tokens=600,
        messages=history,
        temperature=0.7
    )
    return response.content[0].text.strip()
