# context.py

from contextvars import ContextVar

current_token: ContextVar[str | None] = ContextVar(
    "current_token",
    default=None
)