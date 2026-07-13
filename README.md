# 🌦️ Weather GIS AI Chatbot

An AI-powered Weather GIS Chatbot built using **FastAPI**, **Groq LLM**, **PostgreSQL/PostGIS**, and **Weather APIs** that allows users to ask weather-related questions in natural language.

The chatbot can answer:

- 🌤️ Live Weather
- 📅 Daily Forecast Reports
- ⚠️ Hazard Reports
- 📊 Weather Deviation Reports
- 📈 KPI Reports
- 📍 Location-based Weather Queries

using **Natural Language → SQL** generation and live weather APIs.

---

# Features

## 🌤️ Live Weather

Fetches live weather using:

- WeatherAPI (Primary)
- Visual Crossing (Fallback)

Supports:

- Current Weather
- Hourly Forecast
- 7-Day Forecast
- Air Quality
- Astronomy
- Weather Alerts

Example:

> Weather in Delhi

---

## 🤖 AI Powered Chat

Users can ask questions naturally.

Examples:

- Show today's weather report for Delhi
- Rainfall forecast for Ballia
- Hazard report for Jaipur
- Which districts have Extreme temperature?
- Show fog alerts for UP East
- Weather at Connaught Place

---

## 🗺️ Smart Location Resolution

The chatbot automatically understands locations.

Supports:

- District
- City
- State
- Village
- Landmark
- Latitude / Longitude

Example

```
Weather near India Gate
```

↓

```
India Gate
```

↓

```
Latitude & Longitude
```

↓

```
PostGIS Geometry Match
```

↓

```
District : New Delhi
Circle : DEL
```

---

## 🧠 Text-to-SQL

The chatbot converts natural language into PostgreSQL queries.

Example

```
Show today's weather report for Ballia
```

↓

```sql
SELECT *
FROM weatherdata.district_wise_7dayfc_severity
WHERE district='Ballia'
AND days='Day1';
```

Only **SELECT** queries are generated.

---

## 🗃️ Supported Reports

- Daily Forecast Report
- Deviation Report
- Hazard Report
- KPI Report
- Historical Weather Reports

---

# Tech Stack

## Backend

- Python
- FastAPI
- Groq API
- PostgreSQL
- PostGIS
- Psycopg2

## AI

- Llama 3.3 70B
- Prompt Engineering
- Tool Calling
- Text-to-SQL

## Weather Providers

- WeatherAPI
- Visual Crossing

---

# Project Structure

```
weather_chatbot/
│
├── Agents/
│   └── agent.py
│
├── Database/
│   ├── db.py
│   └── executor.py
│
├── LLM_Interaction/
│   ├── tools.py
│   ├── sql_generator.py
│   └── prompts.py
│
├── Reports/
│   ├── daily_report.py
│   ├── deviation_report.py
│   ├── hazard_report.py
│   └── kpi_report.py
│
├── Location/
│   ├── location_cache.py
│   ├── extractor.py
│   ├── resolver.py
│   └── geocoder.py
│
├── Schemas/
│   ├── daily_schema.py
│   ├── deviation_schema.py
│   ├── hazard_schema.py
│   └── kpi_schema.py
│
├── Utils/
│   └── weather_api.py
│
├── app.py
│
└── requirements.txt
```

---

# Architecture

```
                User Query
                     │
                     ▼
              Intent Detection
                     │
                     ▼
           Location Extraction
                     │
                     ▼
             Location Resolver
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
   Live Weather             Report Request
         │                       │
         ▼                       ▼
   WeatherAPI             Text-to-SQL
 Visual Crossing               │
         │                     ▼
         ▼              PostgreSQL/PostGIS
                │               │
                └───────┬───────┘
                        ▼
                 AI Response Generator
                        │
                        ▼
                     JSON Response
```

---

# API Response

```json
{
  "success": true,
  "type": "daily_report",
  "message": "Daily weather report for Ballia.",
  "question": "Today's forecast for Ballia",
  "sql": "SELECT ...",
  "data": [
    {
      "district": "Ballia",
      "temp_max": 41.8,
      "rain_percent": 57
    }
  ]
}
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/<username>/<repository>.git

cd weather_chatbot
```

Create Virtual Environment

```bash
python -m venv py-env
```

Activate

Windows

```bash
py-env\Scripts\activate
```

Linux

```bash
source py-env/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env`

```env
Groq_APIKey=

weatherAPIKey=

visualCrossAPIKey=

maptilerAPIKey=

DB_HOST=

DB_NAME=

DB_USER=

DB_PASSWORD=

DB_PORT=5432
```

---

# Run

```bash
uvicorn app:app --reload
```

or

```bash
python app.py
```

---

# Sample Questions

```
Current weather in Delhi

Today's forecast for Ballia

Show Heavy Rain districts

Hazard report for Jaipur

Weather at Connaught Place

Show temperature deviation report

Which districts have Extreme Heat?

Show weather alerts for Mumbai
```

---

# Future Enhancements

- Multi-turn conversation memory
- Semantic search for weather documentation
- Vector database integration
- Multi-language support
- Streaming responses
- Charts and maps
- Report export (PDF / Excel)
- Voice assistant
- User authentication and roles

---

# License

This project is licensed under the MIT License.

---

# Author

**Vishal Singh**

Software Developer | GIS | AI | Weather Intelligence | FastAPI | PostgreSQL | OpenLayers
