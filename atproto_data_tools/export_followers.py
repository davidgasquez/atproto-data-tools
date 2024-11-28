import os
import argparse
from atproto import Client
from atproto_client.models import utils


def get_all_followers(client, author):
    """Get all followers for a given author"""

    cursor = None
    followers = []
    try:
        while True:
            fetched = client.app.bsky.graph.get_followers(
                params={"actor": author, "cursor": cursor, "limit": 100}
            )
            followers = followers + fetched.followers
            if not fetched.cursor:
                break
            cursor = fetched.cursor
        return followers
    except Exception as e:
        print(f"Error getting followers for {author}: {str(e)}")
        print(f"Exception details: {e}")
        return []


def export_followers(
    author, username=None, password=None, output_file="followers.ndjson"
):
    # Initialize client and login
    client = Client()

    # Use provided credentials or fall back to environment variables
    username = username or os.getenv("BSKY_USERNAME")
    password = password or os.getenv("BSKY_PASSWORD")

    if not username or not password:
        raise ValueError(
            "Bluesky credentials not found. Please either:\n"
            "1. Set BSKY_USERNAME and BSKY_PASSWORD environment variables, or\n"
            "2. Provide credentials using --username and --password arguments"
        )

    client.login(username, password)

    # Get all followers
    print(f"Fetching followers for {author}...")
    followers = get_all_followers(client, author)

    # Export followers to file
    print(f"Exporting followers to {output_file}...")
    with open(output_file, "w") as f:
        for follower in followers:
            f.write(utils.to_json(follower).decode("utf-8") + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Export followers for a specific Bluesky user"
    )
    parser.add_argument("author", help="Author handle to fetch followers for")
    parser.add_argument(
        "--output",
        "-o",
        default="followers.ndjson",
        help="Output file path (default: followers.ndjson)",
    )
    parser.add_argument(
        "--username",
        "-u",
        help="Bluesky username (falls back to BSKY_USERNAME environment variable)",
    )
    parser.add_argument(
        "--password",
        "-p",
        help="Bluesky password (falls back to BSKY_PASSWORD environment variable)",
    )

    args = parser.parse_args()

    try:
        export_followers(
            args.author,
            username=args.username,
            password=args.password,
            output_file=args.output,
        )
        print(f"\nFollowers exported to {args.output}")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
