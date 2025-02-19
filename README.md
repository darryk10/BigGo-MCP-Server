# BigGo MCP Server

A Model Context Protocol (MCP) server that provides product search, price history tracking, and specification search capabilities.

## Features

### Product Search
Search for products across multiple e-commerce platforms with natural language queries.

**Example Prompts:**
```
"Find me iPhone 15 Pro on Shopee"
"Look for Nike running shoes"
```

### Price History Tracking
Track product price history in two ways:
- Direct URL tracking
- History ID tracking (obtained from product search results)

**Example Prompts:**
```
"Show me the price history of this product: https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=13660781"
"Find me the price history of IPhone 15 Pro at Shopee?"
```

### Product Specification Search
Search for products based on specific technical specifications using Elasticsearch.

**Example Prompts:**
```
"Find me refrigerators with the highest energy efficiency rating"
"Search for diving watches that weigh around 120g"
"Show me Japanese air conditioners with heating capability and low noise levels"
```

## Available Tools

### Price History Tools
- **Price History With URL**
  - Tracks price history using product URLs

- **Price History With History ID**
  - Uses history IDs from product search results
  - Typical tool workflow: Search product -> Get history ID -> Track prices

### Product Search
- Product search with biggo search api

### Specification Search Tools
- **Spec Indexes**
  - Lists available Elasticsearch indexes for product specifications

- **Spec Mapping**
  - Shows Elasticsearch index mapping with example documents

- **Spec Search**
  - Advanced specification-based product search

## Installation

### Prerequisites
1. Python 3.13 or higher
2. [uv package manager](https://docs.astral.sh/uv/)
3. BigGo API credentials (client ID and secret) for specification search. Available at [BigGo Account](https://account.biggo.com)

### From Local Project
```json
{
  "mcpServers": {
    "biggo-mcp-server": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/biggo-mcp-server", // Absolute path to project
        "biggo-mcp-server",
        "--client-id",
        "YOUR_CLIENT_ID",
        "--client-secret",
        "YOUR_CLIENT_SECRET"
      ],
      "enabled": true
    }
  }
}
```

### From Published Package
```json
{
  "mcpServers": {
    "biggo-mcp-server": {
      "command": "uvx",
      "args": [
        "--from",
        "biggo-mcp-server", // PROJECT_NAME@VERSION
        "--client-id",
        "YOUR_CLIENT_ID",
        "--client-secret",
        "YOUR_CLIENT_SECRET"
      ],
      "enabled": true
    }
  }
}
```

## Configuration Arguments

| Variable              | Description                       | Default                                    | Choices                                    |
| --------------------- | --------------------------------- | ------------------------------------------ | ------------------------------------------ |
| `--region`            | Region for product search         | TW                                         | US, TW, JP, HK, SG, MY, IN, PH, TH, VN, ID |
| `--client-id`         | Client ID                         | None                                       | Required for specification search          |
| `--client-secret`     | Client Secret                     | None                                       | Required for specification search          |
| `--log-level`         | Log level                         | INFO                                       | DEBUG, INFO, WARNING, ERROR, CRITICAL      |
| `--es-proxy-url`      | Elasticsearch proxy URL           | https://api.biggo.com/api/v1/mcp-es-proxy/ | Any valid URL                              |
| `--es-verify-certs`   | Verify Elasticsearch certificates | True                                       | True, False                                |
| `--auth-token-url`    | Auth token URL                    | https://api.biggo.com/auth/v1/token        | Any valid URL                              |
| `--auth-verify-certs` | Verify Auth certificates          | True                                       | True, False                                |

## Development

### Setup
1. Install [uv](https://docs.astral.sh/uv/) package manager
2. Install dependencies:
   ```
   uv sync
   ```

### Testing and Development
1. Run with MCP Inspector:
   ```
   npx @modelcontextprotocol/inspector uv run biggo-mcp-server
   ```

2. Run tests:
   ```
   uv run --group test pytest
   ```