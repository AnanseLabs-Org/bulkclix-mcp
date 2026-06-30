import os
import config
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions, RevocationOptions
from mcp.server.auth.provider import ProviderTokenVerifier
from auth_provider import InMemoryOAuthProvider

auth_provider = None
token_verifier = None
auth_settings = None

if os.environ.get("MCP_ENABLE_OAUTH", "false").lower() == "true":
    auth_provider = InMemoryOAuthProvider()
    token_verifier = ProviderTokenVerifier(auth_provider)
    public_url = os.environ.get("MCP_PUBLIC_URL", "https://tools.ananselabs.org")
    
    auth_settings = AuthSettings(
        issuer_url=public_url,
        resource_server_url=public_url,
        required_scopes=["mcp"],
        client_registration_options=ClientRegistrationOptions(enabled=True),
        revocation_options=RevocationOptions(enabled=True)
    )

mcp = FastMCP(
    "ananse-mcp",
    host=os.environ.get("MCP_HOST", "0.0.0.0"),
    port=int(os.environ.get("MCP_PORT", "8000")),
    sse_path="/",
    auth_server_provider=auth_provider,
    token_verifier=token_verifier,
    auth=auth_settings,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=os.environ.get("MCP_DNS_REBINDING_PROTECTION", "true").lower() == "true",
        allowed_hosts=[h.strip() for h in os.environ.get("MCP_PUBLIC_HOSTNAME", "localhost,127.0.0.1,*.ananselabs.org").split(",") if h.strip()],
    ),
)
