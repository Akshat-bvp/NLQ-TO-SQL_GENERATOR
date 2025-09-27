from langchain_openai import ChatOpenAI
import sqlite3
import pandas as pd


local_llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="BASE_URL",
    api_key="API_IKEY"
)


conn = sqlite3.connect("data.db")

def get_sql_query(user_prompt: str) -> str:
    prompt = f"""
You are a SQL generator. Convert this into a SQL query:
"{user_prompt}"

Only return raw SQL. No explanation, no markdown.
"""
    return local_llm.invoke(prompt).content.strip()


def get_sql_and_explanation(user_prompt: str) -> tuple:

    sql_query = get_sql_query(user_prompt)

    explanation_prompt = f"""Explain what this SQL query does:
    "{sql_query}"
    """

    explanation = local_llm.invoke(explanation_prompt).content.strip()

    return sql_query, explanation


def run_sql_query(query: str):
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        return f"SQL Execution Error: {e}"


def format_df_markdown(df: pd.DataFrame) -> str:
    insight_prompt = f"summarise the data: \n {df.head().to_markdown(index=True)}"
    return local_llm.invoke(insight_prompt).content.strip()




     
