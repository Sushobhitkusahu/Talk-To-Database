import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration from environment variables
GOOGLE_API_KEY = "Your API Key Here"
db_user = "root"
db_password = "your db password"
db_host = "localhost:3306"
db_name = "atliq_tshirts"

# Create SQLAlchemy engine
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

# Initialize Google Generative AI model
llm = GoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=GOOGLE_API_KEY)

# Custom prompt template
prompt_template = """
Given an input question, create a syntactically correct MySQL query to run. Do not include any markdown formatting or backticks in your response. Only provide the raw SQL query.

Here is the question:
{input}
"""

class SQLOutputParser(BaseOutputParser):
    """Custom output parser for SQL queries."""
    def parse(self, text):
        """Parse the output text."""
        return text

# Create SQL query chain
sql_chain = create_sql_query_chain(llm, db)

def clean_sql_query(query):
    """Clean the SQL query by removing markdown formatting and unnecessary characters."""
    cleaned_query = query.strip()
    if cleaned_query.startswith('```sql'):
        cleaned_query = cleaned_query[6:]
    if cleaned_query.endswith('```'):
        cleaned_query = cleaned_query[:-3]
    return cleaned_query.strip()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_sql_query(question):
    """Generate an SQL query based on the given question."""
    return sql_chain.invoke({"question": question})

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_response(query, result, question):
    """Generate a natural language response based on the SQL query and its result."""
    response_prompt = PromptTemplate.from_template(
        "Based on the SQL query: {query}\n"
        "And its result: {result}\n"
        "Please provide a natural language answer to the question: {question}"
    )
    response_chain = response_prompt | llm | SQLOutputParser()
    return response_chain.invoke({"query": query, "result": result, "question": question})

def get_response(question):
    """Process the user's question and return a response."""
    try:
        sql_query = generate_sql_query(question)
        cleaned_sql_query = clean_sql_query(sql_query)
        result = db.run(cleaned_sql_query)
        response = generate_response(cleaned_sql_query, result, question)
        return response
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    st.title("🤖 AtliQ-Tees ")
    st.subheader("SQL Query Assistant with AI-powered insights.")


    question = st.text_input("Enter your question:")
    if st.button("Ask"):
        if question:
            with st.spinner("Generating response..."):
                response = get_response(question)
            st.write("Response:", response)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
