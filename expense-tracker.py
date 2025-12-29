import argparse
import json

def load_data(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"next_id": 1, "expenses": []}

def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def main():
    filename = "expense-list.json"
    data = load_data(filename)
    parser = argparse.ArgumentParser(description="Enpense Tracker Program")
    subparsers = parser.add_subparsers(dest="command", help="Support commands")

    add_parser = subparsers.add_parser("add", help="Add another expense")
    add_parser.add_argument("--description", type=str, required=True, help="Description of expense")
    add_parser.add_argument("--amount", type=float, required=True, help="Amount spent")

    update_parser = subparsers.add_parser("update", help="Update a expense")
    update_parser.add_argument("--id", type=int, required=True, help="The index in expense list")
    update_parser.add_argument("--description", type=str, required=True, help="Description of expense")
    update_parser.add_argument("--amount", type=float, required=True, help="Amount spent")

    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("--id", type=int, required=True, help="The index in expense list")

    args = parser.parse_args()

    if args.command == "add":
        new_expense = {
            "id": data["next_id"],
            "description": args.description,
            "amount": args.amount,
        }
        data["expenses"].append(new_expense)
        data["next_id"] += 1
        save_data(filename, data)
        print(f"Expense added successfully (ID: {new_expense["id"]})")
    elif args.command == "update":
        for exp in data["expenses"]:
            if exp["id"] == args.id:
                exp["description"] = args.description
                exp["amount"] = args.amount
                save_data(filename, data)
                print(f"Expense updated successfully (ID: {exp["id"]})")
    elif args.command == "delete":
        original_length = len(data["expenses"])
        data["expenses"] = [e for e in data["expenses"] if e["id"] != args.id]
        if len(data["expenses"]) < original_length:
            save_data(filename, data)
            print(f"Expense deleted successfully")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()