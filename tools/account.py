from typing import Any, Dict
from decorators import internal_tool
from http_client import _call_api

@internal_tool(read_only=True, destructive=False, open_world=True)
async def account_wallet_balance() -> Dict[str, Any]:
    """
    Check your BulkClix wallet balance.
    """
    return await _call_api( "GET", "/account/balance")
