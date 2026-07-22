import io
import contextlib
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from database import initialize_database
from Helpers import (
    teachersearch, principalsearch, adminsearch,
    view_all_students, view_all_teachers,
)
from security import verify_password
from Teacher import Teacher
from Principal import Principal
from Admin import Admin, STUDENT_FIELDS

MAX_ATTEMPTS = 3

ROLES = {
    "Teacher": (teachersearch, lambda r: Teacher(r["full_name"], r["id"], r["department"])),
    "Principal": (principalsearch, lambda r: Principal(r["full_name"], r["id"])),
    "Admin": (adminsearch, lambda r: Admin(r["full_name"], r["id"])),
}
def capture(fn, *args, **kwargs):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*args, **kwargs)
    return buf.getvalue().strip()


def info_from(text, title="Result"):
    if text:
        messagebox.showinfo(title, text)


class FormDialog(simpledialog.Dialog):

    def __init__(self, parent, title, fields):
        self.fields = fields
        self.entries = {}
        self.result_values = None
        super().__init__(parent, title=title)

    def body(self, master):
        for i, (label, kind) in enumerate(self.fields):
            tk.Label(master, text=label + ":").grid(row=i, column=0, sticky="e", padx=5, pady=4)
            if isinstance(kind, list):
                var = tk.StringVar(value=kind[0])
                widget = ttk.Combobox(master, textvariable=var, values=kind, state="readonly")
                self.entries[label] = var
            else:
                widget = tk.Entry(master, show="*" if kind == "password" else "")
                self.entries[label] = widget
            widget.grid(row=i, column=1, padx=5, pady=4)
        return None

    def apply(self):
        values = {}
        for label, widget in self.entries.items():
            values[label] = widget.get() if isinstance(widget, tk.Entry) else widget.get()
        self.result_values = values

def ask_form(parent, title, fields):
    dlg = FormDialog(parent, title, fields)
    return dlg.result_values

class LoginFrame(ttk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, padding=30)
        self.on_success = on_success
        self.attempts_left = MAX_ATTEMPTS

        ttk.Label(self, text="School Record System", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 20)
        )

        ttk.Label(self, text="Role:").grid(row=1, column=0, sticky="e", pady=5)
        self.role_var = tk.StringVar(value="Teacher")
        role_box = ttk.Combobox(
            self, textvariable=self.role_var, values=list(ROLES.keys()), state="readonly"
        )
        role_box.grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(self, text="ID (4 digits):").grid(row=2, column=0, sticky="e", pady=5)
        self.id_entry = ttk.Entry(self)
        self.id_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self, text="Password:").grid(row=3, column=0, sticky="e", pady=5)
        self.pw_entry = ttk.Entry(self, show="*")
        self.pw_entry.grid(row=3, column=1, pady=5)
        self.pw_entry.bind("<Return>", lambda e: self.try_login())

        ttk.Button(self, text="Login", command=self.try_login).grid(
            row=4, column=0, columnspan=2, pady=15
        )

        self.status = ttk.Label(self, text="", foreground="red")
        self.status.grid(row=5, column=0, columnspan=2)

    def try_login(self):
        role_name = self.role_var.get()
        lookup, build_user = ROLES[role_name]

        id_input = self.id_entry.get().strip()
        if not (id_input.isdigit() and len(id_input) == 4):
            self.status.config(text="ID must be exactly 4 digits.")
            return
        user_id = int(id_input)

        record = lookup(user_id)
        if not record:
            self.status.config(text=f"No {role_name.lower()} found with ID {user_id}")
            return

        password = self.pw_entry.get()
        if verify_password(password, record["salt"], record["password_hash"]):
            self.on_success(build_user(record))
            return

        self.attempts_left -= 1
        if self.attempts_left <= 0:
            self.status.config(text="Too many failed attempts. Access denied.")
            self.id_entry.delete(0, tk.END)
            self.pw_entry.delete(0, tk.END)
            self.attempts_left = MAX_ATTEMPTS
        else:
            self.status.config(text=f"Incorrect password. {self.attempts_left} attempt(s) remaining.")
        self.pw_entry.delete(0, tk.END)


class DashboardFrame(ttk.Frame):
    STUDENT_COLS = ("id", "full_name", "grade", "score", "presence")
    TEACHER_COLS_ADMIN = ("id", "full_name", "department", "pay")
    TEACHER_COLS_PRINCIPAL = ("id", "full_name", "department")

    def __init__(self, master, user, on_logout):
        super().__init__(master, padding=10)
        self.user = user
        self.on_logout = on_logout

        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 10))
        ttk.Label(
            header,
            text=f"{self.user.position}: {self.user.full_name} (ID {self.user.id_number})",
            font=("Segoe UI", 13, "bold"),
        ).pack(side="left")
        ttk.Button(header, text="Logout", command=self.on_logout).pack(side="right")

        button_bar = ttk.Frame(self)
        button_bar.pack(fill="x", pady=(0, 10))
        self._build_buttons(button_bar)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.students_tree = self._make_tree(self.STUDENT_COLS)
        self.notebook.add(self.students_tree.master, text="Students")

        cols = self.TEACHER_COLS_ADMIN if isinstance(self.user, Admin) else self.TEACHER_COLS_PRINCIPAL
        self.teachers_tree = self._make_tree(cols)
        self.teachers_tab = self.teachers_tree.master
        self.notebook.add(self.teachers_tab, text="Teachers")

        self.refresh_students()
        if isinstance(self.user, Teacher):
            # Teacher isn't permitted to view the teacher list; show it so
            # they get the same denial the CLI menu would give them, then
            # remove the (empty) tab.
            info_from(capture(self.user.teacherlist), "View Teachers")
            self.notebook.forget(self.teachers_tab)
        else:
            self.refresh_teachers()

    def _make_tree(self, columns):
        wrapper = ttk.Frame(self.notebook)
        tree = ttk.Treeview(wrapper, columns=columns, show="headings")
        for c in columns:
            tree.heading(c, text=c.replace("_", " ").title())
            tree.column(c, width=120, anchor="center")
        vsb = ttk.Scrollbar(wrapper, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        return tree

    def refresh_students(self):
        self.students_tree.delete(*self.students_tree.get_children())
        for s in view_all_students():
            self.students_tree.insert("", "end", values=[s.get(c, "") for c in self.STUDENT_COLS])

    def refresh_teachers(self):
        cols = self.teachers_tree["columns"]
        self.teachers_tree.delete(*self.teachers_tree.get_children())
        for t in view_all_teachers():
            self.teachers_tree.insert("", "end", values=[t.get(c, "") for c in cols])

    def _build_buttons(self, bar):
        if isinstance(self.user, Teacher):
            ttk.Button(bar, text="Update Marks", command=self.update_marks).pack(side="left", padx=3)
            ttk.Button(bar, text="Update Attendance", command=self.update_attendance).pack(side="left", padx=3)
            ttk.Button(bar, text="Register Student", command=self.register_student_denied).pack(side="left", padx=3)
        elif isinstance(self.user, Principal):
            ttk.Button(bar, text="School Summary", command=self.summary).pack(side="left", padx=3)
            ttk.Button(bar, text="Register Student", command=self.register_student_denied).pack(side="left", padx=3)
            ttk.Button(bar, text="Set Pay", command=self.set_pay_denied).pack(side="left", padx=3)
        elif isinstance(self.user, Admin):
            ttk.Button(bar, text="Register Student", command=self.register_student).pack(side="left", padx=3)
            ttk.Button(bar, text="Modify Student", command=self.modify_student).pack(side="left", padx=3)
            ttk.Button(bar, text="Remove Student", command=self.remove_student).pack(side="left", padx=3)
            ttk.Button(bar, text="Register Teacher", command=self.register_teacher).pack(side="left", padx=3)
            ttk.Button(bar, text="Set Pay", command=self.set_pay).pack(side="left", padx=3)
            ttk.Button(bar, text="Remove Teacher", command=self.remove_teacher).pack(side="left", padx=3)

    def update_marks(self):
        values = ask_form(self, "Update Marks", [("Student ID", "text"), ("New Score", "text")])
        if not values:
            return
        try:
            sid, score = int(values["Student ID"]), int(values["New Score"])
        except ValueError:
            messagebox.showerror("Invalid input", "Student ID and score must be numbers.")
            return
        info_from(capture(self.user.update_marks, sid, score))
        self.refresh_students()

    def update_attendance(self):
        values = ask_form(self, "Update Attendance", [("Student ID", "text"), ("New Attendance %", "text")])
        if not values:
            return
        try:
            sid, presence = int(values["Student ID"]), int(values["New Attendance %"])
        except ValueError:
            messagebox.showerror("Invalid input", "Student ID and attendance must be numbers.")
            return
        info_from(capture(self.user.update_attendance, sid, presence))
        self.refresh_students()

    def register_student_denied(self):
        
        info_from(capture(self.user.register_student))

    def set_pay_denied(self):
        info_from(capture(self.user.set_pay))

    def summary(self):
        info_from(capture(self.user.summary), "School Summary")

    def register_student(self):
        values = ask_form(self, "Register Student", [
            ("Student ID", "text"), ("Full Name", "text"), ("Grade", "text"),
            ("Score", "text"), ("Presence", "text"),
        ])
        if not values:
            return
        try:
            sid = int(values["Student ID"])
            score = int(values["Score"]) if values["Score"] else 0
            presence = int(values["Presence"]) if values["Presence"] else 0
        except ValueError:
            messagebox.showerror("Invalid input", "ID, score, and presence must be numbers.")
            return
        info_from(capture(self.user.register_student, sid, values["Full Name"], values["Grade"], score, presence))
        self.refresh_students()

    def modify_student(self):
        values = ask_form(self, "Modify Student", [
            ("Student ID", "text"), ("Field", sorted(STUDENT_FIELDS)), ("New Value", "text"),
        ])
        if not values:
            return
        try:
            sid = int(values["Student ID"])
        except ValueError:
            messagebox.showerror("Invalid input", "Student ID must be a number.")
            return
        info_from(capture(self.user.modify_student, sid, values["Field"], values["New Value"]))
        self.refresh_students()

    def remove_student(self):
        values = ask_form(self, "Remove Student", [("Student ID", "text")])
        if not values:
            return
        try:
            sid = int(values["Student ID"])
        except ValueError:
            messagebox.showerror("Invalid input", "Student ID must be a number.")
            return
        info_from(capture(self.user.remove_student, sid))
        self.refresh_students()

    def register_teacher(self):
        values = ask_form(self, "Register Teacher", [
            ("Teacher ID", "text"), ("Full Name", "text"), ("Department", "text"),
            ("Pay", "text"), ("Password", "password"),
        ])
        if not values:
            return
        try:
            tid, pay = int(values["Teacher ID"]), int(values["Pay"])
        except ValueError:
            messagebox.showerror("Invalid input", "Teacher ID and pay must be numbers.")
            return
        info_from(capture(
            self.user.register_teacher, tid, values["Full Name"], values["Department"], pay, values["Password"]
        ))
        self.refresh_teachers()

    def set_pay(self):
        values = ask_form(self, "Set Pay", [("Teacher ID", "text"), ("New Pay", "text")])
        if not values:
            return
        try:
            tid, pay = int(values["Teacher ID"]), int(values["New Pay"])
        except ValueError:
            messagebox.showerror("Invalid input", "Teacher ID and pay must be numbers.")
            return
        info_from(capture(self.user.set_pay, tid, pay))
        self.refresh_teachers()

    def remove_teacher(self):
        values = ask_form(self, "Remove Teacher", [("Teacher ID", "text")])
        if not values:
            return
        try:
            tid = int(values["Teacher ID"])
        except ValueError:
            messagebox.showerror("Invalid input", "Teacher ID must be a number.")
            return
        info_from(capture(self.user.remove_teacher, tid))
        self.refresh_teachers()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("School Record System")
        self.geometry("780x520")
        self.minsize(650, 420)
        self.show_login()

    def show_login(self):
        for child in self.winfo_children():
            child.destroy()
        LoginFrame(self, self.show_dashboard).pack(fill="both", expand=True)

    def show_dashboard(self, user):
        for child in self.winfo_children():
            child.destroy()
        DashboardFrame(self, user, self.show_login).pack(fill="both", expand=True)


if __name__ == "__main__":
    initialize_database()
    App().mainloop()