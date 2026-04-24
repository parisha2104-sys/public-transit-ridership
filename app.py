import streamlit as st
import pandas as pd
import bcrypt

st.set_page_config(page_title="Public Transit Ridership", layout="wide")

# ---------------- SESSION DATABASE ---------------- #
if "users" not in st.session_state:
    st.session_state.users = {}   # {"username": hashed_password}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "page" not in st.session_state:
    st.session_state.page = "Login"


# ---------------- REGISTER PAGE ---------------- #
def register_page():
    st.title("📝 Register Page")

    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if username == "" or password == "":
            st.error("❌ Username aur Password empty nahi ho sakta")
            return

        if password != confirm_password:
            st.error("❌ Password match nahi kar raha")
            return

        if username in st.session_state.users:
            st.error("❌ Username already exists")
            return

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        st.session_state.users[username] = hashed_pw

        st.success("✅ Registration successful! Ab login karo.")
        st.session_state.page = "Login"
        st.rerun()

    if st.button("Already have account? Login"):
        st.session_state.page = "Login"
        st.rerun()


# ---------------- LOGIN PAGE ---------------- #
def login_page():
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users:
            if bcrypt.checkpw(password.encode(), st.session_state.users[username]):
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Wrong password")
        else:
            st.error("❌ Username not found, register first!")

    if st.button("New user? Register"):
        st.session_state.page = "Register"
        st.rerun()


# ---------------- DASHBOARD ---------------- #
def dashboard_page():
    st.sidebar.success(f"Welcome {st.session_state.current_user} 👋")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.session_state.page = "Login"
        st.rerun()

    st.title("🚆 Public Transit Ridership Dashboard")

    df = pd.read_csv("data.csv")

    st.subheader("📌 Dataset Preview")
    st.dataframe(df)

    st.subheader("📊 Basic Analysis")
    st.write("Total Rows:", df.shape[0])
    st.write("Total Columns:", df.shape[1])

    st.subheader("📍 Column Names")
    st.write(df.columns)

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(numeric_cols) > 0:
        st.subheader("📈 Graph Visualization")
        col = st.selectbox("Select column for graph", numeric_cols)
        st.line_chart(df[col])
    else:
        st.info("No numeric columns found for chart.")


# ---------------- MAIN CONTROL ---------------- #
if st.session_state.logged_in:
    dashboard_page()
else:
    if st.session_state.page == "Register":
        register_page()
    else:
        login_page()
