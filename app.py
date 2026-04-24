import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="Public Transit Ridership", layout="wide")


# ---------------- LOGIN SYSTEM ---------------- #

# Fixed users (password already hashed)
users = {
    "parisha": {
        "name": "Parisha",
        "password": "$2b$12$O8WjP7z6Z9QmW7VYgqO7FehYxW8iV9m7vJXgW4Xy7aYkW3aU3d3kC"
    },
    "admin": {
        "name": "Admin",
        "password": "$2b$12$Z1xJ9Jp0zVY8qZQf8aFZWee1bFqvGm5Rj9P8m7g8vWQf9fY8aKj2a"
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

    st.subheader("📌 Dataset Preview")
    st.dataframe(df)

    st.subheader("📊 Basic Analysis")
    st.write("Total Rows:", df.shape[0])
    st.write("Total Columns:", df.shape[1])

    st.subheader("📍 Column Names")
    st.write(df.columns)

    # ---------------- CHART SECTION ---------------- #
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(numeric_cols) > 0:
        st.subheader("📈 Graph Visualization")
        col = st.selectbox("Select column for graph", numeric_cols)
        st.line_chart(df[col])
    else:
        st.info("No numeric columns found for chart.")
