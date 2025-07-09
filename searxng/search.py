"""
SearXNG Search Functions

This module provides async search functionality using SearXNG instances.
"""

import sys
from typing import List, Dict, Optional
from langchain_community.utilities import SearxSearchWrapper


async def searx_search(
    searx_host: str, 
    query: str, 
    num_results: int = 10, 
    engines: Optional[List[str]] = None, 
    categories: Optional[List[str]] = None
) -> List[Dict[str, str]]:
    """
    Perform a search using SearxSearchWrapper.

    Args:
        searx_host: The SearXNG instance host URL
        query: The search query
        num_results: The number of results to return (default: 10)
        engines: List of engines to use (optional)
        categories: List of categories to use (optional)

    Returns:
        List of dictionaries containing search results with title, url, and content
    """
    try:
        searx = SearxSearchWrapper(
            searx_host=searx_host, 
            engines=engines, 
            categories=categories
        )
        results = await searx.aresults(query=query, num_results=num_results)
        return [
            {
                "title": r.get("title", ""), 
                "url": r.get("link", ""), 
                "content": r.get("snippet", "")
            } 
            for r in results
        ]
    except Exception as e:
        print(f"Error performing search: {str(e)}", file=sys.stderr)
        return []
