# /// script
# dependencies = [
#   "atproto",
# ]
# ///

import os
import time
import argparse
from atproto import Client


def get_all_follows(client, author):
    cursor = None
    follows = []
    try:
        while True:
            fetched = client.app.bsky.graph.get_follows(
                params={"actor": author, "cursor": cursor}
            )
            follows = follows + fetched.follows
            if not fetched.cursor:
                break
            cursor = fetched.cursor
        return follows
    except Exception as e:
        print(f"Error getting follows for {author}: {str(e)}")
        print(f"Exception details: {e}")
        return []


def get_posts_with_hashtag(client, hashtag):
    cursor = None
    posts = []

    while True:
        fetched = client.app.bsky.feed.search_posts(
            params={"q": f"#{hashtag}", "cursor": cursor}
        )
        posts = posts + fetched.posts

        if not fetched.cursor:
            break

        cursor = fetched.cursor

    return posts


def export_social_graph(hashtag, username=None, password=None, output_file="edges.csv"):
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

    # Get all posts with hashtag
    print(f"Fetching posts with #{hashtag}...")
    posts = get_posts_with_hashtag(client, hashtag)

    # Get unique authors
    unique_authors = list(set(post.author.handle for post in posts))
    print(f"Found {len(unique_authors)} unique authors")

    # Create edges file
    print("Exporting social graph...")
    with open(output_file, "w") as f:
        # Write header
        f.write(
            "source,target,source_avatar_url,source_posts_count,source_followers_count,source_follows_count\n"
        )

        # Process each author
        for source in unique_authors:
            try:
                print(f"Processing author: {source}")

                # Get author profile
                try:
                    source_actor = client.app.bsky.actor.get_profile(
                        params={"actor": source}
                    )
                except Exception as e:
                    print(f"Error fetching profile for {source}: {str(e)}")
                    continue

                # Get all follows
                author_follows = get_all_follows(client, source)

                # Write edges
                for follow in author_follows:
                    f.write(
                        f"{source},{follow.handle},{source_actor.avatar},{source_actor.posts_count},"
                        f"{source_actor.followers_count},{source_actor.follows_count}\n"
                    )

                # Rate limiting
                time.sleep(0.5)

            except Exception as e:
                print(f"Error processing author {source}: {str(e)}")
                continue


def main():
    parser = argparse.ArgumentParser(
        description="Export social graph for Bluesky users using a specific hashtag"
    )
    parser.add_argument("hashtag", help="Hashtag to search for (without the # symbol)")
    parser.add_argument(
        "--output",
        "-o",
        default="edges.csv",
        help="Output file path (default: edges.csv)",
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
        export_social_graph(
            args.hashtag,
            username=args.username,
            password=args.password,
            output_file=args.output,
        )
        print(f"\nSocial graph exported to {args.output}")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
