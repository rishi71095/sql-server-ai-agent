# SQL Server AI Agent

An AI\-powered SQL Server analytics assistant built using LangChain, OpenAI, SQLAlchemy, and Streamlit.

The agent converts natural language questions into SQL Server queries, executes them against a SQL Server database, and returns business\-friendly answers.

## Features

- Natural language to SQL
- SQL Server integration using SQLAlchemy and PyODBC
- Semantic model driven query generation
- Streamlit chat interface
- Persistent chat history
- Tool\-calling agent architecture
- Business\-oriented analytics responses

## Tech Stack

- Python
- LangChain
- OpenAI GPT\-4.1 Mini
- SQLAlchemy
- SQL Server
- PyODBC
- Streamlit
- Python Dotenv

## Project Structure

sql\-server\-ai\-agent/

│

├── docs/

│   └── semantic\_model.md

│

├── agent\_tools.py

├── app.py

├── streamlit\_app.py

├── requirements.txt

├── README.md

└── .gitignore

## Setup

### 1\. Clone the repository

git clone [https://github.com/rishi71095/sql\-server\-ai\-agent.git](https://github.com/rishi71095/sql-server-ai-agent.git)

cd sql\-server\-ai\-agent

### 2\. Create a virtual environment

python \-m venv venv

### 3\. Activate the virtual environment

Windows PowerShell

.\\venv\\Scripts\\Activate.ps1

### 4\. Install dependencies

pip install \-r requirements.txt

### 5\. Configure environment variables

Create a .env file:

OPENAI\_API\_KEY=your\_openai\_api\_key

SQL\_DRIVER=ODBC Driver 17 for SQL Server

SQL\_SERVER=localhost\\SQLEXPRESS

SQL\_DATABASE=your\_database

SQL\_TRUSTED\_CONNECTION=yes

SQL\_TRUST\_SERVER\_CERTIFICATE=yes

## Running the Console Agent

python app.py

## Running the Streamlit Application

python \-m streamlit run streamlit\_app.py

## Sample Questions

- Rank employees by total sales performance.
- Who are the top 5 employees by sales?
- Show customer purchasing trends in the latest 6 months.
- Which customers have consistently increased their purchases over time?
- What is the average order value?
- Which year experienced the largest increase in sales compared to the previous year?
- Show yearly sales trends.
- What are the highest value orders?

## Semantic Layer

The agent uses a semantic model stored in docs/semantic\_model.md to guide query generation and route business questions to the appropriate views.

Semantic views include:

- Sales.OrderValues
- Sales.EmpOrders
- Sales.CustOrders
- Sales.OrderTotalsByYear

## License

MIT

