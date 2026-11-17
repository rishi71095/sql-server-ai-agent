from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from langchain.agents import create_agent
from agent_tools import execute_query

# -----------------------------------
# Load environment variables
# -----------------------------------

load_dotenv(find_dotenv(), override=True)

# -----------------------------------
# Load semantic context
# -----------------------------------

SEMANTICS = Path(
    "docs/semantic_model.md"
).read_text(
    encoding="utf-8"
)

# -----------------------------------
# System prompt
# -----------------------------------

SYSTEM_PROMPT = f"""
You are an expert SQL Server analytics assistant.

Database semantic model:

{SEMANTICS}

Rules:

1. Use only documented tables and views.
2. Infer joins using documented relationships.
3. Prefer semantic views when applicable.
4. Never invent tables or columns.
5. Generate SQL Server compatible T-SQL.
6. When data is required, ALWAYS use execute_query.
7. Only answer questions asked and do not offer follow-up questions.
"""

# -----------------------------------
# Create agent
# -----------------------------------

agent = create_agent(
    model="openai:gpt-4.1-mini",
    tools=[execute_query],
    system_prompt=SYSTEM_PROMPT
)

print("SQL Agent Ready")
print("Type 'exit' to quit.")

# -----------------------------------
# Chat loop
# -----------------------------------

while True:

    question = input("\nQuestion: ").strip()

    if question.lower() == "exit":
        break

    try:

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            }
        )

        print("\nAnswer:\n")

        print(
            response["messages"][-1].content
        )

    except Exception as ex:

        print(f"\nError: {ex}")
