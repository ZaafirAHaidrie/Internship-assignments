from Helpers import teachersearch, principalsearch, adminsearch
from Teacher import Teacher
from Principal import Principal
from Admin import Admin
from security import verify_password

MAX_ATTEMPTS = 3


def _get_password():
    return input("Enter your password: ")


def login():
    print("Who is viewing?")
    print("1. Teacher")
    print("2. Principal")
    print("3. Admin")
    choice = input("Enter choice (1-3): ")

    if choice == "1":
        role_name, lookup = "Teacher", teachersearch
        build_user = lambda record: Teacher(record["full_name"], record["id"], record["department"])
    elif choice == "2":
        role_name, lookup = "Principal", principalsearch
        build_user = lambda record: Principal(record["full_name"], record["id"])
    elif choice == "3":
        role_name, lookup = "Admin", adminsearch
        build_user = lambda record: Admin(record["full_name"], record["id"])
    else:
        print("Invalid choice")
        return None

    id_input = input(f"Enter your 4-digit {role_name} ID: ").strip()
    if not (id_input.isdigit() and len(id_input) == 4):
        print("ID must be exactly 4 digits.")
        return None
    user_id = int(id_input)

    record = lookup(user_id)
    if not record:
        print(f"No {role_name.lower()} found with ID {user_id}")
        return None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        password = _get_password()
        if verify_password(password, record["salt"], record["password_hash"]):
            return build_user(record)
        remaining = MAX_ATTEMPTS - attempt
        if remaining > 0:
            print(f"Incorrect password. {remaining} attempt(s) remaining.")

    print("Too many failed attempts. Access denied.")
    return None