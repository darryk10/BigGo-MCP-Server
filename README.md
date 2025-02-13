# BigGo MCP Server (Python)

## Tools
- [x] Price History With URL
- [x] Price History With History ID
  - History ID can be found in the result of `product_search`
  - Typical use case:
    - User provide a product name, and the model finds the most relevant product from the search result, use the history ID of the product as the argument.
- [x] Product Search
- [x] Spec Indexes
  - List elasticsearch indexes related to product specification
- [x] Spec Mapping
  - Elasticsearch index mapping plus an example document
- [x] Spec Search
  - Search product specification with elasticsearch query

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
`pytest` is a dependency in group `test`.
We need to specify the group to run tests.
```
uv run --group test pytest
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
        "biggo-mcp-server",
        // "--log-level",
        // "INFO"
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
        "biggo-mcp-server@0.1.0" // PROJECT_NAME@VERSION
        // "--log-level",
        // "INFO"
      ],
      "enabled": true
    }
  }
}
```

### Arguments
| Variable          | Description               | Default                           | Choices                                    |
| ----------------- | ------------------------- | --------------------------------- | ------------------------------------------ |
| `--region`        | Region for product search | TW                                | US, TW, JP, HK, SG, MY, IN, PH, TH, VN, ID |
| `--client-id`     | Client ID                 | None                              |                                            |
| `--client-secret` | Client Secret             | None                              |                                            |
| `--log-level`     | Log level                 | INFO                              | DEBUG, INFO, WARNING, ERROR, CRITICAL      |
| `--es-proxy-url`  | Elasticsearch proxy URL   | http://es-proxy.d.cloud.biggo.com |                                            |
