# SearXNG MCP

A Model Context Protocol (MCP) server and CLI tool for performing web searches using SearxNG.

## Quick Start

Run without installation using `uvx`:

```bash
# CLI search
uvx --from git+https://github.com/varlabz/searxng-mcp searxng-cli "your search query"

# MCP server
uvx --from git+https://github.com/varlabz/searxng-mcp searxng-mcp
```

### Creating Shell Alias

For easier usage, create a shell alias to avoid typing the full `uvx` command:

```bash
# Add to your ~/.bashrc, ~/.zshrc, or ~/.profile
alias searxng-cli='uvx --from git+https://github.com/varlabz/searxng-mcp searxng-cli'
or
alias sx='uvx --from git+https://github.com/varlabz/searxng-mcp searxng-cli --engines "google,duckduckgo" '

# Reload your shell configuration
source ~/.bashrc  # or ~/.zshrc
```

After setting up the alias, you can use it directly:

```bash
searxng-cli "python programming" --engines "google,duckduckgo"
# or
sx "python programming" 
```

**Options:**
- `--host`: SearxNG host URL (default: `http://localhost:8888`)
- `--engines`: Comma-separated search engines (e.g., `google,duckduckgo`)
- `--num-results`: Number of results (default: 10)
- `--categories`: Search categories

**Example:**
```bash
# Full command
uvx --from git+https://github.com/varlabz/searxng-mcp searxng-cli "python programming" --engines "google,duckduckgo"

# Using alias
sx "python programming" --engines "brave"
```

## MCP Server

Provides search functionality to AI models through the Model Context Protocol.

**Configuration:**

Add this to your MCP client configuration for VS Code or other clients (see client configuration):

```json
{
  "mcp": {
    "servers": {
      "searxng": {
        "command": "uvx",
        "args": ["--from", "git+https://github.com/varlabz/searxng-mcp", "searxng-mcp"]
        "env": {
          "SEARX_HOST": "http://localhost:8888"
        }
      }
    }
  }
}
```

**Features:**
- `search` tool for web searches
- Access to SearxNG categories and engines
- Structured JSON output
