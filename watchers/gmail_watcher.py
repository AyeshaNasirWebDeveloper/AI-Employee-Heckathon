import os
import json
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import webbrowser

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose"
]

LAST_EMAIL_FILE = "last_processed_email.json"


# ==============================
# AUTHENTICATION
# ==============================
def authenticate_gmail():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


# ==============================
# MEMORY HANDLING
# ==============================
def load_last_processed():
    if os.path.exists(LAST_EMAIL_FILE):
        with open(LAST_EMAIL_FILE, "r") as f:
            return json.load(f)
    return None


def save_last_processed(email_id):
    with open(LAST_EMAIL_FILE, "w") as f:
        json.dump(email_id, f)


# ==============================
# CHECK FOR NEW EMAIL
# ==============================
def check_for_new_email():
    service = authenticate_gmail()

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        q="is:unread",
        maxResults=1
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        return None

    msg_id = messages[0]["id"]

    # Prevent duplicate processing
    last_processed = load_last_processed()
    if msg_id == last_processed:
        return None

    save_last_processed(msg_id)

    message = service.users().messages().get(
        userId="me",
        id=msg_id,
        format="full"
    ).execute()

    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    subject = ""
    sender = ""
    thread_id = message.get("threadId")

    for header in headers:
        if header["name"] == "Subject":
            subject = header["value"]
        if header["name"] == "From":
            sender = header["value"]

    body = ""

    def extract_body(parts):
        for part in parts:
            mime_type = part.get("mimeType")
            data = part.get("body", {}).get("data")

            if mime_type == "text/plain" and data:
                decoded = base64.urlsafe_b64decode(data)
                return decoded.decode(errors="ignore")

            if part.get("parts"):
                return extract_body(part.get("parts"))
        return ""

    if payload.get("parts"):
        body = extract_body(payload.get("parts"))
    else:
        data = payload.get("body", {}).get("data")
        if data:
            decoded = base64.urlsafe_b64decode(data)
            body = decoded.decode(errors="ignore")

    return {
        "subject": subject,
        "sender": sender,
        "body": body,
        "thread_id": thread_id,
        "service": service
    }


# ==============================
# SEND REPLY
# ==============================
def create_gmail_draft(service, to_email, subject, message_text, thread_id):
    message = MIMEText(message_text)
    message["to"] = to_email
    message["subject"] = "Re: " + subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    draft_body = {
        "message": {
            "raw": raw_message,
            "threadId": thread_id
        }
    }

    service.users().messages().send(
        userId="me",
        body={"raw": raw_message}
    ).execute()

    print("✅ Email Sent successfully.")

    # Open Gmail drafts page
    webbrowser.open("https://mail.google.com/mail/u/0/#drafts")