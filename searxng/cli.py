#!/usr/bin/env python3
"""
SearXNG CLI

Command line interface for searching using SearXNG instances.
"""

import argparse
import sys
import asyncio
from .search import searx_search


def parse_arguments():
    """Parse command line arguments."""
    from .search import CATEGORIES, ENGINES
    engines_by_category = '\n'.join(
        f"  {cat}: {', '.join(engines)}" for cat, engines in ENGINES.items()
    )
    parser = argparse.ArgumentParser(
        description="Search using SearXNG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  %(prog)s "python programming"
  %(prog)s "climate change" --engines "google,duckduckgo"
  %(prog)s "latest news" --categories "news" --num-results 5

Available categories:
  {', '.join(CATEGORIES)}

Engines by category:
{engines_by_category}
        """
    )
    parser.add_argument(
        "query", 
        nargs='+', 
        help="The search query"
    )
    parser.add_argument(
        "--host", 
        type=str, 
        default="http://localhost:8888", 
        help="SearxNG host URL (default: %(default)s)"
    )
    parser.add_argument(
        "--num-results", 
        type=int, 
        default=10, 
        help="Number of results to return (default: %(default)s)"
    )
    parser.add_argument(
        "--engines", 
        type=str, 
        help="Comma-separated list of search engines to use"
    )
    parser.add_argument(
        "--categories",
        type=str,
        help="Comma-separated list of categories to use"
    )
    parser.add_argument(
        "--time-range",
        type=str,
        choices=["day", "month", "year"],
        help="Time range for search results (optional, allowed: day, month, year)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )
    return parser.parse_args()


async def main_async():
    """Main entry point for the CLI."""
    args = parse_arguments()
    engines = [engine.strip() for engine in args.engines.split(",")] if args.engines else None
    categories = [category.strip() for category in args.categories.split(",")] if args.categories else None
    query = " ".join(args.query)
   
    results = await searx_search(
        searx_host=args.host,
        query=query,
        num_results=args.num_results,
        engines=engines,
        categories=categories,
        time_range=args.time_range,
    )
    
    if not results:
        if args.json:
            print("[]")
        else:
            print("No results found.")
        return 1
    
    # Display results
    if args.json:
        import json
        print(json.dumps(results, indent=2))
    else:
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            if result['content']:
                print(f"   {result['content']}")
            print()
        
        print(f"Found {len(results)} results.")
    return 0


def main():
    """CLI entry point."""
    try:
        sys.exit(asyncio.run(main_async()))
    except KeyboardInterrupt:
        print("\nSearch cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
