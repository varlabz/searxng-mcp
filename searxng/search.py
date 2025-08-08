"""
SearXNG Search Functions

This module provides async search functionality using SearXNG instances.
"""

import sys
from typing import List, Dict, Optional
from langchain_community.utilities import SearxSearchWrapper

# Common SearXNG categories
CATEGORIES = [
    "general", "images", "videos", "news", "map", "music",
    "it", "science", "files", "social_media"
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

TIME_RANGES = {"day", "month", "year"}

async def searx_search(
    searx_host: str,
    query: str,
    num_results: int = 10,
    engines: Optional[List[str]] = [],
    categories: Optional[List[str]] = [],
    time_range: Optional[str] = None
) -> List[Dict[str, str]]:
    """
    Perform a search using SearxSearchWrapper.

    Args:
        searx_host: The SearXNG instance host URL
        query: The search query
        num_results: The number of results to return (default: 10)
        engines: List of engines to use (optional)
        categories: List of categories to use (optional)
        time_range: Time range for search results (optional, e.g. 'day', 'month', 'year')

    Returns:
        List of dictionaries containing search results with title, url, and content
    """
    try:
        searx = SearxSearchWrapper(
            searx_host=searx_host,
            engines=engines,
            categories=categories
        )
        aresults_kwargs = {
            "query": query,
            "num_results": num_results,
        }
        if time_range:
            aresults_kwargs["time_range"] = time_range
        results = await searx.aresults(**aresults_kwargs)
        if len(results) == 1 and "Result" in results[0]:    # special case for single result
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
        print(f"Error performing search: {str(e)}", file=sys.stderr)
        return []
