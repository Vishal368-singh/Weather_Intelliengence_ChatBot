from Database.executor import execute_sql
from Database.location_cache import extract_location, resolve_location_by_geometry
from LLM_Interaction.sql_generator import generate_sql
from Schemas.dailyReport import DAILY_SCHEMA


def handle_daily_report(question: str):
    location = extract_location(question)
    resolved_location = resolve_location_by_geometry(location) if location else None

    sql = generate_daily_report_sql(question, resolved_location)

    result = execute_sql(sql)

    return {
        "question": question,
        "sql": sql,
        "rows": result
    }
    



def generate_daily_report_sql(question: str, location: dict = None):
    
    location_context = ""

    if location:
        location_context = f"""
            Resolved Location (Already identified by the system)

            District      : {location.get('district')}
            State         : {location.get('state')}
            Indus Circle  : {location.get('circle')}

            Rules:
            - Do NOT identify another location.
            - If the report table contains 'district', use the resolved district.
            - If the report table contains 'indus_circle', use the resolved Indus Circle.
            """

    prompt = f"""
        You are a PostgreSQL expert.

        {DAILY_SCHEMA}
        {location_context}

        Question:
        {question}

        Generate ONLY PostgreSQL SELECT query.
        Instructions:
        1. Generate ONLY PostgreSQL SELECT query.
        2. Return ONLY SQL.
        3. Do NOT use markdown.
        4. Do NOT explain anything.
        5. Use the resolved location if provided.
        6. If no location is provided, generate the query without location filters.
        """

    return generate_sql(prompt)