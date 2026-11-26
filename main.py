import json
import string as st
import random
import datetime as dt
import streamlit as st_ui



# Original OOP/data structure preserved; Streamlit controls replace terminal input/print.*

class GlobalErrorHandler:

    @staticmethod

    def handle_error(error):

        return f"An error occurred: {str(error)}"


class student:

    data = []

    database = "students.json"

    try:

        with open(database, "r", encoding="utf-8") as s_data:

            data = json.loads(s_data.read())

    except (FileNotFoundError, json.decoder.JSONDecodeError):

        data = []



    @classmethod

    def update(cls):

        with open(cls.database, "w", encoding="utf-8") as stu_data:

            stu_data.write(json.dumps(cls.data, indent=4))

    @classmethod

    def randomid(cls):

        alpha = random.choices(st.ascii_uppercase, k=2)
        s_number = random.choices(st.digits, k=2)
        e_number = random.choices(st.digits, k=6)

        return "".join(s_number + alpha + e_number)



    @classmethod

    def facultyid(cls):

        alph = random.choices(st.ascii_uppercase, k=2)
        s_num = random.choices(st.digits, k=2)
        e_num = random.choices(st.digits, k=4)
        return "".join(s_num + alph + e_num)


stu = student()


def get_student(student_id):

    return next((item for item in stu.data if str(item.get("id", "")).strip() == str(student_id).strip()), None)


def show_details(item):

    st_ui.write(f"**Student ID:** {item.get('id', '')}")

    st_ui.write(f"**Name:** {item.get('name', '')}")

    st_ui.write(f"**Age:** {item.get('Age', '')}")

    st_ui.write(f"**Email:** {item.get('Email', '')}")
    st_ui.write(f"**Faculty ID :** {item.get('FacultyId', '')}")

    st_ui.write(f"**Contact:** +91 {item.get('Contact', '')}")




st_ui.set_page_config(page_title="Student Management System", page_icon="🎓", layout="wide")

st_ui.title("🎓 Student Management System")



# Home page: only login fields and button.*

if "logged_in" not in st_ui.session_state:

    st_ui.session_state.logged_in = False

if "current_user" not in st_ui.session_state:

    st_ui.session_state.current_user = None



if not st_ui.session_state.logged_in:

    login_tab, create_tab = st_ui.tabs(["Login", "Create Account"])



    with login_tab:

        st_ui.subheader("Login")

        with st_ui.form("login_form"):

            username = st_ui.text_input("UserName", key="login_username")

            password = st_ui.text_input("Password", type="password", key="login_password")

            submitted = st_ui.form_submit_button("Login", use_container_width=True)



        if submitted:

            matched = next(

                (item for item in stu.data

                 if str(item.get("UserName", "")).strip() == username.strip()

                 and str(item.get("Password", "")).strip() == password.strip()),

                None

            )

            if matched:

                st_ui.session_state.logged_in = True

                st_ui.session_state.current_user = matched

                st_ui.rerun()

            else:

                st_ui.error("Invalid username or password.")



    with create_tab:

        st_ui.subheader("Create Account")

        with st_ui.form("create_account_form"):

            create_name = st_ui.text_input("Full Name")

            create_age = st_ui.number_input("Age", min_value=1, max_value=120, value=18)

            create_email = st_ui.text_input("Email")

            create_contact = st_ui.text_input("Contact Number")

            create_gender = st_ui.selectbox("Gender", ["MALE", "FEMALE", "OTHER"])

            create_occupation = st_ui.text_input("Occupation")

            create_username = st_ui.text_input("Create UserName")

            create_password = st_ui.text_input("Create Password", type="password")

            confirm_password = st_ui.text_input("Confirm Password", type="password")

            create_submitted = st_ui.form_submit_button("Create Account", use_container_width=True)



        if create_submitted:

            if not all([create_name.strip(), create_email.strip(), create_contact.strip(),

                        create_username.strip(), create_password]):

                st_ui.error("Please fill all required fields.")

            elif any(str(item.get("UserName", "")).strip() == create_username.strip()

                     for item in stu.data):

                st_ui.error("This username already exists. Please choose another.")

            elif create_password != confirm_password:

                st_ui.error("Password and confirm password do not match.")

            else:

                new_student = {

                    "id": stu.randomid(),

                    "name": create_name.strip(),

                    "Age": int(create_age),

                    "Email": create_email.strip(),

                    "Contact": create_contact.strip(),

                    "FacultyId": stu.facultyid(),

                    "Gender": create_gender,

                    "Occupation": create_occupation.strip(),

                    "UserName": create_username.strip(),

                    "Password": create_password

                }

                stu.data.append(new_student)

                stu.update()

                st_ui.success(f"Account created successfully!\nStudent ID: {new_student['id']}\nFaculty ID: {new_student['FacultyId']}")

                st_ui.info("Ab Login tab par jaakar apne username aur password se login karein.")



    st_ui.stop()



current_user = st_ui.session_state.current_user

st_ui.success(f"Logged in as {current_user.get('name', '')}")

with st_ui.sidebar:

    st_ui.subheader("Menu")

    page = st_ui.radio(

        "Choose an option",

        ["My Details", "Student Registration", "Update Student", "Delete Student",

         "View Students", "Search Student", "Assign Grade", "Calculate Average",

         "Sort Marks", "Logout"],

    )



if page == "My Details":

    st_ui.subheader("Your Current Details")

    show_details(current_user)



elif page == "Student Registration":

    st_ui.subheader("Student Registration")

    with st_ui.form("registration_form"):

        name = st_ui.text_input("Name")

        age = st_ui.number_input("Age", min_value=1, max_value=120, step=1)

        email = st_ui.text_input("Email")

        contact = st_ui.text_input("Contact Number")

        gender = st_ui.selectbox("Gender", ["MALE", "FEMALE", "OTHER"])

        occupation = st_ui.text_input("Occupation")

        new_username = st_ui.text_input("Create UserName")

        new_password = st_ui.text_input("Create Password", type="password")

        register = st_ui.form_submit_button("Register")

    if register:

        if not all([name.strip(), email.strip(), contact.strip(), new_username.strip(), new_password]):

            st_ui.error("Please fill all required fields.")

        elif any(x.get("UserName") == new_username.strip() for x in stu.data):

            st_ui.error("This username already exists.")

        else:

            new_student = {

                "id": stu.randomid(), "name": name.strip(), "Age": int(age),

                "Email": email.strip(), "Contact": contact.strip(),

                "FacultyId": stu.facultyid(), "Gender": gender,

                "Occupation": occupation.strip(), "UserName": new_username.strip(),

                "Password": new_password

            }

            stu.data.append(new_student)

            stu.update()

            st_ui.success(f"Registration successful!\nStudent ID: {new_student['id']}\nFaculty ID: {new_student['FacultyId']}")



elif page == "Update Student":

    st_ui.subheader("Update Student Details")

    sid = st_ui.text_input("Student ID", key="update_id")

    item = get_student(sid) if sid else None

    if sid and not item:

        st_ui.error("Student ID not found.")

    if item:

        with st_ui.form("update_form"):

            new_name = st_ui.text_input("Name", value=item.get("name", ""))

            new_age = st_ui.number_input("Age", min_value=1, max_value=120, value=int(item.get("Age", 18)))

            new_email = st_ui.text_input("Email", value=item.get("Email", ""))

            new_contact = st_ui.text_input("Contact", value=item.get("Contact", ""))

            save = st_ui.form_submit_button("Save Changes")

        if save:

            item.update({"name": new_name.strip(), "Age": int(new_age),

                         "Email": new_email.strip(), "Contact": new_contact.strip()})

            stu.update()

            st_ui.success("Student details updated.")



elif page == "Delete Student":
    st_ui.subheader("Delete My Account")
    st_ui.write(f"Logged-in Student: {current_user.get('name', '')}")

    entered_id = st_ui.text_input("Enter your own Student ID", key="delete_own_student_id")
    confirm_delete = st_ui.checkbox(
        "I confirm that I want to delete my own account.",
        key="confirm_delete_own_account"
    )

    if st_ui.button("Delete My Account", type="primary", disabled=not confirm_delete):
        own_id = str(current_user.get("id", "")).strip()

        if not entered_id.strip():
            st_ui.error("Please enter your Student ID.")
        elif entered_id.strip() != own_id:
            st_ui.error("You can delete only your own account. Student ID does not match.")
        else:
            own_record = get_student(own_id)
            if own_record is None:
                st_ui.error("Your account was not found.")
            else:
                stu.data.remove(own_record)
                stu.update()
                st_ui.session_state.logged_in = False
                st_ui.session_state.current_user = None
                st_ui.success("Your account has been deleted.")
                st_ui.rerun()

elif page == "View Students":

    st_ui.subheader("All Student Details")

    if stu.data:

        st_ui.dataframe(

            [{"Name": x.get("name"), "Age": x.get("Age"),

              "Email": x.get("Email"), "Contact": x.get("Contact")} for x in stu.data],

            use_container_width=True

        )

        st_ui.caption(f"Total Students: {len(stu.data)}")

    else:

        st_ui.info("No students registered yet.")



elif page == "Search Student":

    st_ui.subheader("Search Student")

    sid = st_ui.text_input("Enter Student ID", key="search_id")

    if sid:

        item = get_student(sid)

        if item:

            show_details(item)



            if "Mark" in item and item["Mark"]:

                st_ui.subheader("Marks Details")

                st_ui.dataframe(

                    [{"Subject": subject, "Marks": marks}

                     for subject, marks in item["Mark"].items()],

                    use_container_width=True

                )

                if "Total_Marks" in item:

                    st_ui.metric("Total Marks", f"{item['Total_Marks']}/500")

                if "Grade" in item:

                    st_ui.metric("Grade", item["Grade"])

            else:

                st_ui.info("Marks are not available for this student yet.")

        else:

            st_ui.error("Student ID not found.")



elif page == "Assign Grade":

    st_ui.subheader("Assign Grade")

    faculty_id = st_ui.text_input("Faculty ID")

    target_id = st_ui.text_input("Student ID")

    target = get_student(target_id) if target_id else None

    if st_ui.button("Verify Faculty and Student"):

        faculty = next((x for x in stu.data if str(x.get("FacultyId", "")) == faculty_id.strip()), None)

        if not faculty:

            st_ui.error("Invalid Faculty ID.")

        elif not target:

            st_ui.error("Student ID not found.")

        else:

            st_ui.session_state.grade_faculty_verified = True

            st_ui.session_state.grade_target_id = target_id.strip()

            st_ui.success(f"Verified. Assign marks for {target.get('name', '')}.")

    if st_ui.session_state.get("grade_faculty_verified"):

        target = get_student(st_ui.session_state.grade_target_id)

        if target:

            with st_ui.form("grade_form"):

                subjects = ["Math", "Chemistry", "Physics", "Science", "English"]

                marks = {subject: st_ui.number_input(subject, min_value=0, max_value=100, step=1)

                         for subject in subjects}

                save_marks = st_ui.form_submit_button("Save Marks")

            if save_marks:

                total = sum(marks.values())

                if total >= 450:

                    grade = "A+"

                elif total >= 400:

                    grade = "B"

                elif total >= 300:

                    grade = "C"

                elif total >= 250:

                    grade = "D"

                else:

                    grade = "F"

                target["Mark"] = {k: int(v) for k, v in marks.items()}

                target["Total_Marks"] = int(total)

                target["Grade"] = grade

                stu.update()

                st_ui.success(f"Marks saved. Total: {total}/500 | Grade: {grade}")

                st_ui.session_state.grade_faculty_verified = False



elif page == "Calculate Average":

    st_ui.subheader("Calculate Average")

    sid = st_ui.text_input("Student ID", key="average_id")

    if sid:

        item = get_student(sid)

        if not item:

            st_ui.error("Student ID not found.")

        elif "Mark" not in item:

            st_ui.warning("Marks have not been assigned yet.")

        else:

            total = sum(item["Mark"].values())

            average = total / len(item["Mark"])

            st_ui.metric("Total Marks", f"{total}/500")

            st_ui.metric("Average", f"{average:.2f}")



elif page == "Sort Marks":

    st_ui.subheader("Sort Marks")

    sid = st_ui.text_input("Student ID", key="sort_id")

    if sid:

        item = get_student(sid)

        if not item:

            st_ui.error("Student ID not found.")

        elif "Mark" not in item:

            st_ui.warning("Marks have not been assigned yet.")

        else:

            sorted_marks = dict(sorted(item["Mark"].items(), key=lambda x: x[1], reverse=True))

            st_ui.dataframe([{"Subject": k, "Marks": v} for k, v in sorted_marks.items()],

                            use_container_width=True)



elif page == "Logout":

    st_ui.session_state.logged_in = False

    st_ui.session_state.current_user = None

    st_ui.rerun()
