import random
import os

# In-memory database
users = {"admin": "password123"}
trains = [
    {"train_no": 12626, "name": "Kerala Express", "from": "NDLS", "to": "TVC", "base_fare": 500, "coaches": {"AC": 2, "SL": 5, "GEN": 10}},
    {"train_no": 12952, "name": "Mumbai Rajdhani", "from": "NDLS", "to": "MMCT", "base_fare": 1200, "coaches": {"AC": 4, "SL": 2, "GEN": 0}},
    {"train_no": 12002, "name": "Bhopal Shatabdi", "from": "NDLS", "to": "BPL", "base_fare": 400, "coaches": {"AC": 6, "SL": 0, "GEN": 8}}
]
bookings = [] 
logged_in_user = None

def validate_pnr(pnr_str):
    """Checks if the entered PNR string is correctly formatted."""
    if len(pnr_str) != 10:
        print("\n[Validation Error]: A valid PNR must be exactly 10 digits long.")
        return False
    if not pnr_str.isdigit():
        print("\n[Validation Error]: PNR must contain numeric digits only.")
        return False
    return True

def register():
    print("\n--- User Registration ---")
    username = input("Enter username: ").strip()
    if username in users:
        print("Username already exists!")
        return
    password = input("Enter password: ").strip()
    if username and password:
        users[username] = password
        print("Registration successful!")
    else:
        print("Fields cannot be empty.")

def login():
    global logged_in_user
    print("\n--- User Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if username in users and users[username] == password:
        logged_in_user = username
        print(f"Welcome, {username}!")
        return True
    print("Invalid credentials!")
    return False

def view_trains():
    print("\n--- Available Trains ---")
    print(f"{'Train No':<10} {'Train Name':<20} {'From':<6} {'To':<6} {'AC':<5} {'SL':<5} {'GEN':<5} {'Base Fare':<10}")
    print("-" * 75)
    for t in trains:
        print(f"{t['train_no']:<10} {t['name']:<20} {t['from']:<6} {t['to']:<6} {t['coaches']['AC']:<5} {t['coaches']['SL']:<5} {t['coaches']['GEN']:<5} Rs.{t['base_fare']}")

def calculate_fare(base_fare, coach):
    multipliers = {"AC": 2.5, "SL": 1.2, "GEN": 0.8}
    return int(base_fare * multipliers[coach])

def book_ticket():
    if not logged_in_user:
        print("Please log in first to continue."); return
    view_trains()
    try:
        t_no = int(input("\nEnter Train Number: "))
    except ValueError:
        print("Invalid input format!"); return

    train = next((t for t in trains if t["train_no"] == t_no), None)
    if not train:
        print("Train route not found!"); return

    coach = input("Enter Coach Type (AC / SL / GEN): ").strip().upper()
    if coach not in train["coaches"]:
        print("Invalid coach assignment or option not configured for this train."); return
    
    available_seats = train["coaches"][coach]
    status = "CONFIRMED"
    berth = "N/A"
    
    if available_seats <= 0:
        status = random.choice(["RAC", "WL"])
        print(f"No vacant seats left in {coach}. Ticket booking route queued as: Status [{status}]")
    else:
        if coach in ["AC", "SL"]:
            print("Select Berth Preference: 1. Lower  2. Middle  3. Upper  4. Side Upper")
            b_choice = input("Enter preference (1-4): ").strip()
            berth_map = {"1": "LOWER", "2": "MIDDLE", "3": "UPPER", "4": "SIDE UPPER"}
            berth = berth_map.get(b_choice, "LOWER")
        else:
            berth = "GENERAL SEAT"

    p_name = input("Passenger Full Name: ").strip()
    p_age = input("Passenger Age: ").strip()
    if not p_name or not p_age:
        print("Passenger details cannot be empty!"); return

    if status == "CONFIRMED":
        train["coaches"][coach] -= 1

    pnr = random.randint(1000000000, 9999999999)
    fare = calculate_fare(train["base_fare"], coach)
    
    ticket = {
        "pnr": pnr, "username": logged_in_user, "train_no": t_no, "train_name": train["name"],
        "passenger": p_name, "age": p_age, "coach": coach, "berth": berth, "fare": fare, "status": status
    }
    bookings.append(ticket)
    print(f"\n Booking Created! PNR: {pnr} | Status: {status} | Berth: {berth} | Fare: Rs.{fare}")

def check_pnr_status():
    print("\n--- PNR Live Status Inquiry ---")
    pnr_input = input("Enter 10-digit PNR Number: ").strip()
    
    if not validate_pnr(pnr_input):
        return

    pnr_num = int(pnr_input)
    ticket = next((b for b in bookings if b["pnr"] == pnr_num), None)
    if not ticket:
        print("PNR record not found.")
        return

    print("-" * 50)
    print(f"PNR Ref: {ticket['pnr']} | Passenger: {ticket['passenger']} ({ticket['age']}Y)")
    print(f"Train Identifier: {ticket['train_name']} ({ticket['train_no']})")
    print(f"Allocated Coach: {ticket['coach']} | Berth: {ticket['berth']}")
    print(f"Current Verified Status: {ticket['status']}")
    print("-" * 50)

def cancel_ticket():
    if not logged_in_user:
        print("Please log in first to continue."); return
    
    pnr_input = input("\nEnter the 10-digit PNR to cancel: ").strip()
    if not validate_pnr(pnr_input):
        return

    pnr_num = int(pnr_input)
    ticket = next((b for b in bookings if b["pnr"] == pnr_num and b["username"] == logged_in_user), None)
    if not ticket:
        print("No active ticket record found with that PNR for your account."); return

    if ticket["status"] == "CANCELLED":
        print("This ticket has already been cancelled."); return

    if ticket["status"] == "CONFIRMED":
        train = next((t for t in trains if t["train_no"] == ticket["train_no"]), None)
        if train:
            train["coaches"][ticket["coach"]] += 1

    ticket["status"] = "CANCELLED"
    ticket["berth"] = "CANCELLED"
    print(f"Ticket with PNR {pnr_num} successfully cancelled. Full refund initiated.")

def prepare_chart():
    print("\n--- Chart Preparation Engine ---")
    try:
        t_no = int(input("Enter Train Number to process charts: "))
    except ValueError:
        print("Invalid format!"); return

    train = next((t for t in trains if t["train_no"] == t_no), None)
    if not train:
        print("Target train mapping reference not found!"); return

    chart_lines = []
    chart_lines.append(f"=======================================================")
    chart_lines.append(f"       OFFICIAL RESERVATION CHART: {train['name'].upper()} ({t_no})   ")
    chart_lines.append(f"=======================================================")
    chart_lines.append(f"{'PNR Number':<14} {'Passenger Name':<18} {'Coach':<7} {'Berth':<12} {'Final Status':<12}")
    chart_lines.append("-" * 68)
    
    train_bookings = [b for b in bookings if b["train_no"] == t_no]
    if not train_bookings:
        chart_lines.append("         No system passenger manifests for this voyage.        ")
    else:
        for b in train_bookings:
            if b["status"] in ["WL", "RAC"] and train["coaches"][b["coach"]] > 0:
                b["status"] = "CONFIRMED"
                b["berth"] = "LOWER" 
                train["coaches"][b["coach"]] -= 1
            chart_lines.append(f"{b['pnr']:<14} {b['passenger']:<18} {b['coach']:<7} {b['berth']:<12} {b['status']:<12}")
    chart_lines.append("=======================================================\n")

    chart_output = "\n".join(chart_lines)
    print(chart_output)

    # Safe File Exporter using macOS explicit home directory rules
    filename = f"train_{t_no}_reservation_chart.txt"
    home_dir = os.path.expanduser("~") 
    safe_filepath = os.path.join(home_dir, "Downloads", filename)

    try:
        with open(safe_filepath, "w") as file:
            file.write(chart_output)
        print(f"\n Success: File safely exported to: {safe_filepath}")
    except Exception as e:
        print(f"\n[File System Notification]: Console chart complete. File skip profile triggered ({e})")

def main_menu():
    global logged_in_user
    while True:
        print("\n==================================")
        print("    IRCTC PORTAL MANAGEMENT       ")
        print("==================================")
        if logged_in_user:
            print(f"System Session: Active ({logged_in_user})")
            print("1. View Available Trains\n2. Book a Ticket\n3. Cancel a Ticket\n4. Check PNR Status\n5. Chart Preparation Engine\n6. Terminate Session (Logout)\n7. Exit Terminal")
        else:
            print("1. Account Authentication (Login)\n2. Setup Profile (Register)\n3. View Available Trains\n4. Check PNR Status\n5. Exit Terminal")
        
        choice = input("\nEnter routing selection index: ").strip()
        if logged_in_user:
            if choice == "1": view_trains()
            elif choice == "2": book_ticket()
            elif choice == "3": cancel_ticket()
            elif choice == "4": check_pnr_status()
            elif choice == "5": prepare_chart()
            elif choice == "6": logged_in_user = None; print("Session scrubbed. Logged out cleanly.")
            elif choice == "7": print("Execution routine halted. Goodbye!"); break
            else: print("Error code: Option reference index invalid.")
        else:
            if choice == "1": login()
            elif choice == "2": register()
            elif choice == "3": view_trains()
            elif choice == "4": check_pnr_status()
            elif choice == "5": print("Execution routine halted. Goodbye!"); break
            else: print("Error code: Option reference index invalid.")

if __name__ == "__main__":
    main_menu()
