# BigGo MCP Server (Python)

## Tools
- Price History
- Product Search
- Get EC List 
- Spec Search

## Development
> Install [uv](https://docs.astral.sh/uv/) package manager

### Install Dependencies
```
uv sync
```

### Run with MCP Inspector
```
npx @modelcontextprotocol/inspector uv run biggo-mcp-server
```

### Test
```
uv run test
```

### Build 
```
uv build
```

### Publish
```
uv publish --publish-url http://devpi.cloud.biggo.com/alex/alex
```


## Installation
### From local project
```json
{
  "mcpServers": {
    "biggo-mcp-server": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/home/alex/work/biggo-mcp-server-python", // Absolute path to project
        "biggo-mcp-server"
      ],
      "enabled": true
    }
  }
}
```
### From published package
```json
{
  "mcpServers": {
    "biggo-mcp-server": {
      "command": "uvx",
      "args": [
        "--index",
        "http://devpi.cloud.biggo.com/alex/alex/+simple",
        "--from",
        "biggo-mcp-server@0.1.0", // PROJECT_NAME@VERSION
      ],
      "enabled": true
    }
  }
}
```


