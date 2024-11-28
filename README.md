# `atproto` Data Tools

Small scripts and tools to extract and analyze data from the AT Protocol (the protocol that powers Bluesky).

## 🔍 Overview

The AT Protocol (Authenticated Transfer Protocol) is a networking technology that powers decentralized social applications like Bluesky. These tools help you extract and analyze data from the AT Protocol network.

## ⚙️ Requirements

- Python 3.8+
- Bluesky account (for some commands)

## 🚀 Setup

You can install this package in two ways:

1. Using pip:

```bash
pip install git+https://github.com/davidgasquez/atproto-data-tools
```

2. Running commands directly with `uvx`:

```bash
uvx --from 'git+https://github.com/davidgasquez/atproto-data-tools' <command>
```

For commands that require authentication, you'll need to set up your Bluesky credentials as environment variables:

```bash
export BSKY_USERNAME="your-username"
export BSKY_PASSWORD="your-app-password"
```

Note: For the password, use an App Password generated from your Bluesky account settings for better security.

## 🛠️ Commands

### `adt-social-graph`

Builds an edge list (source, target) of follows from profiles found in a Bluesky hashtag search. This is useful for social network analysis and visualizing communities around specific topics.

```bash
adt-social-graph --hashtag ai --output ai_network.csv
```

Output format: CSV file with columns `source,target` representing follow relationships.

### `adt-export-followers`

Exports all followers of a given Bluesky user. The data includes usernames and other profile information.

```bash
adt-export-followers yourawesomeusername.com
```

Output format: JSON file containing follower details including handle, display name, and follower count.

### `adt-export-plc`

Exports all records from plc.directory, which contains DID (Decentralized Identifier) information for AT Protocol users.

```bash
adt-export-plc --output plc_records.json
```

Output format: JSON file containing PLC directory records.

## 📄 License

MIT
