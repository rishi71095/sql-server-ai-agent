import json
import os
import time
import uuid

import streamlit as st

from pathlib import Path
from dotenv import load_dotenv, find_dotenv

from langchain.agents import create_agent

from agent_tools import execute_query


# ----------------------------------
# Environment
# ----------------------------------

load_dotenv(find_dotenv(), override=True)


# ----------------------------------
# Files
# ----------------------------------

HERE = os.path.dirname(
    os.path.abspath(__file__)
)

STORE = os.path.join(
    HERE,
    "chat_history.json"
)


# ----------------------------------
# Streamlit Config
# ----------------------------------

st.set_page_config(
    page_title="SQL Server AI Agent",
    page_icon="🗄️",
    layout="wide"
)


# ----------------------------------
# Semantic Context
# ----------------------------------

SEMANTICS = Path(
    "docs/semantic_model.md"
).read_text(
    encoding="utf-8"
)


# ----------------------------------
# System Prompt
# ----------------------------------

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


# ----------------------------------
# Chat Storage
# ----------------------------------

def load_store():

    try:

        with open(
            STORE,
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        return data["chats"], data["order"]

    except Exception:

        return {}, []


def save_store():

    with open(
        STORE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "chats": st.session_state.chats,
                "order": st.session_state.order
            },
            f,
            ensure_ascii=False
        )


# ----------------------------------
# Session State
# ----------------------------------

if "chats" not in st.session_state:

    (
        st.session_state.chats,
        st.session_state.order
    ) = load_store()

    st.session_state.current = None


# ----------------------------------
# Agent
# ----------------------------------

@st.cache_resource(show_spinner=False)
def build_agent():

    return create_agent(
        model="openai:gpt-4.1-mini",
        tools=[execute_query],
        system_prompt=SYSTEM_PROMPT
    )


# ----------------------------------
# Agent Call
# ----------------------------------

def ask_agent(question, turns):

    messages = []

    for turn in turns:

        messages.append(
            {
                "role": "user",
                "content": turn["question"]
            }
        )

        messages.append(
            {
                "role": "assistant",
                "content": turn["answer"]
            }
        )

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    result = build_agent().invoke(
        {
            "messages": messages
        }
    )

    return result["messages"][-1].content


# ----------------------------------
# Sidebar
# ----------------------------------

with st.sidebar:

    st.title("🗄️ SQL Agent")

    st.caption(
        f"""
        Database: {os.getenv('SQL_DATABASE')}

        Model: GPT-4.1-mini
        """
    )

    if st.button(
        "＋ New Chat",
        use_container_width=True,
        type="primary"
    ):

        st.session_state.current = None

        st.rerun()

    st.divider()

    st.subheader("Chat History")

    if not st.session_state.order:

        st.caption(
            "Your chats will appear here."
        )

    for cid in st.session_state.order:

        chat = st.session_state.chats[cid]

        title = chat["title"]

        active = (
            cid == st.session_state.current
        )

        if st.button(
            title,
            key=f"chat_{cid}",
            help=title,
            use_container_width=True,
            type="primary" if active else "secondary"
        ):

            st.session_state.current = cid

            st.rerun()

    if st.session_state.current:

        st.divider()

        if st.button(
            "🗑️ Delete Current Chat",
            use_container_width=True
        ):

            cid = st.session_state.current

            st.session_state.chats.pop(
                cid,
                None
            )

            if cid in st.session_state.order:

                st.session_state.order.remove(
                    cid
                )

            st.session_state.current = None

            save_store()

            st.rerun()


# ----------------------------------
# Main
# ----------------------------------

st.title("SQL Server AI Agent")

st.caption(
    "Semantic-model driven SQL Server assistant powered by LangChain and OpenAI."
)

with st.expander("Example Questions"):

    st.markdown(
        """
        - How many tables do we have?
        - Who are the top 5 employees by sales?
        - Show total purchases by month for the latest 6 months.
        - Which customers have consistently increased their purchases over time?
        - What is the average order value?
        - Which year experienced the largest increase in sales?
        - Show yearly sales trends.
        - Who are the top 10 customers by purchase volume?
        - What are the highest value orders?
        """
    )


chat = st.session_state.chats.get(
    st.session_state.current
)

turns = chat["turns"] if chat else []


for turn in turns:

    with st.chat_message("user"):

        st.write(turn["question"])

    with st.chat_message("assistant"):

        st.write(turn["answer"])

        st.caption(
            f"{turn['secs']:.1f}s"
        )


question = st.chat_input(
    "Ask a question about your database..."
)


if question:

    with st.chat_message("user"):

        st.write(question)

    with st.chat_message("assistant"):

        try:

            start = time.time()

            with st.spinner(
                "Analyzing database..."
            ):

                answer = ask_agent(
                    question,
                    turns
                )

            st.write(answer)

            secs = (
                time.time()
                - start
            )

        except Exception as ex:

            st.error(
                f"Agent Error: {ex}"
            )

            st.stop()

    turn = {
        "question": question,
        "answer": answer,
        "secs": secs
    }

    if chat is None:

        cid = uuid.uuid4().hex[:8]

        st.session_state.chats[cid] = {
            "title": question,
            "turns": []
        }

        st.session_state.order.insert(
            0,
            cid
        )

        st.session_state.current = cid

        chat = st.session_state.chats[cid]

    chat["turns"].append(turn)

    save_store()

    st.rerun()
