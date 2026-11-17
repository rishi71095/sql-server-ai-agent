import os
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv, find_dotenv
from langchain.tools import tool

# Load environment variables from .env
load_dotenv(find_dotenv(), override=True)


# Create a reusable SQL Server engine
def get_sql_server_engine():

    # Build the SQL Server connection string from environment variables
    conn_str = (
        f"DRIVER={{{os.getenv('SQL_DRIVER')}}};"
        f"SERVER={os.getenv('SQL_SERVER')};"
        f"DATABASE={os.getenv('SQL_DATABASE')};"
        f"Trusted_Connection={os.getenv('SQL_TRUSTED_CONNECTION')};"
        f"TrustServerCertificate={os.getenv('SQL_TRUST_SERVER_CERTIFICATE')};"
    )

    # DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=TSQLV6;Trusted_Connection=yes;TrustServerCertificate=yes;

    # Return a SQLAlchemy engine with connection health checks enabled
    return create_engine(
        f"mssql+pyodbc:///?odbc_connect={quote_plus(conn_str)}",
        pool_pre_ping=True
    )


# Initialize a shared database connection
engine = get_sql_server_engine()


@tool
def execute_query(query: str) -> str:
    """
    Execute a SQL query and return the results as text.
    """
    try:

        print("\nEXECUTE_QUERY TOOL CALLED")

        # uncomment to see SQL query being run by the agent in the output
        # print("\n==== SQL ====")
        # print(query)
        # print("================\n")

        df = pd.read_sql(query, engine)

        return df.to_string(index=False)

    except Exception as ex:

        return f"SQL_ERROR: {str(ex)}"
