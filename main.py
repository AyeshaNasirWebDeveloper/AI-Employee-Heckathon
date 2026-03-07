import os
import asyncio
import logging
import webbrowser
import urllib.parse
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

from watchers.gmail_watcher import check_for_new_email, create_gmail_draft
from watchers.linkedin_watcher import check_linkedin_activity
from skills.planning_skill import generate_plan_prompt
from skills.linkedin_skill import generate_linkedin_post_prompt
from mcp.action_server import post_to_linkedin
from utils.obsidian import save_to_obsidian

# ==============================
# ENV + LOGGING
# ==============================
load_dotenv()

gmail_account = os.getenv("GMAIL_ACCOUNT")

logging.basicConfig(
    filename="ai_employee.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("🚀 AI Employee System Booted")

# ==============================
# MODEL CONFIG
# ==============================
gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


# ==============================
# AGENT FUNCTIONS
# ==============================
async def create_plan(task):
    agent = Agent(
        name="Strategic Planner",
        instructions="Create a structured markdown execution plan.",
        model=model
    )

    prompt = generate_plan_prompt(task)
    result = await Runner.run(agent, prompt, run_config=config)
    return result.final_output

async def generate_email_reply(context):
    agent = Agent(
        name="Email Response Agent",
        instructions="Write a professional and concise email reply.",
        model=model
    )

    prompt = f"""
Reply professionally to this email:

{context}
"""

    result = await Runner.run(agent, prompt, run_config=config)
    return result.final_output

def open_gmail_draft(to, subject, body):

    subject_encoded = urllib.parse.quote(subject)
    body_encoded = urllib.parse.quote(body)

    url = f"https://mail.google.com/mail/?view=cm&fs=1&to={to}&su={subject_encoded}&body={body_encoded}"

    webbrowser.open(url)

async def generate_linkedin_post(context):
    agent = Agent(
        name="LinkedIn Growth Agent",
        instructions="Create persuasive LinkedIn sales posts.",
        model=model
    )

    prompt = generate_linkedin_post_prompt(context)
    result = await Runner.run(agent, prompt, run_config=config)
    return result.final_output


# ==============================
# MAIN LOOP
# ==============================
async def main():
    print("🤖 AI Employee System Started...\n")

    while True:
        try:
            # ================= Gmail =================
            print("🔎 Checking Gmail...")
            email_data = check_for_new_email()

            if email_data:
                logging.info("New Gmail detected.")

                task_text = f"""
Subject: {email_data['subject']}

Body:
{email_data['body']}
"""

                plan = await create_plan(task_text)

                print("\n--- GENERATED PLAN ---\n")
                print(plan)

                approval = input("\nApprove this plan? (yes/no): ").strip().lower()

                if approval == "yes":
                    save_to_obsidian(plan, folder="approvals", title="Approved_Plan")
                    logging.info("Plan approved.")

                    reply = await generate_email_reply(task_text)

                    print("\n📧 Generated Email Reply:\n")
                    print(reply)

                    send_confirm = input("Send this reply? (yes/no): ").strip().lower()

                    if send_confirm == "yes":
                        create_gmail_draft(
                            email_data["service"],
                            email_data["sender"],
                            email_data["subject"],
                            reply,
                            email_data["thread_id"]
                        )
                        logging.info("Email reply sent.")

                    if send_confirm.lower() == "yes":
                        open_gmail_draft(
                            gmail_account,
                            "Regarding your Google Security Alert",
                            reply
                        )

                else:
                    save_to_obsidian(plan, folder="plans", title="Rejected_Plan")
                    logging.info("Plan rejected.")

            # ================= LinkedIn =================
            print("\n🔎 Checking LinkedIn...")
            linkedin_context = check_linkedin_activity()

            if linkedin_context:
                logging.info("LinkedIn activity detected.")

                post = await generate_linkedin_post(linkedin_context)

                print("\n📢 Generated LinkedIn Post:\n")
                print(post)

                approval = input("Approve LinkedIn post? (yes/no): ").strip().lower()

                if approval == "yes":
                    print("LinkedIn post ready to publish.")
                    save_to_obsidian(post, folder="approvals", title="LinkedIn_Post")
                    logging.info("LinkedIn post saved for approval.")

                    # Call the function to post to LinkedIn
                    post_to_linkedin(post)
                    print("LinkedIn post ready to publish.")
                    webbrowser.open("https://www.linkedin.com/feed/")
                    logging.info("LinkedIn post published.")

            print("\n⏳ Waiting 60 seconds...\n")
            await asyncio.sleep(60)

        except Exception as e:
            logging.error(f"System error: {e}")
            print(f"⚠️ Error: {e}")
            await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(main())