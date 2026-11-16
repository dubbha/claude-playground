import asyncio
import argparse
from starlette.requests import Request
from starlette.responses import Response
from mcp.server.fastmcp import FastMCP, Context

parser = argparse.ArgumentParser()
parser.add_argument("--stateless-http", action="store_true")
parser.add_argument("--json-response", action="store_true")

stateless_http = parser.parse_args().stateless_http
json_response = parser.parse_args().json_response

stateless_http_color = "\033[32m" if stateless_http else "\033[31m"
stateless_http_status = "enabled" if stateless_http else "disabled"
print(f"\nStateless HTTP (--stateless-http): {stateless_http_color}{stateless_http_status}\033[0m")

json_response_color = "\033[32m" if json_response else "\033[31m"
json_response_status = "enabled" if json_response else "disabled"
print(f"JSON Response (--json-response): {json_response_color}{json_response_status}\033[0m\n")

mcp = FastMCP(
    "mcp-server",
    host="localhost",
    stateless_http=stateless_http,
    json_response=json_response,
)


@mcp.tool()
async def add(a: int, b: int, ctx: Context) -> int:
    await ctx.info("Preparing to add...")
    await asyncio.sleep(2)
    await ctx.report_progress(80, 100)

    return a + b


# Load the demo HTML page
@mcp.custom_route("/", methods=["GET"])
async def get(request: Request) -> Response:
    with open("index.html", "r") as f:
        html_content = f.read()

    disabled_attribute = "disabled" if stateless_http else ""
    html_content = html_content.replace(
        "{{DISABLED_IF_STATELESS_HTTP}}", disabled_attribute
    )
    
    return Response(content=html_content, media_type="text/html")


mcp.run(transport="streamable-http")
