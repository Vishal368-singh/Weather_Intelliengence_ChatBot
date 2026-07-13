from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

from Utils.weather_api import get_live_weather
from Utils.DailyReport import handle_daily_report


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    parameters: Dict[str, Any]


TOOL_SPECS = {

    "live_weather": ToolSpec(
        name="live_weather",
        description=(
            "Fetch current weather, hourly forecast "
            "air quality, astronomy and alerts."
        ),
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City, district, state or latitude,longitude"
                }
            },
            "required": ["location"],
            "additionalProperties": False,
        },
    ),

    # Keep these for Phase 2
      # ----------------------------
    # DAILY FORECAST REPORT
    # ----------------------------
    "daily_report": ToolSpec(
        name="daily_report",
        description=(
            "Generate SQL for district-wise 7-day daily forecast reports."
        ),
        parameters={
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "Natural language question about daily forecast reports."
                }
            },
            "required": ["question"],
            "additionalProperties": False,
        },
    ),
    
}


def list_tool_specs(names=None):

    if names is None:
        return list(TOOL_SPECS.values())

    return [TOOL_SPECS[n] for n in names if n in TOOL_SPECS]


def build_openai_tools(names=None):

    return [
        {
            "type": "function",
            "function": {
                "name": spec.name,
                "description": spec.description,
                "parameters": spec.parameters,
            },
        }
        for spec in list_tool_specs(names)
    ]


# ----------------------------
# Tool Dispatcher
# ----------------------------
def call_tool(tool_name: str, payload: Dict[str, Any]):

    if tool_name == "live_weather":
        return get_live_weather(
            payload["location"]
        )

    elif tool_name == "daily_report":
        return handle_daily_report(payload["question"])

    raise ValueError(f"Unknown tool: {tool_name}")


__all__ = [
    "ToolSpec",
    "TOOL_SPECS",
    "list_tool_specs",
    "build_openai_tools",
    "call_tool",
]