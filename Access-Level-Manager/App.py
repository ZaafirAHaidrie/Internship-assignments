import pandas as pd
import streamlit as st

from database import initialize_database, create_connection
from security import verify_password, hash_password
from Helpers import (
    studentsearch,
    teachersearch,
    principalsearch,
    adminsearch,
    view_all_students,
    view_all_teachers,
)
STUDENT_FIELDS = {"full_name", "grade", "score", "presence"}
st.set_page_config(page_title="School Record System", layout="wide")

@st.cache_resource
def _init_db():
    initialize_database()
    return True
_init_db()

def register_student(student_id, full_name, grade, score, presence):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (id, full_name, grade, score, presence) VALUES (?, ?, ?, ?, ?)",
        (student_id, full_name, grade, score, presence),
    )
    conn.commit()
    conn.close()


def modify_student(student_id, field, value):
    student = studentsearch(student_id)
    if student and field in STUDENT_FIELDS:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(f"UPDATE students SET {field} = ? WHERE id = ?", (value, student_id))
        conn.commit()
        conn.close()
        return True, student
    return False, student

def remove_student(student_id):
    student = studentsearch(student_id)
    if student:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()
        return True, student
    return False, student

def update_marks(student_id, score):
    student = studentsearch(student_id)
    if student:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("UPDATE students SET score = ? WHERE id = ?", (score, student_id))
        conn.commit()
        conn.close()
    return student


def update_attendance(student_id, presence):
    student = studentsearch(student_id)
    if student:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("UPDATE students SET presence = ? WHERE id = ?", (presence, student_id))
        conn.commit()
        conn.close()
    return student

def register_teacher(teacher_id, full_name, department, pay, password):
    salt, pwd_hash = hash_password(password)
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO teachers (id, full_name, department, pay, salt, password_hash) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (teacher_id, full_name, department, pay, salt, pwd_hash),
    )
    conn.commit()
    conn.close()

def set_pay(teacher_id, pay):
    teacher = teachersearch(teacher_id)
    if teacher:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("UPDATE teachers SET pay = ? WHERE id = ?", (pay, teacher_id))
        conn.commit()
        conn.close()
    return teacher

def remove_teacher(teacher_id):
    teacher = teachersearch(teacher_id)
    if teacher:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM teachers WHERE id = ?", (teacher_id,))
        conn.commit()
        conn.close()
    return teacher


def students_df():
    students = view_all_students()
    return pd.DataFrame(students) if students else pd.DataFrame(
        columns=["id", "full_name", "grade", "score", "presence"]
    )

def teachers_df():
    teachers = view_all_teachers()
    return pd.DataFrame(teachers) if teachers else pd.DataFrame(
        columns=["id", "full_name", "department", "pay"]
    )
ROLE_LOOKUP = {
    "Teacher": teachersearch,
    "Principal": principalsearch,
    "Admin": adminsearch,
}
def login_screen():
    st.title("School Record System")
    st.subheader("Sign in")

    role = st.selectbox("Who is viewing?", ["Teacher", "Principal", "Admin"])
    user_id = st.text_input("4-digit ID", max_chars=4)
    password = st.text_input("Password", type="password")

    if st.button("Login", type="primary"):
        if not (user_id.isdigit() and len(user_id) == 4):
            st.error("ID must be exactly 4 digits.")
            return

        record = ROLE_LOOKUP[role](int(user_id))
        if not record:
            st.error(f"No {role.lower()} found with ID {user_id}")
            return

        if verify_password(password, record["salt"], record["password_hash"]):
            st.session_state.user = {
                "role": role,
                "id": record["id"],
                "full_name": record["full_name"],
                "department": record.get("department"),
            }
            st.rerun()
        else:
            st.error("Incorrect password.")

    st.caption("Made by Zaafir Abbas Haidrie")


def logout_button():
    with st.sidebar:
        user = st.session_state.user
        st.markdown(f"**{user['role']}**: {user['full_name']}  \nID: {user['id']}")
        if user.get("department"):
            st.markdown(f"Department: {user['department']}")
        if st.button("Log out"):
            del st.session_state.user
            st.rerun()


def teacher_dashboard(user):
    st.title(f"Teacher Dashboard — {user['full_name']}")
    tabs = st.tabs(["View Students", "Update Marks", "Update Attendance", "Register Student"])

    with tabs[0]:
        st.subheader(f"Students ({user['department']} class)")
        st.dataframe(students_df(), use_container_width=True, hide_index=True)

    with tabs[1]:
        st.subheader("Update Marks")
        sid = st.number_input("Student ID", min_value=1, step=1, key="marks_id")
        score = st.number_input("New score", min_value=0, max_value=100, step=1, key="marks_score")
        if st.button("Update score"):
            student = update_marks(int(sid), int(score))
            if student:
                st.success(f"Updated score for {student['full_name']} to {score}.")
            else:
                st.error(f"No student found with ID {int(sid)}.")

    with tabs[2]:
        st.subheader("Update Attendance")
        sid = st.number_input("Student ID", min_value=1, step=1, key="att_id")
        presence = st.number_input("New attendance %", min_value=0, max_value=100, step=1, key="att_presence")
        if st.button("Update attendance"):
            student = update_attendance(int(sid), int(presence))
            if student:
                st.success(f"Updated attendance for {student['full_name']} to {presence}%.")
            else:
                st.error(f"No student found with ID {int(sid)}.")

    with tabs[3]:
        st.subheader("Register Student")
        st.info("Teachers are not permitted to register students.")


def principal_dashboard(user):
    st.title(f"Principal Dashboard — {user['full_name']}")
    tabs = st.tabs(["View Students", "View Teachers", "School Summary", "Register Student", "Set Pay"])

    with tabs[0]:
        st.subheader("Students")
        st.dataframe(students_df(), use_container_width=True, hide_index=True)

    with tabs[1]:
        st.subheader("Teachers")
        st.dataframe(teachers_df(), use_container_width=True, hide_index=True)

    with tabs[2]:
        st.subheader("School Summary")
        df = students_df()
        t_df = teachers_df()
        if not df.empty:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Students", len(df))
            c2.metric("Teachers", len(t_df))
            c3.metric("Average Score", f"{df['score'].mean():.1f}")
            c4.metric("Average Attendance", f"{df['presence'].mean():.1f}%")

            st.markdown("#### Average score & attendance by grade")
            by_grade = df.groupby("grade")[["score", "presence"]].mean()
            st.bar_chart(by_grade)
        else:
            st.info("No student data yet.")

    with tabs[3]:
        st.subheader("Register Student")
        st.info("Principals are not permitted to register students.")

    with tabs[4]:
        st.subheader("Set Pay")
        st.info("Principals are not permitted to change staff pay.")


def admin_dashboard(user):
    st.title(f"Admin Dashboard — {user['full_name']}")
    tabs = st.tabs(
        [
            "View Students",
            "View Teachers",
            "Register Student",
            "Modify Student",
            "Remove Student",
            "Register Teacher",
            "Set Pay",
            "Remove Teacher",
        ]
    )
    with tabs[0]:
        st.subheader("Students")
        st.dataframe(students_df(), use_container_width=True, hide_index=True)

    with tabs[1]:
        st.subheader("Teachers")
        st.dataframe(teachers_df(), use_container_width=True, hide_index=True)

    with tabs[2]:
        st.subheader("Register Student")
        sid = st.number_input("New student ID", min_value=1, step=1, key="reg_id")
        full_name = st.text_input("Full name", key="reg_name")
        grade = st.text_input("Grade", key="reg_grade")
        score = st.number_input("Score", min_value=0, max_value=100, step=1, key="reg_score")
        presence = st.number_input("Presence %", min_value=0, max_value=100, step=1, key="reg_presence")
        if st.button("Register student"):
            if studentsearch(int(sid)):
                st.error(f"A student with ID {int(sid)} already exists.")
            elif not full_name:
                st.error("Full name is required.")
            else:
                register_student(int(sid), full_name, grade, int(score), int(presence))
                st.success(f"Registered student {full_name} with ID {int(sid)}")
                st.rerun()

    with tabs[3]:
        st.subheader("Modify Student")
        sid = st.number_input("Student ID", min_value=1, step=1, key="mod_id")
        field = st.selectbox("Field to update", sorted(STUDENT_FIELDS), key="mod_field")
        value = st.text_input("New value", key="mod_value")
        if st.button("Update student"):
            ok, student = modify_student(int(sid), field, value)
            if ok:
                st.success(f"Updated {field} for {student['full_name']} to {value}")
                st.rerun()
            else:
                st.error("Update failed")

    with tabs[4]:
        st.subheader("Remove Student")
        sid = st.number_input("Student ID", min_value=1, step=1, key="rm_id")
        if st.button("Remove student"):
            ok, student = remove_student(int(sid))
            if ok:
                st.success(f"Removed student {student['full_name']} with ID {int(sid)}")
                st.rerun()
            else:
                st.error("Removal failed")

    with tabs[5]:
        st.subheader("Register Teacher")
        tid = st.number_input("New teacher ID", min_value=1, step=1, key="regt_id")
        full_name = st.text_input("Full name", key="regt_name")
        department = st.text_input("Department", key="regt_dept")
        pay = st.number_input("Pay", min_value=0, step=1000, key="regt_pay")
        password = st.text_input("Set a password for this teacher", type="password", key="regt_pass")
        if st.button("Register teacher"):
            if teachersearch(int(tid)):
                st.error(f"A teacher with ID {int(tid)} already exists.")
            elif not full_name or not password:
                st.error("Full name and password are required.")
            else:
                register_teacher(int(tid), full_name, department, int(pay), password)
                st.success(f"Registered teacher {full_name} with ID {int(tid)}")
                st.rerun()

    with tabs[6]:
        st.subheader("Set Pay")
        tid = st.number_input("Teacher ID", min_value=1, step=1, key="pay_id")
        pay = st.number_input("New pay", min_value=0, step=1000, key="pay_value")
        if st.button("Update pay"):
            teacher = set_pay(int(tid), int(pay))
            if teacher:
                st.success(f"Updated pay for {teacher['full_name']} to {pay}")
                st.rerun()
            else:
                st.error("Update failed")

    with tabs[7]:
        st.subheader("Remove Teacher")
        tid = st.number_input("Teacher ID", min_value=1, step=1, key="rmt_id")
        if st.button("Remove teacher"):
            teacher = remove_teacher(int(tid))
            if teacher:
                st.success(f"Removed teacher {teacher['full_name']} with ID {int(tid)}")
                st.rerun()
            else:
                st.error("Removal failed")

def main():
    if "user" not in st.session_state:
        login_screen()
        return

    logout_button()
    user = st.session_state.user
    if user["role"] == "Teacher":
        teacher_dashboard(user)
    elif user["role"] == "Principal":
        principal_dashboard(user)
    elif user["role"] == "Admin":
        admin_dashboard(user)


if __name__ == "__main__":
    main()