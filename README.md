# SearxNG Search with MCP

A tool for performing searches using SearxNG, with both CLI and Model Context Protocol (MCP) interfaces.

## Installation

1. Clone this repository
2. Install the package:
```bash
pip install -e .
```

## Usage

### Command Line Interface

```bash
searxng-cli "your search query" --host "http://your-searx-instance" [--engines "engine1,engine2"]
```

#### CLI Arguments

- `query`: Search query (positional argument)
- `--host`: SearxNG host URL (default: http://localhost:8888)
- `--engines`: Comma-separated list of search engines to use (optional)
- `--num-results`: Number of results to return (optional, default: 10)
- `--categories`: Comma-separated list of categories to use (optional)

#### CLI Example

```bash
searxng-cli "python programming" --host "http://localhost:8888" --engines "google,duckduckgo"
```

### MCP Server

This project includes an MCP server that allows AI models to access SearxNG search functionality.

#### Running the MCP Server

You can run the MCP server directly:

```bash
searxng-mcp
```

Or use it with MCP development tools:

```bash
mcp dev searxng-mcp
```

#### MCP Features

- `search` tool: Search the web via SearxNG
- Resources: Access information about SearxNG categories and engines
- Structured output: Results are returned in a well-structured format for easy parsing

## Requirements

- Python 3.8+
- langchain-community
- mcp

## Configuration

Set the `SEARX_HOST` environment variable to specify your SearxNG instance:

```bash
export SEARX_HOST=http://localhost:8888
```

## Notes

Make sure your SearxNG instance is properly set up and accessible at the provided host URL.
