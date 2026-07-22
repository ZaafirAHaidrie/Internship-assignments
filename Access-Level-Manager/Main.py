from database import initialize_database
from Auth import login
from Teacher import Teacher
from Principal import Principal
from Admin import Admin
from Menu import teachermenu, principalmenu, adminmenu


if __name__ == '__main__':
    initialize_database()
    user = login()
    if user:
        user.display()
        if isinstance(user, Teacher):
            teachermenu(user)
        elif isinstance(user, Principal):
            principalmenu(user)
        elif isinstance(user, Admin):
            adminmenu(user)