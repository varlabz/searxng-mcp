"""
SearXNG Search Functions

This module provides async search functionality using SearXNG instances.
"""

import sys
from typing import List, Dict, Optional, Literal
from .searx_search import SearxSearchWrapper

# Common SearXNG categories
CATEGORIES = [
    "web", "images", "videos", "news", "map", "music",
    "it", "science", "files", "social media"
]

# Common SearXNG engines grouped by category
ENGINES = {
    "general": [
        "google", "bing", "duckduckgo", "startpage", "brave", "yahoo", "yandex", "mojeek", "qwant", "presearch"
    ],
    "images": [
        "google_images", "bing_images", "duckduckgo_extra", "unsplash", "pixabay", "flickr", "imgur", "pinterest", "wallhaven", "wikicommons"
    ],
    "videos": [
        "youtube_noapi", "vimeo", "dailymotion", "peertube", "rumble", "odysee", "bilibili", "niconico"
    ],
    "news": [
        "google_news", "bing_news", "yahoo_news", "reuters", "bbc", "cnn", "guardian", "reddit", "qwant", "tagesschau"
    ],
    "map": [
        "openstreetmap", "apple_maps", "photon"
    ],
    "music": [
        "genius", "bandcamp", "deezer", "mixcloud", "soundcloud", "youtube_noapi", "radio_browser"
    ],
    "it": [
        "github", "gitlab", "stackoverflow", "pypi", "npm", "crates", "docker_hub", "metacpan", "huggingface"
    ],
    "science": [
        "arxiv", "pubmed", "crossref", "semantic_scholar", "google_scholar", "mediawiki"
    ],
    "files": [
        "apkmirror", "apple_app_store", "fdroid", "google_play", "piratebay", "zlibrary", "annas_archive", "nyaa"
    ],
    "social_media": [
        "reddit", "lemmy", "mastodon", "9gag", "tootfinder"
    ]
}

async def searx_search(
    searx_host: str,
    query: str,
    num_results: int = 10,
    engines: Optional[List[str]] = [],
    categories: Optional[List[str]] = [],
    time_range: Optional[Literal["day", "month", "year"]] = None
) -> List[Dict[str, str]]:
    """
    Perform async search using SearXNG.

    Args:
        searx_host: SearXNG instance URL
        query: Search query
        num_results: Number of results (default: 10)
        engines: Specific engines to use
        categories: Specific categories to search
        time_range: Time filter ('day', 'month', or 'year')

    Returns:
        List of search results with title, url, and content
    """
    try:
        searx = SearxSearchWrapper(
            searx_host=searx_host,
            engines=engines,
            categories=categories
        )
        
        search_params = {"query": query, "num_results": num_results}
        if time_range:
            search_params["time_range"] = time_range
           
        results = await searx.aresults(**search_params)
        
        # Handle empty result case
        if len(results) == 1 and "Result" in results[0]:
            return []

        return [
            {
                "title": r.get("title", ""),
                "url": r.get("link", ""),
                "content": r.get("snippet", "")
            }
            for r in results
        ]
    except Exception as e:
        print(f"Search error: {e}", file=sys.stderr)
        return []
