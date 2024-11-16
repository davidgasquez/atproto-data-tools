# `atproto` Data Tools

Small scripts and tools to do data stuff with the AT Protocol.

## 🚀 Setup

You can either install this package (`pip install git+https://github.com/davidgasquez/atproto-data-tools`) or run the commands directly with `uvx`.

```bash
uvx --from 'git+https://github.com/davidgasquez/atproto-data-tools' adt-export-followers username.com --username $BSKY_USERNAME --password $BSKY_PASSWORD
```

## 🛠️ Commands

- `adt-socialgraph`: Builds an edge list (source, target) of follows from profiles found in a Bluesky hashtag search.
- `adt-export-followers`: Exports followers of a given Bluesky user.
- `adt-export-plc`: Exports all plc.directory records.

## 📄 License

MIT
