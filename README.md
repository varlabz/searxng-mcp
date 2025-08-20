# SearXNG MCP / CLI for local hosting SearXNG search engine

A Model Context Protocol (MCP) server and CLI tool for performing web searches using SearXNG.

## MCP Server Configuration

The MCP server provides a powerful way to integrate SearXNG with AI models. It exposes a `search` tool that can be configured with various parameters to customize your search queries.

### Server Parameters

The MCP server can be configured using the following environment variables:

- `SEARX_HOST`: The URL of your SearxNG instance. Defaults to `http://localhost:8888`.

### MCP Tool: `search`

The `search` tool allows you to perform web searches through SearXNG. It accepts the following parameters:

- `query` (string, required): The search query.
- `num_results` (integer, optional): The number of search results to return. Defaults to `10`.
- `engines` (string, optional): A comma-separated list of search engines to use (e.g., "google,duckduckgo").
- `categories` (string, optional): A comma-separated list of search categories to filter results (e.g., "news,images").
- `time_range` (string, optional): The time range for the search. Can be one of `"day"`, `"month"`, or `"year"`.

### MCP Resources

The MCP server also provides the following resources to get more information about your SearxNG instance:

- `searx-categories://`: Returns a list of available search categories.
- `searx-engines://`: Returns a list of available search engines.
- `searx-info://`: Provides general information about the SearXNG MCP server.

### Example MCP Client Configuration

To use the SearXNG MCP server with your AI model, you need to add it to your MCP client configuration. Here is an example configuration for a VS Code client:

```json
{
  "mcp": {
    "servers": {
      "searxng": {
        "command": "uvx",
        "args": ["--from", "git+https://github.com/varlabz/searxng-mcp", "mcp-server"],
        "env": {
          "SEARX_HOST": "http://localhost:8888"
        }
      }
    }
  }
}
```

## CLI Usage

### Quick Start

You can run the CLI without installation using `uvx`:

```bash
uvx --from git+https://github.com/varlabz/searxng-mcp cli "your search query"
```

### Creating Shell Alias

For easier usage, create a shell alias to avoid typing the full `uvx` command:

```bash
# Add to your ~/.bashrc, ~/.zshrc, or ~/.profile
alias searxng-cli='uvx --from git+https://github.com/varlabz/searxng-mcp cli'
or
alias sx='uvx --from git+https://github.com/varlabz/searxng-mcp cli --engines "google,duckduckgo" '

# Reload your shell configuration
source ~/.bashrc  # or ~/.zshrc
```

### CLI Options

- `--host`: SearxNG host URL (default: `http://localhost:8888`).
- `--num-results`: Number of results to return (default: `10`).
- `--engines`: Comma-separated list of search engines to use.
- `--categories`: Comma-separated list of search categories to use.
- `--time-range`: Time range for search results (day, month, or year).
- `--json`: Output results in JSON format.

```bash
$ sx --help
usage: cli [-h] [--host HOST] [--num-results NUM_RESULTS] [--engines ENGINES] [--categories CATEGORIES] [--time-range {day,month,year}] [--json] query [query ...]

Search using SearXNG

positional arguments:
  query                 The search query

options:
  -h, --help            show this help message and exit
  --host HOST           SearxNG host URL (default: http://localhost:8888)
  --num-results NUM_RESULTS
                        Number of results to return (default: 10)
  --engines ENGINES     Comma-separated list of search engines to use
  --categories CATEGORIES
                        Comma-separated list of categories to use
  --time-range {day,month,year}
                        Time range for search results (optional, allowed: day, month, year)
  --json                Output results in JSON format

Examples:
  cli "python programming"
  cli "climate change" --engines "google,duckduckgo"
  cli "latest news" --categories "news" --num-results 5

Available categories:
  general, images, videos, news, map, music, it, science, files, social_media

Engines by category:
  general: google, bing, duckduckgo, startpage, brave, yahoo, yandex, mojeek, qwant, presearch
  images: google_images, bing_images, duckduckgo_extra, unsplash, pixabay, flickr, imgur, pinterest, wallhaven, wikicommons
  videos: youtube_noapi, vimeo, dailymotion, peertube, rumble, odysee, bilibili, niconico
  news: google_news, bing_news, yahoo_news, reuters, bbc, cnn, guardian, reddit, qwant, tagesschau
  map: openstreetmap, apple_maps, photon
  music: genius, bandcamp, deezer, mixcloud, soundcloud, youtube_noapi, radio_browser
  it: github, gitlab, stackoverflow, pypi, npm, crates, docker_hub, metacpan, huggingface
  science: arxiv, pubmed, crossref, semantic_scholar, google_scholar, mediawiki
  files: apkmirror, apple_app_store, fdroid, google_play, piratebay, zlibrary, annas_archive, nyaa
  social_media: reddit, lemmy, mastodon, 9gag, tootfinder
```

### Examples

```bash
# Basic search
sx "python programming"

# Search with specific engines
sx "python programming" --engines "google,duckduckgo"

# Search for news within the last day
sx "latest news" --categories "news" --time-range "day"
```

