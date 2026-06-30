from app import mcp
from config import ENABLE_INTERNAL_TOOLS

from mcp.types import ToolAnnotations

def internal_tool(read_only: bool = False, destructive: bool = False, open_world: bool = True):
    """Register a tool only when internal tools are enabled on the server."""
    def decorator(func):
        if ENABLE_INTERNAL_TOOLS:
            return mcp.tool(
                annotations=ToolAnnotations(
                    readOnlyHint=read_only,
                    destructiveHint=destructive,
                    openWorldHint=open_world
                )
            )(func)
        return func

    return decorator
