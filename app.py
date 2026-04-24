import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# ---------------- LOGIN SYSTEM ---------------- #

st.set_page_config(page_title="Public Transit Ridership", layout="wide")

# Users list (register manually yaha add karna)
users = {
    "parisha": {
        "name": "Parisha",
        "password": stauth.Hasher(["12345"]).generate()[0]
    },
    "admin": {
        "name": "Admin",
        "password": stauth.Hasher(["admin123"]).generate()[0]
    }
}

credentials = {"usernames": users}

authenticator = stauth.Authenticate(
    credentials,
    "ridership_cookie",
    "random_key_12345",
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("❌ Wrong username or password")

if authentication_status == None:
    st.warning("⚠️ Please login to continue")

# ---------------- DASHBOARD AFTER LOGIN ---------------- #

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome {name} 👋")

    st.title("🚆 Public Transit Ridership Dashboard")

    # ---------------- LOAD CSV ---------------- #
    df = pd.read_csv("data.csv")

    st.subheader("Dataset Preview")
    st.dataframe(df)

    st.subheader("Basic Analysis")
    st.write("Total Rows:", df.shape[0])
    st.write("Total Columns:", df.shape[1])

    st.subheader("Column Names")
    st.write(df.columns)

    # Example chart if numeric column exists
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(numeric_cols) > 0:
        col = st.selectbox("Select column for graph", numeric_cols)
        st.line_chart(df[col])
    else:
        st.info("No numeric columns found for chart.")
