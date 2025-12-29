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

def add_expense(data, description, amount):
    new_expense = {
        "id": data["next_id"],
        "description": description,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    data["expenses"].append(new_expense)
    data["next_id"] += 1
    print(f"Expense added successfully (ID: {new_expense['id']})")

def update_expense(data, exp_id, description, amount):
    for exp in data["expenses"]:
        if exp["id"] == exp_id:
            exp["description"] = description
            exp["amount"] = amount
            print(f"Expense updated successfully (ID: {exp_id})")
            return True
    print(f"Error: Expense with ID {exp_id} not found.")
    return False

def delete_expense(data, exp_id):
    original_length = len(data["expenses"])
    data["expenses"] = [e for e in data["expenses"] if e["id"] != exp_id]
    if len(data["expenses"]) < original_length:
        print(f"Expense deleted successfully.")
        return True
    print(f"Error: Expense with ID {exp_id} not found.")
    return False

def list_expenses(data):
    if not data["expenses"]:
        print("The list is empty.")
        return
    
    print(f"{'ID':<7} {'Date':<15} {'Description':<20} {'Amount':<10}")
    print("-" * 52)
    for exp in data["expenses"]:
        print(f"{exp['id']:<7} {exp['date']:<15} {exp['description']:<20} ${exp['amount']:<10}")

def show_summary(data, month=None):
    months_map = {
        1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
        7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
    }
    
    total = 0
    if month:
        for exp in data["expenses"]:
            exp_month = datetime.strptime(exp["date"], "%Y-%m-%d").month
            if exp_month == month:
                total += exp["amount"]
        print(f"Total expenses for {months_map.get(month, 'Unknown')}: ${total}")
    else:
        total = sum(exp["amount"] for exp in data["expenses"])
        print(f"Total expenses: ${total}")


def main():
    filename = "expense-list.json"
    data = load_data(filename)
    
    parser = argparse.ArgumentParser(description="Expense Tracker Program")
    subparsers = parser.add_subparsers(dest="command", help="Support commands")

    add_p = subparsers.add_parser("add", help="Add an expense")
    add_p.add_argument("--description", type=str, required=True)
    add_p.add_argument("--amount", type=float, required=True)

    up_p = subparsers.add_parser("update", help="Update an expense")
    up_p.add_argument("--id", type=int, required=True)
    up_p.add_argument("--description", type=str, required=True)
    up_p.add_argument("--amount", type=float, required=True)

    del_p = subparsers.add_parser("delete", help="Delete an expense")
    del_p.add_argument("--id", type=int, required=True)

    subparsers.add_parser("list", help="View all expenses")

    sum_p = subparsers.add_parser("summary", help="Show total expenses")
    sum_p.add_argument("--month", type=int, help="Month (1-12)")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(data, args.description, args.amount)
        save_data(filename, data)
    elif args.command == "update":
        if update_expense(data, args.id, args.description, args.amount):
            save_data(filename, data)
    elif args.command == "delete":
        if delete_expense(data, args.id):
            save_data(filename, data)
    elif args.command == "list":
        list_expenses(data)
    elif args.command == "summary":
        show_summary(data, args.month)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()