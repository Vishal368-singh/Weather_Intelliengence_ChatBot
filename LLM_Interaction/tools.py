
# Core Functions:
# call_tool() – Call tools by name
# call_endpoint() – Call any endpoint directly
# build_openai_tools() – Generate OpenAI function definitions
# list_tool_specs() – List available tools


from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import requests


DEFAULT_BASE_URL = os.environ.get(
    "WEATHER_CHATBOT_BASE_URL",
    os.environ.get("WEATHER_CHATBOT_API_URL", "http://127.0.0.1:6633"),
)


@dataclass(frozen=True)
class ToolSpec:
    name: str
    path: str
    method: str
    description: str
    parameters: Dict[str, Any]
    auth_required: bool = True

# Tools used in Weather API's and Used For ChatBot Interaction
TOOL_SPECS: Dict[str, ToolSpec] = {
    
    "weather_lookup": ToolSpec(
        name="weather_lookup",
        path="/get_weather",
        method="POST",
        description="Fetch current weather data for a query string or place.",
        parameters={
            "type": "object",
            "properties": {"q": {"type": "string", "description": "Search query or location"}},
            "required": ["q"],
            "additionalProperties": False,
        },
    ),
    "current_weather": ToolSpec(
        name="current_weather",
        path="/get-current-weather",
        method="POST",
        description="Fetch current weather data for the selected date.",
        parameters={
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "properties": {
                        "selectedDate": {"type": "string", "description": "Selected date"}
                    },
                    "required": ["selectedDate"],
                    "additionalProperties": False,
                }
            },
            "required": ["params"],
            "additionalProperties": False,
        },
    ),
    "circle_weather_min_max": ToolSpec(
        name="circle_weather_min_max",
        path="/get_circle_weather_min_max",
        method="POST",
        description="Fetch min/max weather data for a circle.",
        parameters={
            "type": "object",
            "properties": {"circle": {"type": "string", "description": "Circle name"}},
            "required": ["circle"],
            "additionalProperties": False,
        },
    ),
    "earthquake_data": ToolSpec(
        name="earthquake_data",
        path="/get-earthquake",
        method="POST",
        description="Fetch earthquake data.",
        parameters={"type": "object", "properties": {}, "additionalProperties": False},
    ),
    "deviation_hazards_list": ToolSpec(
        name="deviation_hazards_list",
        path="/get-deviation-hazards-list",
        method="POST",
        description="Fetch deviation (severity) hazards list for a circle.",
        parameters={
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "properties": {"circle": {"type": "string"}},
                    "required": ["circle"],
                }
            },
            "required": ["params"],
            "additionalProperties": False,
        },
    ),
    "deviation_severity_list": ToolSpec(
        name="deviation_severity_list",
        path="/get-deviation-severity-list",
        method="POST",
        description="Fetch severity list for a hazard type and circle.",
        parameters={
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "properties": {
                        "hazardType": {"type": "string"},
                        "circle": {"type": "string"},
                    },
                    "required": ["hazardType", "circle"],
                }
            },
            "required": ["params"],
            "additionalProperties": False,
        },
    ),
    "today_deviation": ToolSpec(
        name="today_deviation",
        path="/get-today-deviation",
        method="POST",
        description="Fetch today's deviation data for hazard and severity.",
        parameters={
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "properties": {
                        "hazardType": {"type": "string"},
                        "severityType": {"type": "string"},
                        "circle": {"type": "string"},
                    },
                    "required": ["hazardType", "severityType", "circle"],
                }
            },
            "required": ["params"],
            "additionalProperties": False,
        },
    ),
    "today_disasters": ToolSpec(
        name="today_disasters",
        path="/get-nsystem-today-disasters",
        method="POST",
        description="Fetch today's disasters for hazard type and severity.",
        parameters={
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "properties": {
                        "hazardType": {"type": "string"},
                        "severityType": {"type": "string"},
                        "circle": {"type": "string"},
                    },
                    "required": ["hazardType", "severityType", "circle"],
                }
            },
            "required": ["params"],
            "additionalProperties": False,
        },
    ),
    "hazards_list": ToolSpec(
        name="hazards_list",
        path="/get-nsystem-hazards-list",
        method="POST",
        description="Fetch hazards list for a circle.",
        parameters={
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "properties": {"circle": {"type": "string"}},
                    "required": ["circle"],
                }
            },
            "required": ["params"],
            "additionalProperties": False,
        },
    ),
    "severity_list": ToolSpec(
        name="severity_list",
        path="/get-nsystem-severity-list",
        method="POST",
        description="Fetch severity list for a hazard and circle.",
        parameters={
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "properties": {
                        "hazardType": {"type": "string"},
                        "circle": {"type": "string"},
                    },
                    "required": ["hazardType", "circle"],
                }
            },
            "required": ["params"],
            "additionalProperties": False,
        },
    ),
    "circle_list": ToolSpec(
        name="circle_list",
        path="/get_circle_list",
        method="POST",
        description="List circles for the requested circle filter.",
        parameters={
            "type": "object",
            "properties": {"circle": {"type": "string", "description": "Circle name or All Circle"}},
            "required": ["circle"],
            "additionalProperties": False,
        },
    ),
    "district_list": ToolSpec(
        name="district_list",
        path="/get_district_list",
        method="POST",
        description="List districts for a circle.",
        parameters={
            "type": "object",
            "properties": {"circle": {"type": "string", "description": "Circle name or All Circle"}},
            "required": ["circle"],
            "additionalProperties": False,
        },
    ),
    "inserted_hazard_circle_list": ToolSpec(
        name="inserted_hazard_circle_list",
        path="/inserted_hazard_circle_list",
        method="POST",
        description="Fetch circles where a hazard was inserted today.",
        parameters={
            "type": "object",
            "properties": {"hazard": {"type": "string", "description": "Hazard name"}},
            "required": ["hazard"],
            "additionalProperties": False,
        },
    ),
    "hazards_forecast": ToolSpec(
        name="hazards_forecast",
        path="/get-hazards",
        method="POST",
        description="Fetch today's hazard forecast records for a hazard type.",
        parameters={
            "type": "object",
            "properties": {"hazard": {"type": "string", "description": "Hazard name"}},
            "required": ["hazard"],
            "additionalProperties": False,
        },
    ),
    "district_wise_hazards_forecast": ToolSpec(
        name="district_wise_hazards_forecast",
        path="/get-district-wise-hazards",
        method="POST",
        description="Fetch district-wise hazard forecasts for a hazard and circle.",
        parameters={
            "type": "object",
            "properties": {
                "hazardType": {"type": "string", "description": "Hazard name"},
                "circle": {"type": "string", "description": "Circle name"},
            },
            "required": ["hazardType", "circle"],
            "additionalProperties": False,
        },
    ),
    "hazard_affected_districts": ToolSpec(
        name="hazard_affected_districts",
        path="/get-hazard-affected-district",
        method="POST",
        description="Fetch hazard impacted districts for a circle.",
        parameters={
            "type": "object",
            "properties": {"circle": {"type": "string", "description": "Circle name"}},
            "required": ["circle"],
            "additionalProperties": False,
        },
    ),
   "district_rainfall_obs": ToolSpec(
        name="district_rainfall_obs",
        path="/get_district_rainfall_obs",
        method="POST",
        description="Fetch district rainfall observation for a latitude and longitude.",
        parameters={
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
                "selectedDay": {"type": "string", "description": "TODAY or TOMORROW"},
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False,
        },
    ),
    "accumulated_rainfall": ToolSpec(
        name="accumulated_rainfall",
        path="/fetch_accumulated_rainfall",
        method="POST",
        description="Fetch accumulated rainfall data for a circle.",
        parameters={
            "type": "object",
            "properties": {"circle": {"type": "string"}},
            "required": ["circle"],
            "additionalProperties": False,
        },
    ),
    "kpi_history": ToolSpec(
        name="kpi_history",
        path="/get-kpi-history",
        method="POST",
        description="Fetch KPI modification history.",
        parameters={"type": "object", "properties": {}, "additionalProperties": False},
    ),
   "circle_report": ToolSpec(
        name="circle_report",
        path="/fetch_circle_report",
        method="POST",
        description="Fetch circle weather report data.",
        parameters={
            "type": "object",
            "properties": {"circle": {"type": "string"}},
            "required": ["circle"],
            "additionalProperties": False,
        },
    ),
    "district_names_severity_wise": ToolSpec(
        name="district_names_severity_wise",
        path="/fetch_district_names_severity_wise",
        method="POST",
        description="Fetch district names grouped by severity for 7 days.",
        parameters={
            "type": "object",
            "properties": {"circle": {"type": "string"}},
            "required": ["circle"],
            "additionalProperties": False,
        },
    ),
    "district_wise_kpi_values": ToolSpec(
        name="district_wise_kpi_values",
        path="/fetch_district_wise_KPI_values",
        method="POST",
        description="Fetch district-wise KPI values for 7 days.",
        parameters={
            "type": "object",
            "properties": {"circle": {"type": "string"}},
            "required": ["circle"],
            "additionalProperties": False,
        },
    ),
   "kpi_legend_with_color": ToolSpec(
        name="kpi_legend_with_color",
        path="/fetch_kpi_legend_with_color",
        method="POST",
        description="Fetch KPI legend with severity colors for a circle.",
        parameters={
            "type": "object",
            "properties": {"circle": {"type": "string"}},
            "required": ["circle"],
            "additionalProperties": False,
        },
    ),
   
}


def _get_base_url(base_url: Optional[str] = None) -> str:
    """Get the base URL for API calls."""
    return (base_url or DEFAULT_BASE_URL).rstrip("/")


def list_tool_specs(names: Optional[Iterable[str]] = None) -> List[ToolSpec]:
    """List available tool specifications.
    
    Args:
        names: Optional iterable of tool names to filter by.
        
    Returns:
        List of ToolSpec objects.
    """
    if names is None:
        return list(TOOL_SPECS.values())
    return [TOOL_SPECS[name] for name in names if name in TOOL_SPECS]


def build_openai_tools(names: Optional[Iterable[str]] = None) -> List[Dict[str, Any]]:
    """Build OpenAI-style tool definitions.
    
    Args:
        names: Optional iterable of tool names to filter by.
        
    Returns:
        List of OpenAI function definitions.
    """
    tool_defs: List[Dict[str, Any]] = []
    for spec in list_tool_specs(names):
        tool_defs.append(
            {
                "type": "function",
                "function": {
                    "name": spec.name,
                    "description": spec.description,
                    "parameters": spec.parameters,
                },
            }
        )
    return tool_defs


def call_tool(
    tool_name: str,
    payload: Optional[Dict[str, Any]] = None,
    *,
    base_url: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30,
) -> Any:
    """Call a tool by name.
    
    Args:
        tool_name: Name of the tool to call.
        payload: JSON payload for the request.
        base_url: Override the base URL.
        headers: Additional headers to include.
        timeout: Request timeout in seconds.
        
    Returns:
        JSON response or text.
        
    Raises:
        KeyError: If tool_name is not found.
        requests.RequestException: If the request fails.
    """
    if tool_name not in TOOL_SPECS:
        raise KeyError(f"Unknown tool: {tool_name}")

    spec = TOOL_SPECS[tool_name]
    url = f"{_get_base_url(base_url)}{spec.path}"
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)

    response = requests.request(
        spec.method,
        url,
        json=payload or {},
        headers=request_headers,
        timeout=timeout,
    )
    response.raise_for_status()

    try:
        return response.json()
    except ValueError:
        return response.text


def call_endpoint(
    path: str,
    payload: Optional[Dict[str, Any]] = None,
    *,
    method: str = "POST",
    base_url: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30,
) -> Any:
    """Call an endpoint directly by path.
    
    Args:
        path: API endpoint path.
        payload: JSON payload for the request.
        method: HTTP method (default: POST).
        base_url: Override the base URL.
        headers: Additional headers to include.
        timeout: Request timeout in seconds.
        
    Returns:
        JSON response or text.
        
    Raises:
        requests.RequestException: If the request fails.
    """
    url = f"{_get_base_url(base_url)}{path if path.startswith('/') else '/' + path}"
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)

    response = requests.request(
        method.upper(),
        url,
        json=payload or {},
        headers=request_headers,
        timeout=timeout,
    )
    response.raise_for_status()

    try:
        return response.json()
    except ValueError:
        return response.text


__all__ = [
    "ToolSpec",
    "TOOL_SPECS",
    "build_openai_tools",
    "call_endpoint",
    "call_tool",
    "list_tool_specs",
]
