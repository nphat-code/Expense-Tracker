import argparse
import json
from datetime import datetime
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

    add_parser = subparsers.add_parser("add", help="Add an expense")
    add_parser.add_argument("--description", type=str, required=True, help="Description of expense")
    add_parser.add_argument("--amount", type=float, required=True, help="Amount spent")

    update_parser = subparsers.add_parser("update", help="Update an expense")
    update_parser.add_argument("--id", type=int, required=True, help="The index in expense list")
    update_parser.add_argument("--description", type=str, required=True, help="Description of expense")
    update_parser.add_argument("--amount", type=float, required=True, help="Amount spent")

    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("--id", type=int, required=True, help="The index in expense list")

    list_parser = subparsers.add_parser("list", help="View all expenses")

    sum_parser = subparsers.add_parser("summary", help="A summary of all expenses")
    sum_parser.add_argument("--month", type=int, help="for a specific month")

    args = parser.parse_args()

    if args.command == "add":
        new_expense = {
            "id": data["next_id"],
            "description": args.description,
            "amount": args.amount,
            "date": datetime.now().strftime("%Y-%m-%d")
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
    elif args.command == "list":
        if len(data["expenses"]) > 0:
            print(f"{"ID":7} {"Date":15} {"Description":15} {"Amount":10}")
            for exp in data["expenses"]:
                print(f"{str(exp["id"]):7} {exp["date"]:15} {exp["description"]:15} ${str(exp["amount"]):10}")
        else:
            print("The list is empty")
    elif args.command == "summary":
        months = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
        if args.month is None:
            total_expenses = 0
            for exp in data["expenses"]:
                total_expenses += exp["amount"]
            print(f"Total expenses: ${total_expenses}")
        else:

            total_expenses = 0
            for exp in data["expenses"]:
                if args.month == datetime.strptime(exp["date"], "%Y-%m-%d").month:
                    total_expenses += exp["amount"]
            print(f"Total expenses for {months[args.month]}: ${total_expenses}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()