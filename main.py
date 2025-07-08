#!/usr/bin/env python3
from langchain_community.utilities import SearxSearchWrapper
from typing import List, Dict
import argparse
import sys
import asyncio

async def searx_search(searx_host: str, query: str, num_results: int = 10, engines: List[str] = None, categories: List[str] = None) -> List[Dict[str, str]]:
    """
    Perform a search using SearxSearchWrapper.

    Args:
        searx_host (str): The Searx instance host URL.
        query (str): The search query.
        num_results (int): The number of results to return.
        engines (List[str], optional): List of engines to use. Defaults to None.
        categories (List[str], optional): List of categories to use. Defaults to None.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing the title, link, and snippet of a search result.
    """
    try:
        searx = SearxSearchWrapper(searx_host=searx_host, engines=engines, categories=categories)
        results = await searx.aresults(query=query, num_results=num_results, )
        return [{"title": r.get("title", ""), "url": r.get("link", ""), "content": r.get("snippet", "")} for r in results]
    except Exception as e:
        print(f"Error performing search: {str(e)}", file=sys.stderr)
        return []

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Search using SearxNG")
    parser.add_argument("--host", type=str, required=True, help="SearxNG host URL (e.g., 'http://localhost:8888')")
    parser.add_argument("--num-results", type=int, default=10, help="Number of results to return")
    parser.add_argument("--engines", type=str, help="Comma-separated list of search engines to use")
    parser.add_argument("--categories", type=str, help="Comma-separated list of categories to use")
    parser.add_argument("query", nargs='+', help="The search query")
    return parser.parse_args()

async def main():
    """Main entry point for the CLI."""
    args = parse_arguments()
    engines = [engine.strip() for engine in args.engines.split(",")] if args.engines else None
    categories = [category.strip() for category in args.categories.split(",")] if args.categories else None
    query = " ".join(args.query)
    results = await searx_search(args.host, query, num_results=args.num_results, engines=engines, categories=categories)
    for result in results:
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Content: {result['content']}")
        print("-" * 20)
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

# Categories:
# general, images, videos, news, map, music, science, social media

# Common engines available in SearxNG:
# Web Search Engines:
#   google, bing, duckduckgo, startpage, searx, yandex, yahoo, brave, kagi
#   qwant, mojeek, yep, presearch, metager, swisscows, peertube
#
# News Engines:
#   google news, bing news, yahoo news, reuters, associated press, bbc
#   cnn, guardian, npr, reddit, hackernews, lobste.rs
#
# Image Engines:
#   google images, bing images, flickr, unsplash, pixabay, deviantart
#   wikimedia commons, 1x, 500px
#
# Video Engines:
#   youtube, vimeo, dailymotion, peertube, invidious, bilibili
#
# Map Engines:
#   openstreetmap, google maps, bing maps, wikimapia, fdroid
#
# Music Engines:
#   soundcloud, spotify, bandcamp, genius, musixmatch, radio browser
#
# Science/Academic:
#   arxiv, pubmed, crossref, semantic scholar, google scholar, microsoft academic
#   internet archive, library genesis, anna's archive
#
# IT/Programming:
#   github, gitlab, stackoverflow, codeberg, pypi, npm, dockerhub
#   arch linux wiki, gentoo wiki, askubuntu, superuser
#
# Social Media:
#   mastodon, lemmy, reddit, 4chan, tiktok, imgur
#
# Dictionary/Reference:
#   wiktionary, wikipedia, urban dictionary, wordnik, etymonline
#
# Files/Torrents:
#   piratebay, 1337x, nyaa, eztv, torrentz, solidtorrents
#
# Shopping:
#   amazon, ebay, google shopping, bing shopping, wikidata
#
# Note: Available engines depend on your SearxNG instance configuration.
# Use the preferences page of your SearxNG instance to see which engines are enabled.    