import os
import json
from openai import OpenAI

SYSTEM_PROMPT = """You are a B2B sales assistant. When given a customer inquiry, analyze it and return a JSON object with exactly these fields:

- intent_level: "High", "Medium", or "Low" based on budget clarity, timeline urgency, and need specificity
- intent_reason: one sentence explaining the intent level judgment
- ai_analysis: a concise summary of the customer's key pain points and requirements (in Chinese, 2-3 sentences)
- email_draft: a professional English reply email. Use placeholders [Customer Name] for the name. The email should acknowledge their inquiry, show understanding, propose next steps, and end with a signature from "AI Consultation Team"
- follow_up_date: a suggested follow-up date in YYYY-MM-DD format. High intent = 2 days from now, Medium = 5 days, Low = 14 days

Rules:
- If budget is clearly stated and high, timeline is urgent (e.g., "ASAP", "this month"), or need is very specific → likely High
- If budget is vague, timeline is flexible, or need is general → likely Medium
- If budget is "none" / "just browsing", timeline is "no rush" / far future, or no specific need → likely Low

Return ONLY valid JSON, no other text. Do not wrap in markdown code blocks."""


def analyze_customer(name, email, company="", need="", budget="",
                     timeline="", notes=""):
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError(
            "DEEPSEEK_API_KEY environment variable not set. "
            "Run: export DEEPSEEK_API_KEY='your-key'"
        )

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    from datetime import date
    today = date.today().isoformat()

    user_message = f"""Today's date: {today}

Analyze this customer inquiry:

Name: {name or 'N/A'}
Email: {email or 'N/A'}
Company: {company or 'N/A'}
Need: {need or 'N/A'}
Budget: {budget or 'N/A'}
Timeline: {timeline or 'N/A'}
Notes: {notes or 'N/A'}"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        max_tokens=1024,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    )

    raw = response.choices[0].message.content
    result = json.loads(raw)

    return {
        "intent_level": result.get("intent_level", "Medium"),
        "intent_reason": result.get("intent_reason", ""),
        "ai_analysis": result.get("ai_analysis", ""),
        "email_draft": result.get("email_draft", ""),
        "follow_up_date": result.get("follow_up_date", "")
    }
