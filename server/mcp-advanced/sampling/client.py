import asyncio
import os
from dotenv import load_dotenv
from anthropic import AsyncAnthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import RequestContext
from mcp.types import (
    CreateMessageRequestParams,
    CreateMessageResult,
    TextContent,
    SamplingMessage,
)

load_dotenv()

anthropic_client = AsyncAnthropic()
model = os.getenv("CLAUDE_MODEL", "claude-haiku-5-5")

server_params = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
)


async def chat(input_messages: list[SamplingMessage], max_tokens=4000):
    messages = []
    for msg in input_messages:
        if msg.role == "user" and msg.content.type == "text":
            content = (
                msg.content.text
                if hasattr(msg.content, "text")
                else str(msg.content)
            )
            messages.append({"role": "user", "content": content})
        elif msg.role == "assistant" and msg.content.type == "text":
            content = (
                msg.content.text
                if hasattr(msg.content, "text")
                else str(msg.content)
            )
            messages.append({"role": "assistant", "content": content})

    response = await anthropic_client.messages.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
    )

    text = "".join([p.text for p in response.content if p.type == "text"])
    return text


async def sampling_callback(
    context: RequestContext, params: CreateMessageRequestParams
):
    # Call Claude using the Anthropic SDK
    text = await chat(params.messages)

    return CreateMessageResult(
        role="assistant",
        model=model,
        content=TextContent(type="text", text=text),
    )


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, sampling_callback=sampling_callback
        ) as session:
            await session.initialize()

            result = await session.call_tool(
                name="summarize",
                arguments={"text_to_summarize": "MCP defines a standardized framework for integrating AI systems with external data sources and tools.[2] Applications include querying structured databases in plain language. The protocol distinguishes between MCP hosts, MCP clients and MCP servers. An MCP host is typically an AI agent that interacts with an LLM and requires services from one or more MCP servers. For each of these MCP servers, the MCP host will create a dedicated MCP client that communicates with that server. Client and host will typically run on the same machine, while the MCP servers may be local or remote. Each server provides one or more tools or resources. Tools might include database access, calculators, or access to code or repositories; a resource might be a document such as an FAQ. The MCP client asks its server for a list of tools and resources the server provides; the server replies with a natural-language description of the capabilities of each tool and the expected format to call the tool. This information is given to the LLM; if the LLM requires the services of one of these tools, the MCP host will instruct the relevant MCP client to call the tool. The MCP server performs the tool action and returns the results, which the MCP host then injects into the LLM conversation.[12] Client and server communicate using the JSON-RPC 2.0 messages. The protocol was released with software development kits (SDKs) in programming languages including Python, TypeScript, C# and Java and examples of MCP server implementations. The protocol is used in AI-assisted software development tools. Integrated development environments (IDEs), coding platforms such as Replit, and code intelligence tools like Sourcegraph have adopted MCP to grant AI coding assistants real-time access to project context.[6]"}
            )
            print(result.content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
