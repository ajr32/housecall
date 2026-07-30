"""
Custom exceptions used by HouseCall.
"""


class HouseCallError(Exception):
    """Base exception for HouseCall."""


class ConfigurationError(HouseCallError):
    """Configuration error."""


class APIError(HouseCallError):
    """Home Assistant API error."""
