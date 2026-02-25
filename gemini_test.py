import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
import asyncio

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.5-flash",
    openai_client = external_client,
)

config = RunConfig(
    model = model,
    model_provider = external_client,
    tracing_disabled = True
)

async def run_agent():
    agent = Agent(
    name="AI Project Manager",
    instructions=(
        "You are a professional AI project manager.\n"
        "Consider previous conversation context before answering.\n"
        "Tasks:\n"
        "1. Analyze client email.\n"
        "2. Detect urgency level (Low / Medium / High).\n"
        "3. Summarize client request.\n"
        "4. Draft a professional reply.\n"
        "Keep response structured.\n"
        """Return output in this JSON format:
{
  "urgency": "",
  "summary": "",
  "reply": ""
}"""
    ),
        model=model
    )

#     conversation = [
#     {
#         "role": "user",
#         "content": "Client: We need the project proposal by Friday."
#     },
#     {
#         "role": "assistant",
#         "content": "Acknowledged. We are preparing the timeline."
#     },
#     {
#         "role": "user",
#         "content": "Also confirm updated budget and final delivery date."
#     }
# ]

    with open("client_email.txt", "r") as f:
        email_content = f.read()

    result = await Runner.run(
        agent,
        # user_input,
        # conversation,
        f"Client Email:\n{email_content}",
        run_config=config
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(run_agent())
    