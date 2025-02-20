# Build Documentation
Documentation for local development and installation.

## Development
### Setup
1. Install [uv](https://docs.astral.sh/uv/) package manager
2. Install dependencies:
   ```
   uv sync
   ```

### Testing and development
1. Run with MCP Inspector:
   ```
   npx @modelcontextprotocol/inspector uv run BigGo-MCP-Server
   ```

2. Run tests:
   ```
   uv run --group test pytest
   ```


## Install From Local Project
Use absolute path for `--directory` argument.
```json
{
  "mcpServers": {
    "biggo-mcp-server": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/biggo-mcp-server",
        "BigGo-MCP-Server",
      ],
      "env": {
        "BIGGO_MCP_SERVER_CLIENT_ID": "YOUR_CLIENT_ID",
        "BIGGO_MCP_SERVER_CLIENT_SECRET": "YOUR_CLIENT_SECRET",
        "BIGGO_MCP_SERVER_REGION": "YOUR_REGION"
      }
    }
  }
}
```

## Complete Environment Variables
| Variable                             | Description                        | Default                                      | Choices                                    |
| ------------------------------------ | ---------------------------------- | -------------------------------------------- | ------------------------------------------ |
| `BIGGO_MCP_SERVER_REGION`            | Region for product search          | TW                                           | US, TW, JP, HK, SG, MY, IN, PH, TH, VN, ID |
| `BIGGO_MCP_SERVER_CLIENT_ID`         | Client ID                          | None                                         | Required for specification search          |
| `BIGGO_MCP_SERVER_CLIENT_SECRET`     | Client Secret                      | None                                         | Required for specification search          |
| `BIGGO_MCP_SERVER_LOG_LEVEL`         | Log level                          | INFO                                         | DEBUG, INFO, WARNING, ERROR, CRITICAL      |
| `BIGGO_MCP_SERVER_ES_PROXY_URL`      | Elasticsearch proxy URL            | `https://api.biggo.com/api/v1/mcp-es-proxy/` |
| `BIGGO_MCP_SERVER_ES_VERIFY_CERTS`   | Verify Elasticsearch certificates  | True                                         | True, False                                |
| `BIGGO_MCP_SERVER_AUTH_TOKEN_URL`    | Auth token URL                     | `https://api.biggo.com/auth/v1/token`        |
| `BIGGO_MCP_SERVER_AUTH_VERIFY_CERTS` | Verify Auth token URL certificates | True                                         | True, False                                |

### Project Architecture
```
src/
└── biggo_mcp_server/
    ├── __init__.py         # MCP Server Entrypoint
    ├── lib/
    │   ...
    │   ├── server.py       # Server class      
    │   └── server_setup.py # Server initialization (load tools..etc)
    ├── services/           # Tool logic
    ├── tools/              # Tool entrypoint
    └── types/
        ├── api_ret/        # API responses
        ...
        ├── responses.py    # Tool responses
        └── setting.py      # Server setting
```

### Publishing
Publishing is done automatically with GitHub Actions when a new release is created. 
1. Create a new release in the GitHub Releases page
2. GitHub Actions will build the project and push the new version to PyPI
3. Package version will be the release tag, ex: `v0.1.1`
