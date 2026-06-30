from app import mcp
from config import ENABLE_INTERNAL_TOOLS

def internal_tool():
    """Register a tool only when internal tools are enabled on the server."""
    def decorator(func):
        if ENABLE_INTERNAL_TOOLS:
            return mcp.tool()(func)
        return func

    return decorator
