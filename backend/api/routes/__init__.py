"""
API Routes for KrisiSar AI Backend
"""

from . import diagnosis
from . import weather
from . import risk_score
from . import recommendations
from . import schemes
from . import chat
from . import analytics
from . import alerts

__all__ = [
    "diagnosis",
    "weather",
    "risk_score",
    "recommendations",
    "schemes",
    "chat",
    "analytics",
    "alerts",
]
