import streamlit as st
import psycopg2
from openai import OpenAI

# Database Configuration
DB_HOST = "localhost"
DB_NAME = "newdatabase"
DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_PORT = "5432"

# Use the correct model name "gpt-4o-mini"
OPENAI_API_KEY = "your_openai_api_key_here" 
client = OpenAI(api_key=OPENAI_API_KEY)

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

def nl_to_sql(user_query):
    # This prompt tells the AI EXACTLY what you built in your terminal
    system_prompt = """
You are a PostgreSQL expert. Convert the user question into a SAFE, READ-ONLY SQL query.
The database schema is as follows:
- department1 (id, name)
- employe (id, name, department1_id, email, salary)
- orders1 (id, customer_name, employee_id, order_total, order_date)
- product1 (id, name, price)

JOIN rules: 
- Join employe.department1_id with department1.id
- Join orders1.employee_id with employe.id

Return ONLY the SQL query. Do not use Markdown blocks or extra text.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini", # Fixed model name
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()
    # Clean up any markdown the AI might accidentally include
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

def run_query(sql):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return columns, rows

# Streamlit UI
st.set_page_config(page_title="SQL AI Assistant", layout="wide")
st.title("Check data in  PostgreSQL")

user_query = st.text_input("Ask about your data:", placeholder="e.g., Show me the total salary for Engineering")

if st.button("Generate & Run"):
    if not user_query.strip():
        st.error("Please enter a question.")
    else:
        try:
            sql = nl_to_sql(user_query)
            
            # Security Check
            if not sql.lower().startswith("select"):
                st.error("Action blocked: Only SELECT queries are allowed.")
            else:
                st.subheader("Generated SQL:")
                st.code(sql, language="sql")

                columns, rows = run_query(sql)

                st.subheader("Results:")
                if rows:
                    # Convert to list of dicts for Streamlit dataframe
                    data = [dict(zip(columns, row)) for row in rows]
                    st.dataframe(data, use_container_width=True)
                else:
                    st.info("Query returned no results.")

        except Exception as e:
            st.error(f"Database Error: {e}")