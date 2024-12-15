from mcp import server
from mcp.server import NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types
import mcp.server.stdio
import os
import pathlib


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="create-hello-file",
            description="Creates a hello-world.txt file in the downloads folder",
            inputSchema={
                "type": "object",
                "properties": {},  # No properties needed for this simple example
                "required": []
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
        name: str,
        arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution."""
    if name != "create-hello-file":
        raise ValueError(f"Unknown tool: {name}")

    # Get downloads directory
    downloads_dir = str(pathlib.Path.home() / "Downloads")
    filepath = os.path.join(downloads_dir, "hello-world.txt")

    try:
        with open(filepath, "w") as f:
            f.write("Hello, World!")

        return [types.TextContent(
            type="text",
            text=f"Successfully created hello-world.txt in {downloads_dir}"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error creating file: {str(e)}"
        )]


async def main():
    """Run the server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="hello-world",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )