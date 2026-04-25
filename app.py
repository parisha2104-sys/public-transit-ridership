import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
import bcrypt

warnings.filterwarnings("ignore")

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Public Transit Ridership Forecasting",
    page_icon="🚌",
    layout="wide"
)

# ----------------------------
# LOGIN/REGISTER SYSTEM (TEMPORARY)
# ----------------------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "page" not in st.session_state:
    st.session_state.page = "login"


def register_page():
    st.title("📝 Register")

    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if username.strip() == "" or password.strip() == "":
            st.error("❌ Username and Password cannot be empty")
            return

        if password != confirm_password:
            st.error("❌ Passwords do not match")
            return

        if username in st.session_state.users:
            st.error("❌ Username already exists")
            return

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        st.session_state.users[username] = hashed_pw

        st.success("✅ Registration successful! Now login.")
        st.session_state.page = "login"
        st.rerun()

    if st.button("Already have an account? Login"):
        st.session_state.page = "login"
        st.rerun()


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


# ----------------------------
# MAIN DASHBOARD (YOUR ORIGINAL WEBSITE)
# ----------------------------
def dashboard():

    # ----------------------------
    # TITLE
    # ----------------------------
    st.title("🚌 Public Transit Ridership Forecasting & Analytics Dashboard")
    st.markdown("**Parisha • Rishika • Tanisha**")
    st.write("---")

    # Logout Button
    st.sidebar.success(f"👋 Welcome {st.session_state.current_user}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.session_state.page = "login"
        st.rerun()

    # ----------------------------
    # LOAD DATASET
    # ----------------------------
    @st.cache_data
    def load_data():
        df = pd.read_csv("public_transit_dataset_clean.csv")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
        return df

    df = load_data()

    # ----------------------------
    # ADD DUMMY COORDINATES (CHANDIGARH BASED)
    # ----------------------------
    @st.cache_data
    def generate_route_coordinates(df):
        route_ids = df["Route_ID"].unique()

        # Chandigarh city center coordinates
        base_lat = 30.7333
        base_lon = 76.7794

        coords = {}
        np.random.seed(42)

        for route in route_ids:
            coords[route] = (
                base_lat + np.random.uniform(-0.05, 0.05),
                base_lon + np.random.uniform(-0.05, 0.05)
            )

        return coords

    route_coords = generate_route_coordinates(df)

    df["Latitude"] = df["Route_ID"].map(lambda x: route_coords[x][0])
    df["Longitude"] = df["Route_ID"].map(lambda x: route_coords[x][1])

    # ----------------------------
    # SIDEBAR FILTERS
    # ----------------------------
    st.sidebar.header("🔍 Filters")

    route_filter = st.sidebar.selectbox("Select Route", ["All"] + sorted(df["Route_ID"].unique().tolist()))
    weather_filter = st.sidebar.selectbox("Select Weather", ["All"] + sorted(df["Weather"].unique().tolist()))
    weekend_filter = st.sidebar.selectbox("Weekend Filter", ["All", "Weekend Only", "Weekday Only"])
    holiday_filter = st.sidebar.selectbox("Holiday Filter", ["All", "Holiday Only", "Non-Holiday Only"])

    filtered_df = df.copy()

    if route_filter != "All":
        filtered_df = filtered_df[filtered_df["Route_ID"] == route_filter]

    if weather_filter != "All":
        filtered_df = filtered_df[filtered_df["Weather"] == weather_filter]

    if weekend_filter == "Weekend Only":
        filtered_df = filtered_df[filtered_df["Is_Weekend"] == 1]
    elif weekend_filter == "Weekday Only":
        filtered_df = filtered_df[filtered_df["Is_Weekend"] == 0]

    if holiday_filter == "Holiday Only":
        filtered_df = filtered_df[filtered_df["Is_Holiday"] == 1]
    elif holiday_filter == "Non-Holiday Only":
        filtered_df = filtered_df[filtered_df["Is_Holiday"] == 0]

    # ----------------------------
    # SIDEBAR NAVIGATION MENU
    # ----------------------------
    st.sidebar.header("📌 Navigation Menu")

    menu = st.sidebar.radio(
        "Choose Section",
        [
            "Dashboard",
            "Ridership Forecasting (ARIMA)",
            "Revenue Forecasting (ARIMA)",
            "Preferred Routes",
            "Peak Hour Analysis",
            "Weather Impact Analysis",
            "Weekend vs Weekday Analysis",
            "Festive/Holiday Analysis",
            "Interactive Route Map (Chandigarh)",
            "Route Query Assistant",
            "About"
        ]
    )

    # ----------------------------
    # DASHBOARD PAGE
    # ----------------------------
    if menu == "Dashboard":
        st.subheader("📊 Transit Dashboard Overview")

        total_passengers = filtered_df["Passengers"].sum()
        total_revenue = filtered_df["Revenue"].sum()

        avg_daily_passengers = filtered_df.groupby("Date")["Passengers"].sum().mean()

        if len(filtered_df) > 0:
            busiest_route = filtered_df.groupby("Route_ID")["Passengers"].sum().idxmax()
        else:
            busiest_route = "No Data"

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Passengers", f"{total_passengers:,.0f}")
        col2.metric("Total Revenue", f"₹ {total_revenue:,.0f}")
        col3.metric("Avg Daily Passengers", f"{avg_daily_passengers:,.0f}")
        col4.metric("Busiest Route", f"{busiest_route}")

        st.write("---")

        daily_trend = filtered_df.groupby("Date")["Passengers"].sum().reset_index()
        fig = px.line(daily_trend, x="Date", y="Passengers", title="Daily Ridership Trend")
        st.plotly_chart(fig, use_container_width=True)

        revenue_trend = filtered_df.groupby("Date")["Revenue"].sum().reset_index()
        fig2 = px.line(revenue_trend, x="Date", y="Revenue", title="Daily Revenue Trend")
        st.plotly_chart(fig2, use_container_width=True)

    # ----------------------------
    # RIDERSHIP FORECASTING (ARIMA)
    # ----------------------------
    elif menu == "Ridership Forecasting (ARIMA)":
        st.subheader("📈 Ridership Forecasting using ARIMA")

        daily_data = filtered_df.groupby("Date")["Passengers"].sum().reset_index()
        daily_data = daily_data.sort_values("Date")

        fig = px.line(daily_data, x="Date", y="Passengers", title="Actual Daily Ridership")
        st.plotly_chart(fig, use_container_width=True)

        forecast_days = st.slider("Select Forecast Days", 7, 90, 30)

        if len(daily_data) < 20:
            st.warning("⚠️ Not enough data for forecasting. Try selecting broader filters.")
        else:
            series = daily_data["Passengers"]

            train_size = int(len(series) * 0.8)
            train, test = series[:train_size], series[train_size:]

            model = ARIMA(train, order=(5, 1, 0))
            model_fit = model.fit()

            predictions = model_fit.forecast(steps=len(test))

            mae = mean_absolute_error(test, predictions)
            rmse = np.sqrt(mean_squared_error(test, predictions))

            st.success(f"Model Evaluation → MAE: {mae:.2f} | RMSE: {rmse:.2f}")

            future_forecast = model_fit.forecast(steps=forecast_days)

            future_dates = pd.date_range(start=daily_data["Date"].max(), periods=forecast_days + 1)[1:]
            forecast_df = pd.DataFrame({"Date": future_dates, "Forecast_Passengers": future_forecast})

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=daily_data["Date"], y=daily_data["Passengers"], mode="lines", name="Actual"))
            fig2.add_trace(go.Scatter(x=forecast_df["Date"], y=forecast_df["Forecast_Passengers"], mode="lines", name="Forecast"))

            fig2.update_layout(
                title="Ridership Forecast (ARIMA)",
                xaxis_title="Date",
                yaxis_title="Passengers"
            )

            st.plotly_chart(fig2, use_container_width=True)
            st.dataframe(forecast_df)

    # ----------------------------
    # REVENUE FORECASTING (ARIMA)
    # ----------------------------
    elif menu == "Revenue Forecasting (ARIMA)":
        st.subheader("💰 Revenue Forecasting using ARIMA")

        daily_revenue = filtered_df.groupby("Date")["Revenue"].sum().reset_index()
        daily_revenue = daily_revenue.sort_values("Date")

        fig = px.line(daily_revenue, x="Date", y="Revenue", title="Actual Daily Revenue")
        st.plotly_chart(fig, use_container_width=True)

        forecast_days = st.slider("Select Forecast Days", 7, 90, 30)

        if len(daily_revenue) < 20:
            st.warning("⚠️ Not enough data for forecasting. Try selecting broader filters.")
        else:
            series = daily_revenue["Revenue"]

            train_size = int(len(series) * 0.8)
            train, test = series[:train_size], series[train_size:]

            model = ARIMA(train, order=(5, 1, 0))
            model_fit = model.fit()

            predictions = model_fit.forecast(steps=len(test))

            mae = mean_absolute_error(test, predictions)
            rmse = np.sqrt(mean_squared_error(test, predictions))

            st.success(f"Model Evaluation → MAE: {mae:.2f} | RMSE: {rmse:.2f}")

            future_forecast = model_fit.forecast(steps=forecast_days)

            future_dates = pd.date_range(start=daily_revenue["Date"].max(), periods=forecast_days + 1)[1:]
            forecast_df = pd.DataFrame({"Date": future_dates, "Forecast_Revenue": future_forecast})

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=daily_revenue["Date"], y=daily_revenue["Revenue"], mode="lines", name="Actual"))
            fig2.add_trace(go.Scatter(x=forecast_df["Date"], y=forecast_df["Forecast_Revenue"], mode="lines", name="Forecast"))

            fig2.update_layout(
                title="Revenue Forecast (ARIMA)",
                xaxis_title="Date",
                yaxis_title="Revenue"
            )

            st.plotly_chart(fig2, use_container_width=True)
            st.dataframe(forecast_df)

    # ----------------------------
    # PREFERRED ROUTES
    # ----------------------------
    elif menu == "Preferred Routes":
        st.subheader("🛣️ Preferred Routes Recommendation")

        route_stats = filtered_df.groupby("Route_ID")[["Passengers", "Revenue"]].sum().reset_index()
        route_stats = route_stats.sort_values("Passengers", ascending=False)

        fig = px.bar(route_stats.head(10), x="Route_ID", y="Passengers", title="Top 10 Routes by Passenger Count")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(route_stats.head(10), x="Route_ID", y="Revenue", title="Top 10 Routes by Revenue")
        st.plotly_chart(fig2, use_container_width=True)

        st.write("### ✅ Recommended Routes to Increase Bus Frequency")
        st.dataframe(route_stats.head(5))

    # ----------------------------
    # PEAK HOUR ANALYSIS
    # ----------------------------
    elif menu == "Peak Hour Analysis":
        st.subheader("⏰ Peak Hour Demand Analysis")

        peak_stats = filtered_df.groupby("Peak_Hour")["Passengers"].sum().reset_index()

        fig = px.bar(peak_stats, x="Peak_Hour", y="Passengers", title="Passengers Distribution During Peak Hours")
        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # WEATHER IMPACT ANALYSIS
    # ----------------------------
    elif menu == "Weather Impact Analysis":
        st.subheader("🌦️ Weather-Based Ridership Analysis")

        weather_stats = filtered_df.groupby("Weather")[["Passengers", "Revenue"]].mean().reset_index()

        fig = px.bar(weather_stats, x="Weather", y="Passengers", title="Average Passengers by Weather Condition")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(weather_stats, x="Weather", y="Revenue", title="Average Revenue by Weather Condition")
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.scatter(filtered_df, x="Temperature", y="Passengers", title="Temperature vs Passengers")
        st.plotly_chart(fig3, use_container_width=True)

    # ----------------------------
    # WEEKEND VS WEEKDAY ANALYSIS
    # ----------------------------
    elif menu == "Weekend vs Weekday Analysis":
        st.subheader("📅 Weekend vs Weekday Ridership Analysis")

        weekend_stats = filtered_df.groupby("Is_Weekend")[["Passengers", "Revenue"]].mean().reset_index()
        weekend_stats["Is_Weekend"] = weekend_stats["Is_Weekend"].map({0: "Weekday", 1: "Weekend"})

        fig = px.bar(weekend_stats, x="Is_Weekend", y="Passengers", title="Avg Passengers: Weekday vs Weekend")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(weekend_stats, x="Is_Weekend", y="Revenue", title="Avg Revenue: Weekday vs Weekend")
        st.plotly_chart(fig2, use_container_width=True)

    # ----------------------------
    # FESTIVE/HOLIDAY ANALYSIS
    # ----------------------------
    elif menu == "Festive/Holiday Analysis":
        st.subheader("🎉 Festive Season / Holiday Impact Analysis")

        holiday_stats = filtered_df.groupby("Is_Holiday")[["Passengers", "Revenue"]].mean().reset_index()
        holiday_stats["Is_Holiday"] = holiday_stats["Is_Holiday"].map({0: "Normal Day", 1: "Holiday/Festive Day"})

        fig = px.bar(holiday_stats, x="Is_Holiday", y="Passengers", title="Avg Passengers: Holiday vs Normal Day")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(holiday_stats, x="Is_Holiday", y="Revenue", title="Avg Revenue: Holiday vs Normal Day")
        st.plotly_chart(fig2, use_container_width=True)

    # ----------------------------
    # INTERACTIVE ROUTE MAP
    # ----------------------------
    elif menu == "Interactive Route Map (Chandigarh)":
        st.subheader("🗺️ Interactive Route Map (Chandigarh City)")

        chandigarh_map = folium.Map(location=[30.7333, 76.7794], zoom_start=12)

        top_routes = filtered_df.groupby("Route_ID")["Passengers"].sum().reset_index()
        top_routes = top_routes.sort_values("Passengers", ascending=False).head(15)

        for _, row in top_routes.iterrows():
            route = row["Route_ID"]
            passengers = row["Passengers"]

            lat, lon = route_coords[route]

            folium.Marker(
                location=[lat, lon],
                popup=f"<b>Route:</b> {route}<br><b>Passengers:</b> {passengers}",
                tooltip=f"{route}"
            ).add_to(chandigarh_map)

        st_folium(chandigarh_map, width=1200, height=600)

    # ----------------------------
    # ROUTE QUERY ASSISTANT
    # ----------------------------
    elif menu == "Route Query Assistant":
        st.subheader("🤖 Route Query Assistant (AI Recommendation System)")

        st.write("Ask questions like:")
        st.info("""
        - Which route is most preferable?
        - Best route for weekends?
        - Best route during rainy weather?
        - Highest revenue route?
        - Most crowded route in holidays?
        """)

        user_query = st.text_input("Type your question:")

        if st.button("Get Recommendation"):
            if user_query.strip() == "":
                st.warning("⚠️ Please type a question first.")
            else:
                query = user_query.lower()
                temp_df = df.copy()

                if "weekend" in query:
                    temp_df = temp_df[temp_df["Is_Weekend"] == 1]

                if "weekday" in query:
                    temp_df = temp_df[temp_df["Is_Weekend"] == 0]

                if "holiday" in query or "festive" in query or "festival" in query:
                    temp_df = temp_df[temp_df["Is_Holiday"] == 1]

                if "rain" in query:
                    temp_df = temp_df[temp_df["Weather"].str.lower() == "rainy"]

                if "sun" in query:
                    temp_df = temp_df[temp_df["Weather"].str.lower() == "sunny"]

                if "cloud" in query:
                    temp_df = temp_df[temp_df["Weather"].str.lower() == "cloudy"]

                if temp_df.empty:
                    st.error("❌ No data found for this query. Try another question.")
                else:
                    if "revenue" in query or "profit" in query:
                        route_summary = temp_df.groupby("Route_ID")["Revenue"].sum().reset_index()
                        best_route = route_summary.sort_values("Revenue", ascending=False).iloc[0]

                        st.success(f"✅ Recommended Route: {best_route['Route_ID']}")
                        st.write(f"💰 Total Revenue: ₹ {best_route['Revenue']:,.0f}")

                        fig = px.bar(
                            route_summary.sort_values("Revenue", ascending=False).head(10),
                            x="Route_ID",
                            y="Revenue",
                            title="Top 10 Routes by Revenue"
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    else:
                        route_summary = temp_df.groupby("Route_ID")["Passengers"].sum().reset_index()
                        best_route = route_summary.sort_values("Passengers", ascending=False).iloc[0]

                        st.success(f"✅ Most Preferable Route: {best_route['Route_ID']}")
                        st.write(f"🧍 Total Passengers: {best_route['Passengers']:,.0f}")

                        fig = px.bar(
                            route_summary.sort_values("Passengers", ascending=False).head(10),
                            x="Route_ID",
                            y="Passengers",
                            title="Top 10 Routes by Ridership"
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    st.write("### Explanation")
                    st.info("The system analyzed transit demand patterns based on your question and recommended the highest performing route.")

    # ----------------------------
    # ABOUT PAGE
    # ----------------------------
    elif menu == "About":
        st.subheader("📌 About This Project")

        st.markdown("""
        ### 🚍 Public Transit Ridership Forecasting System  
        This project is designed to analyze and forecast public transit ridership patterns using AI & Machine Learning techniques.

        #### 🔥 Key Features:
        - Ridership Forecasting using ARIMA  
        - Revenue Trend Prediction  
        - Preferred Route Recommendation System  
        - Peak Hour Demand Analysis  
        - Weather Impact Analysis  
        - Weekend vs Weekday Analysis  
        - Festive/Holiday Ridership Analysis  
        - Interactive Route Map (Chandigarh)  
        - Route Query Assistant  

        #### 👩‍💻 Developed By:
        **Parisha • Rishika • Tanisha**
        """)

        st.success("Built using Streamlit, ARIMA Time-Series Forecasting, Plotly Graphs, and Folium Maps.")


# ----------------------------
# CONTROL FLOW
# ----------------------------
if st.session_state.logged_in:
    dashboard()
else:
    if st.session_state.page == "register":
        register_page()
    else:
        login_page()
