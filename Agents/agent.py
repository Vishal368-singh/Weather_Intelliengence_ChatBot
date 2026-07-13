import os
import json
from dotenv import load_dotenv
from groq import Groq

from LLM_Interaction.tools import (
    build_openai_tools,
    call_tool
)

load_dotenv()

client = Groq(
    api_key=os.getenv("Groq_APIKey")
)

tools = build_openai_tools()


def ask_agent(user_query):

    messages = [
        {
            "role": "system",
            "content": """
            You are a Weather GIS Assistant.
            
            Format:

            {
                "success": true,
                "message": "Result message to the user",
                "Question": user_query,
                "SQL Query" : "If the user query requires a SQL query, provide it here. If not, leave it empty.",
                "data": []
            }


           
            Rules:

            1. For current weather, forecast, temperature, humidity, rainfall,
            wind, AQI, astronomy or weather alerts,
            ALWAYS call the live_weather tool.

            2. Never answer weather questions from memory.

            3. Use only the tool response to answer.

            4. If the tool returns an error,
            politely inform the user that live weather data is unavailable.

            5. Do not expose raw JSON.
            """
        },
        {
            "role": "user",
            "content": user_query
        }
    ]

    # First LLM Call
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    assistant_message = response.choices[0].message

    # If no tool was called
    if not assistant_message.tool_calls:
        return assistant_message.content

    # Add assistant message
    messages.append(assistant_message)

    # Execute all tool calls
    for tool_call in assistant_message.tool_calls:

        tool_name = tool_call.function.name

        tool_args = json.loads(
            tool_call.function.arguments
        )

        try:
            tool_result = call_tool(
                tool_name=tool_name,
                payload=tool_args
            )
            
            # Handle authentication failure
            if (
                isinstance(tool_result, dict)
                and tool_result.get("error") == "UNAUTHORIZED"
            ):
                return "Your session has expired or been revoked. Please log in again."

        except Exception as e:
            tool_result = {
                "error": str(e)
            }

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result)
        })

    # Second LLM Call
    final_response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    response_format={"type": "json_object"},
    temperature=0
    )

    return json.loads(final_response.choices[0].message.content)