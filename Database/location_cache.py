from Database.db import get_connection
from Utils.helper import get_geo_location

LOCATION_CACHE = {
    "districts": {},
    "states": {},
    "circles": {}
}

import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("Groq_APIKey"))


def extract_location(question: str):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
Extract ONLY the location from the user's question.

Return JSON.

Examples:

Question:
Show today's report for Connaught Place

Response:
{
  "location":"Connaught Place"
}

Question:
Weather at Mumbai Airport

Response:
{
  "location":"Mumbai Airport"
}

Question:
Show High Rain districts

Response:
{
  "location":null
}
"""
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return json.loads(
        response.choices[0].message.content
    )

    

def resolve_location_by_geometry(location: str):
    
    
    loc = get_geo_location(location)
    latitude = loc['lat']
    longitude = loc['lon']
    
    conn = get_connection()
    cur = conn.cursor()
    

    cur.execute("""
        SELECT
            district,
            state_ut,
            indus_circle,
            indus_circle_name
        FROM weatherdata.district_geometry
        WHERE ST_Intersects(
            geometry,
            ST_SetSRID(
                ST_Point(%s, %s),
                4326
            )
        )
        LIMIT 1
    """, (longitude, latitude))   # IMPORTANT: longitude first

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "district": row[0],
        "state": row[1],
        "circle": row[2],
        "circle_name": row[3]
    }