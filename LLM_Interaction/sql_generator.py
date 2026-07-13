import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("Groq_APIKey")
)

MODEL = "llama-3.3-70b-versatile"
# MODEL = "qwen/qwen3-32b"


def generate_sql(prompt: str) -> str:

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You are an expert PostgreSQL SQL Generator.

Rules:

1. Generate ONLY PostgreSQL SQL.
2. Output ONLY the SQL query.
3. Do not use markdown.
4. Do not explain anything.
5. Never generate INSERT.
6. Never generate UPDATE.
7. Never generate DELETE.
8. Never generate DROP.
9. Never generate ALTER.
10. Only SELECT queries are allowed.
11. Use only the tables and columns provided.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    # Remove markdown if the model adds it
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql