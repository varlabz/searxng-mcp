"""
MCP Server for SearXNG Search

This module implements a Model Context Protocol (MCP) server that provides access to SearXNG search functionality.
"""

import os
from typing import List, Optional
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP, Context

from .search import searx_search

# Create an MCP server
mcp = FastMCP(
    "SearXNG Search",
)

# Define models for structured output
class SearchResult(BaseModel):
    """A single search result from SearXNG"""
    title: str = Field(description="The title of the search result")
    url: str = Field(description="The URL of the search result")
    content: str = Field(description="The snippet or content of the search result")

class SearchResults(BaseModel):
    """A collection of search results from SearXNG"""
    results: List[SearchResult] = Field(description="List of search results")
    query: str = Field(description="The search query that was executed")
    total_results: int = Field(description="The number of results returned")

@mcp.tool()
async def search(
    query: str, 
    num_results: int = 10,
    engines: Optional[str] = None,
    categories: Optional[str] = None,
    ctx: Context = None
) -> SearchResults:
    """
    Search the web using SearXNG.   
    """

    searx_host = os.getenv("SEARX_HOST", "http://localhost:8888")
      
    # Log the search query
    if ctx:
        await ctx.info(f"Searching for: {query} with {searx_host}")
        await ctx.report_progress(progress=0.2, message="Starting search...")
    
    # Parse engines and categories if provided
    engines_list = [e.strip() for e in engines.split(",")] if engines else None
    categories_list = [c.strip() for c in categories.split(",")] if categories else None
    
    # Perform the search
    if ctx:
        await ctx.report_progress(progress=0.5, message="Querying SearxNG...")

    results = await searx_search(
        searx_host=searx_host,
        query=query,
        num_results=num_results,
        engines=engines_list,
        categories=categories_list
    )
    
    if ctx:
        await ctx.report_progress(progress=1.0, message=f"Search complete, found {len(results)} results")
    
    # Convert to structured output
    search_results = [
        SearchResult(title=r["title"], url=r["url"], content=r["content"])
        for r in results
    ]
    
    return SearchResults(
        results=search_results,
        query=query,
        total_results=len(search_results)
    )

@mcp.resource("searx-categories://")
def get_categories() -> str:
    """Get a list of available SearxNG search categories"""
    from .search import CATEGORIES
    return "\n".join([f"- {category}" for category in CATEGORIES])

@mcp.resource("searx-engines://")
def get_engines() -> str:
    """Get a list of common SearxNG search engines"""
    from .search import ENGINES
    result = []
    for category, engine_list in ENGINES.items():
        result.append(f"## {category}")
        for engine in engine_list:
            result.append(f"- {engine}")
        result.append("")
    return "\n".join(result)

@mcp.resource("searx-info://")
def get_info() -> str:
    """Get information about SearXNG and how to use it"""
    return """# SearXNG Search

SearXNG is a privacy-respecting, hackable metasearch engine. It aggregates results from various search engines while respecting your privacy.

## How to use this MCP server

1. Use the `search` tool to perform web searches through SearXNG
2. Customize your search with engines and categories parameters
3. Browse available categories with the `searx-categories://` resource
4. Browse common engines with the `searx-engines://` resource

## Examples

- Basic search: `search(query="climate change")`
- Search with specific engines: `search(query="python tutorial", engines="google,stackoverflow,github")`
- Search news only: `search(query="latest developments", categories="news")`

## Note

Make sure the SearxNG instance is running and accessible at the provided host URL.
"""

@mcp.prompt(title="Search Assistant")
def search_prompt(query: str = "climate change") -> str:
    """Create a prompt to help with searching"""
    return f"""Please help me find information about: {query}
Use the search tool to look for relevant information, and provide a summary of the findings.
You may want to try different search engines or categories if the initial results aren't helpful.
"""

def main():
    # Run the MCP server using the default stdio transport
    mcp.run()

if __name__ == "__main__":
    main()