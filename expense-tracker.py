import argparse

def main():
    parser = argparse.ArgumentParser(description="Enpense Tracker Program")
    subparsers = parser.add_subparsers(dest="command", help="Support commands")
    add_parser = subparsers.add_parser("add", help="Add another expense")
    add_parser.add_argument("--description", type=str, required=True, help="Description of expense")
    add_parser.add_argument("--amount", type=float, required=True, help="Amount spent")

    args = parser.parse_args()

    if args.command == "add":
        print("--- Added Successfully ---")
        print(f"Content: {args.description}")
        print(f"Amount: {args.amount}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()