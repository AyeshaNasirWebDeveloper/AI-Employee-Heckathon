# AI Digital Employee (Hackathon Project)

An AI-powered Email Assistant that acts like a Digital Employee for founders.

## 🚀 Problem

Founders are overwhelmed by emails and administrative tasks.  
Important emails get buried, responses are delayed, and productivity suffers.

## 💡 Solution

This project builds a local AI Digital Employee that:

- Fetches unread Gmail emails
- Summarizes emails using Claude AI
- Generates intelligent reply drafts
- Saves structured tasks in a markdown-based workflow
- Requires human approval before sending replies

Safe. Structured. Assistive.

---

## 🏗 Architecture

- Python
- Gmail API
- Claude API
- Local Markdown Vault Workflow

---

## 🔐 Security

Sensitive credentials are not stored in the repository.
Environment variables are used for API keys.

---

## 🛠 Setup Instructions

1. Clone repo
2. Create virtual environment
3. Install dependencies
4. Add `credentials.json` (Google OAuth)
5. Add `.env` with Claude API key
6. Run: `python gmail_test.py`

---

## 🎯 Hackathon Scope

This version focuses on:
- Email Fetch
- AI Summary
- Draft Generation
- Approval Workflow

Future versions may include:
- Cloud deployment
- ERP integration
- Multi-agent orchestration

---

## 👩‍💻 Author

Built for Hackathon 2026