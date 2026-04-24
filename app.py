import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import bcrypt

st.set_page_config(page_title="Public Transit Ridership", layout="wide")


# ------------------ SESSION STORAGE ------------------ #
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "page" not in st.session_state:
    st.session_state.page = "login"


# ------------------ REGISTER PAGE ------------------ #
def register_page():
    st.title("📝 Register")

    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if username == "" or password == "":
            st.error("❌ Username/password cannot be empty")
            return

        if password != confirm:
            st.error("❌ Passwords do not match")
            return

        if username in st.session_state.users:
            st.error("❌ Username already exists")
            return

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        st.session_state.users[username] = hashed_pw

        st.success("✅ Registered successfully! Now login.")
        st.session_state.page = "login"
        st.rerun()

    if st.button("Already have account? Login"):
        st.session_state.page = "login"
        st.rerun()


# ------------------ LOGIN PAGE ------------------ #
def login_page():
    st.title("🔐 Login")

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
            st.error("❌ User not found. Please register first.")

    if st.button("New user? Register"):
        st.session_state.page = "register"
        st.rerun()


# ------------------ SIMPLE QUERY BOT ------------------ #
def query_bot(df, question):
    q = question.lower()

    if "columns" in q or "features" in q:
        return f"Columns are: {', '.join(df.columns)}"

    if "rows" in q or "records" in q:
        return f"Total rows in dataset: {df.shape[0]}"

    if "mean" in q or "average" in q:
        nums = df.select_dtypes(include=[np.number])
        if nums.shape[1] == 0:
            return "No numeric column found."
        return f"Mean values:\n{nums.mean().to_string()}"

    if "max" in q:
        nums = df.select_dtypes(include=[np.number])
        if nums.shape[1] == 0:
            return "No numeric column found."
        return f"Max values:\n{nums.max().to_string()}"

    if "min" in q:
        nums = df.select_dtypes(include=[np.number])
        if nums.shape[1] == 0:
            return "No numeric column found."
        return f"Min values:\n{nums.min().to_string()}"

    if "describe" in q or "summary" in q:
        return str(df.describe(include="all"))

    return "❓ Sorry, I can answer only dataset-related questions like rows, columns, mean, min, max, summary."


# ------------------ DASHBOARD ------------------ #
def dashboard():
    st.sidebar.success(f"👋 Welcome {st.session_state.current_user}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.session_state.page = "login"
        st.rerun()

    st.title("🚆 Public Transit Ridership Dashboard")

    # Load CSV
    df = pd.read_csv("data.csv")

    st.subheader("📌 Dataset Preview")
    st.dataframe(df, use_container_width=True)

    # Sidebar Filters
    st.sidebar.header("🔍 Filters")

    filtered_df = df.copy()

    # Filter for categorical columns
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if len(cat_cols) > 0:
        selected_cat = st.sidebar.selectbox("Select Categorical Column", ["None"] + cat_cols)

        if selected_cat != "None":
            values = df[selected_cat].dropna().unique().tolist()
            selected_values = st.sidebar.multiselect(f"Select values for {selected_cat}", values)

            if selected_values:
                filtered_df = filtered_df[filtered_df[selected_cat].isin(selected_values)]

    # Filter for numeric column
    if len(num_cols) > 0:
        selected_num = st.sidebar.selectbox("Select Numeric Column", ["None"] + num_cols)

        if selected_num != "None":
            min_val = float(df[selected_num].min())
            max_val = float(df[selected_num].max())

            range_val = st.sidebar.slider(
                f"Select range for {selected_num}",
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val)
            )

            filtered_df = filtered_df[
                (filtered_df[selected_num] >= range_val[0]) &
                (filtered_df[selected_num] <= range_val[1])
            ]

    st.subheader("✅ Filtered Data")
    st.write("Rows after filtering:", filtered_df.shape[0])
    st.dataframe(filtered_df, use_container_width=True)

    # Download filtered dataset
    st.download_button(
        "⬇️ Download Filtered CSV",
        filtered_df.to_csv(index=False),
        file_name="filtered_data.csv",
        mime="text/csv"
    )

    # Charts section
    st.subheader("📊 Charts & Visualizations")

    if len(num_cols) > 0:
        chart_col = st.selectbox("Select Numeric Column for Chart", num_cols)

        chart_type = st.selectbox("Select Chart Type", ["Line Chart", "Bar Chart", "Histogram"])

        fig, ax = plt.subplots()

        if chart_type == "Line Chart":
            ax.plot(filtered_df[chart_col].values)
            ax.set_title(f"Line Chart of {chart_col}")

        elif chart_type == "Bar Chart":
            ax.bar(range(len(filtered_df[chart_col].values)), filtered_df[chart_col].values)
            ax.set_title(f"Bar Chart of {chart_col}")

        elif chart_type == "Histogram":
            ax.hist(filtered_df[chart_col].dropna(), bins=20)
            ax.set_title(f"Histogram of {chart_col}")

        st.pyplot(fig)

    else:
        st.info("No numeric columns available for charts.")

    # Query Bot
    st.subheader("🤖 Query Bot (Ask Questions about Dataset)")

    question = st.text_input("Ask something like: rows?, columns?, mean?, max?, summary?")

    if st.button("Ask Bot"):
        if question.strip() == "":
            st.warning("Please type a question.")
        else:
            answer = query_bot(filtered_df, question)
            st.success(answer)


# ------------------ MAIN CONTROL ------------------ #
if st.session_state.logged_in:
    dashboard()
else:
    if st.session_state.page == "register":
        register_page()
    else:
        login_page()
