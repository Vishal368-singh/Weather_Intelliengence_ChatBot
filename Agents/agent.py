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


def ask_agent(user_query, authorization):

    messages = [
        {
            "role": "system",
            "content": """
            You are a Weather GIS Assistant.

            Always use tools whenever weather,
            hazard, district, rainfall, cyclone,
            circle or KPI information is requested.

            Never make up weather information.
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
                payload=tool_args,
                headers={
                    "Authorization": authorization
                }
            )

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
        messages=messages
    )

    return final_response.choices[0].message.content