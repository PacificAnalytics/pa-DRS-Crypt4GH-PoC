import argparse
from .drs import post_metadata


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Upload file data and register metadata with Data Repository "
            "Service (DRS) web services")
    )
    parser.add_argument("name", type=str, help="File to upload")
    parser.add_argument(
        "--url", type=str, help="DRS base URL",
        default="http://localhost:8080"
    )
    parser.add_argument(
        "--desc", type=str, help="description of the object.", default="",
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    file_id = post_metadata(
        args.name, args.url, args.desc
    )
    print(file_id)


if __name__ == "__main__":
    main()
