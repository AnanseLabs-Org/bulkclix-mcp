import os
import httpx
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from app import mcp
from db import _get_db
from mcp.types import ToolAnnotations

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.environ.get("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True))
async def whatsapp_send(
    *,
    to_number: str,
    body: str
) -> Dict[str, Any]:
    """
    Send a WhatsApp message using Twilio's API.
    :param to_number: The recipient's phone number or WhatsApp ID (e.g. "+233241234567" or "whatsapp:+233241234567").
    :param body: The text message content to send.
    """
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        return {
            "success": False,
            "error": "Twilio credentials (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) are not set in the environment variables."
        }

    # Normalize recipient WhatsApp prefix
    formatted_to = to_number
    if not formatted_to.startswith("whatsapp:"):
        formatted_to = f"whatsapp:{formatted_to}"

    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    
    data = {
        "From": TWILIO_WHATSAPP_FROM,
        "To": formatted_to,
        "Body": body
    }

    auth = (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=data, auth=auth)
            if response.status_code in (200, 201):
                res_data = response.json()
                return {
                    "success": True,
                    "message_sid": res_data.get("sid"),
                    "status": res_data.get("status"),
                    "to": formatted_to,
                    "from": TWILIO_WHATSAPP_FROM
                }
            else:
                return {
                    "success": False,
                    "error": f"Twilio API Error {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {"success": False, "error": f"Failed to send WhatsApp message: {str(e)}"}


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True))
async def whatsapp_get_messages(
    *,
    limit: int = 20,
    phone_number: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve recent incoming WhatsApp messages from MongoDB.
    :param limit: Maximum number of messages to return (default is 20).
    :param phone_number: Optional phone number to filter messages from a specific customer.
    """
    try:
        db = _get_db()
        if db is None:
            return {"success": False, "error": "Database connection is not available."}

        query = {}
        if phone_number:
            formatted_num = phone_number
            if not formatted_num.startswith("whatsapp:"):
                formatted_num = f"whatsapp:{formatted_num}"
            query["from"] = formatted_num

        cursor = db.whatsapp_messages.find(query, {"_id": 0}).sort("received_at", -1).limit(limit)
        messages = await cursor.to_list(length=limit)

        # Convert datetime objects to ISO strings for JSON serialization
        for msg in messages:
            if isinstance(msg.get("received_at"), datetime):
                msg["received_at"] = msg["received_at"].isoformat()

        return {
            "success": True,
            "count": len(messages),
            "messages": messages
        }
    except Exception as e:
        return {"success": False, "error": f"Failed to retrieve messages: {str(e)}"}
