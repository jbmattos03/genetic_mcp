# genetic_mcp
An MCP server to solve maximization problems using Genetic Algorithm.

# Table of Contents
1. [How it works](#how-it-works)
2. [How to run](#how-to-run)
    - 2.1 [Genetic Algorithm](#genetic-algorithm)
    - 2.2 [MCP Server](#mcp-server)
3. [How to add the MCP server to Cursor](#how-to-add-the-mcp-server-to-cursor)

# How it works
...

# How to run
## Genetic Algorithm
There's already a sample problem loaded in `genetic-mcp-server/genetic_algorithm/main.py`. To run it, run the following commands:
```bash
cd genetic-mcp-server/genetic_algorithm
python3 main.py
```

There are also sample problems in `genetic-mcp-server/genetic_algorithm/samples`. To run them, simply replace `<problem>` below with the name of the actual problem you want to run:
```python
cd genetic-mcp-server/genetic_algorithm
python3 main.py samples/<problem>.json
```

If you want to run your own problems, you have 2 options:
1. Simply modify the following section of `genetic-mcp-server/genetic_algorithm/main.py`:
```python
tsp_data = {
            "options": {
                "population_size": 100,
                "chromosome_size": 4,
                "fitness_function": {
                    "cities": ["A", "B", "C", "D"],
                    "distance_matrix": [
                        [0, 10, 15, 20],
                        [10, 0, 35, 25],
                        [15, 35, 0, 30],
                        [20, 25, 30, 0]
                    ]
                }
            },
            "problem": "traveling_salesman",
            "generations": 50
}
```
2. Create a .json file in the same style of the ones in `genetic-mcp-server/genetic_algorithm/samples` and replace `<path_to_your_file>` with the path to your file:
```python
cd genetic-mcp-server/genetic_algorithm
python3 <path_to_your_file>
```

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
