from langchain.tools import tool
from datetime import datetime

# in-memory email
SENT_MAILS = []

@tool
def send_email(
    details: str
) -> str:
    """Sends an email.
    Expected input format:
    "to: person@example.com | subject: Hello | body: How are you?"

    This is a simulation (no actual email sending).
    """
    SENT_MAILS.append({
        'details': details,
        'sent_at': datetime.now().isoformat()
    })

    return f'Email sent: {details}'

@tool
def list_sent_emails(_: str = ""):
    """Returns all emails sent so far."""
    if not SENT_MAILS:
        return "No emails sent."

    return "\n".join([
        f"- {e['details']} (sent {e['sent_at']})"
        for e in SENT_MAILS
    ])