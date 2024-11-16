import json
import time
import httpx
import argparse


def export_plc_data(output_file):
    client = httpx.Client()
    cursor = None

    while True:
        response = client.get(f"https://plc.directory/export?count=1000&after={cursor}")

        if response.status_code == 429:
            print("Rate limit hit. Retrying after 60 seconds.")
            time.sleep(60)
            continue

        lines = response.text.strip().split("\n")
        data = [json.loads(line) for line in lines]

        with open(output_file, "a") as f:
            for entry in data:
                json.dump(entry, f)
                f.write("\n")

        cursor = data[-1]["createdAt"]


def main():
    parser = argparse.ArgumentParser(
        description="Export PLC Directory data to a specified file"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="pld.ndjson",
        help="Output file path (default: pld.ndjson)",
    )

    args = parser.parse_args()

    try:
        export_plc_data(args.output)
        print(f"\nPLC data exported to {args.output}")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
