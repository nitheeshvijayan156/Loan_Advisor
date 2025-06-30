import os
import anthropic

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def format_lenders(lenders):
    return "\n".join([
        f"- {l['name']} (Interest Rate: {l['interest_rate']}%, Score: {l['match_score']*100:.1f}%)"
        for l in lenders
    ])

def generate_llm_response(user_input: dict, top_lenders: list) -> str:
    prompt = f"""
You are a helpful loan advisor. A user has applied for a loan with these details:

- Loan Amount: {user_input['loan_amount']}
- Income: {user_input['annual_income']}
- Employment Status: {user_input['employment_status']}
- Credit Score: {user_input['credit_score']}
- Purpose: {user_input['loan_purpose']}

The system matched these top lenders:
{format_lenders(top_lenders)}

Write a friendly, clear explanation to the user about why these lenders were selected.Keep it short and to the point, focusing on the benefits of each lender for the user's situation. Avoid technical jargon and make it easy to understand.
"""

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=500,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()
