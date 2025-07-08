# SearxNG Search CLI

A simple command-line interface for performing searches using SearxNG.

## Installation

1. Clone this repository
2. Install dependencies:
```
pip install -r requirements.txt
```

## Usage

```
python main.py --host "http://your-searx-instance" --query "your search query" [--engines "engine1,engine2"]
```

### Arguments

- `--host`: SearxNG host URL (required)
- `--query`: Search query (required)
- `--engines`: Comma-separated list of search engines to use (optional)

### Example

```
python main.py --host "http://localhost:8888" --query "python programming" --engines "google,duckduckgo"
```

## Requirements

- Python 3.7+
- langchain-community
- argparse

## Notes

Make sure your SearxNG instance is properly set up and accessible at the provided host URL.
