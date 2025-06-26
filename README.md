# genetic_mcp
An MCP server to solve maximization problems using Genetic Algorithm.

# Table of Contents
1. [How it works](#how-it-works)
2. [How to run](#how-to-run)
    - 2.1 [Genetic Algorithm](#genetic-algorithm)
    - 2.2 [MCP Server](#mcp-server)
3. [How to add the MCP server to Cursor](#how-to-add-the-mcp-server-to-cursor)

# How it works

# How to run
## Genetic Algorithm
There's already a sample problem loaded in `genetic-mcp-server/genetic_algorithm/main.py`. To run it, run the following commands:
```bash
cd genetic-mcp-server/genetic_algorithm
python3 main.py
```

If you want to run your own problems, simply modify the following section of `genetic-mcp-server/genetic_algorithm/main.py`:
```python
if __name__ == "__main__":
    main(
        {
            "population_size": 1000,
            "chromosome_size": 10,
            "fitness_function": {
                    "capacity": [5, 4, 3, 2, 1, 6, 2, 3, 4, 5],
                    "weight": [2, 3, 4, 5, 7, 1, 6, 4.5, 3.5, 2.5],
                    "value": [40, 50, 65, 80, 110, 15, 90, 70, 60, 55],
                    "max_weight": 50
            }
        }
    )
```

**Support for arguments coming soon!**

## MCP Server
If you want to run the MCP server, run:
```bash
cd genetic-mcp-server
uv run main.py
```

# How to add the MCP server to Cursor
Replace `<full-path-to-genetic-mcp-server>` in the following JSON with your actual path:
```json
{
    "mcpServers": {
        "genetic_algorithm_mcp_server": {
            "command": "uv",
            "args": [
                "--directory",
                <full-path-to-genetic-mcp-server>,
                "run",
                "main.py"
            ]
        }
    }
}
```
