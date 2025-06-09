from server import mcp

def main():
    print("Starting the Genetic MCP Server...")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
