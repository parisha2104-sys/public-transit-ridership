import streamlit as st
import pandas as pd
import bcrypt

st.set_page_config(page_title="Public Transit Ridership", layout="wide")

# ---------------- USERS DATABASE (STATIC) ---------------- #
# Passwords hashed using bcrypt
users = {
    "parisha": bcrypt.hashpw("12345".encode(), bcrypt.gensalt()),
    "admin": bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
}

# ---------------- SESSION STATE ---------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------- LOGIN PAGE ---------------- #
if not st.session_state.logged_in:
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users:
            if bcrypt.checkpw(password.encode(), users[username]):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Wrong password")
        else:
            st.error("❌ Username not found")

    st.stop()

# ---------------- LOGOUT BUTTON ---------------- #
st.sidebar.success(f"Welcome {st.session_state.username} 👋")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# ---------------- DASHBOARD AFTER LOGIN ---------------- #
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
