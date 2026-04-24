import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

st.set_page_config(page_title="Public Transit Ridership", layout="wide")

# ---------------- LOGIN SYSTEM ---------------- #

names = ["Parisha", "Admin"]
usernames = ["parisha", "admin"]

# Passwords (plain)
passwords = ["12345", "admin123"]

# Convert to hashed passwords
hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "ridership_cookie",
    "random_key_12345",
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("❌ Wrong Username or Password")

if authentication_status == None:
    st.warning("⚠️ Please enter your username and password")

if authentication_status:

    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome {name} 👋")

    # ---------------- DASHBOARD ---------------- #

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
