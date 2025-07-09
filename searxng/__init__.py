"""
SearXNG MCP Server and CLI Package

A tool for performing searches using SearXNG, with both CLI and Model Context Protocol (MCP) interfaces.
"""

__version__ = "0.2.1"
__author__ = "varlabz"
__email__ = "varlabz@umdoze.com"

from .search import searx_search

__all__ = ["searx_search"]
