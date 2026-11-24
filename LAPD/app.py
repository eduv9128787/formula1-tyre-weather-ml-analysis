
# Import the libraries needed for our F1 dashboard
import streamlit as st
import pandas as pd

# Configure the browser tab and dashboard layout
st.set_page_config(
    page_title="LAPD | Formula 1 Analytics",
    page_icon="🏎️",
    layout="wide"
)

# Display the dashboard heading
st.title("🏎️ LAPD")
st.subheader("Lap Analysis & Prediction Dashboard")

# Explain the purpose of our application
st.write(
    "Explore Formula 1 lap-time performance using "
    "tyre characteristics, weather conditions, "
    "and machine learning."
)

# Display the seasons included in our research
st.info("Research dataset: 2023–2025 Formula 1 seasons")

# Confirm that the dashboard is running
st.success("LAPD is running successfully! 🏁")


# --------------------------------------------------
# SECTION 1: DATASET OVERVIEW
# --------------------------------------------------

# Load our cleaned Formula 1 research dataset
f1_data = pd.read_csv("f1_2023_2025_model_ready.csv")

st.header("📊 Formula 1 Dataset Overview")

# Create three columns for our dataset statistics
col1, col2, col3 = st.columns(3)

# Show the total number of lap records
col1.metric(
    "Total Laps",
    f"{len(f1_data):,}"
)

# Show the total number of races
col2.metric(
    "Total Races",
    f"{f1_data['session_key'].nunique():,}"
)

# Show the number of tyre compounds
col3.metric(
    "Tyre Compounds",
    f"{f1_data['compound'].nunique():,}"
)


# --------------------------------------------------
# SECTION 2: TYRE COMPOUND ANALYSIS
# --------------------------------------------------

st.header("🏎️ Tyre Compound Analysis")

# Count laps for each tyre compound
tyre_counts = f1_data["compound"].value_counts()

# Let users choose which compounds to display
selected_compounds = st.multiselect(
    "Select tyre compounds:",
    options=tyre_counts.index.tolist(),
    default=tyre_counts.index.tolist()
)

# Update the chart based on the selected compounds
if selected_compounds:
    st.bar_chart(tyre_counts.loc[selected_compounds])
else:
    st.info("Please select at least one tyre compound.")

# Explain what the chart represents
st.caption(
    "Number of recorded laps for each tyre compound "
    "in the 2023–2025 research dataset."
)


# --------------------------------------------------
# SECTION 3: LAP TIME BY TYRE COMPOUND
# --------------------------------------------------

st.header("⏱️ Lap Time by Tyre Compound")

# Calculate median lap duration for each compound
median_lap_times = (
    f1_data.groupby("compound")["lap_duration"]
    .median()
    .sort_values()
)

# Display the median lap-time comparison
st.bar_chart(median_lap_times)

# Explain the limitations of this comparison
st.caption(
    "Median lap duration in seconds for each tyre compound. "
    "Lower values indicate faster recorded laps. "
    "These are descriptive comparisons and do not control "
    "for circuit differences or racing conditions."
)


# --------------------------------------------------
# SECTION 4: RACE-SPECIFIC TYRE COMPARISON
# --------------------------------------------------

st.header("🏁 Race-Specific Tyre Comparison")

# Get the available race session identifiers
race_options = sorted(
    f1_data["session_key"].dropna().unique()
)

# Let users select a race
selected_race = st.selectbox(
    "Select a race session:",
    options=race_options
)

# Keep only laps from the selected race
selected_race_data = f1_data[
    f1_data["session_key"] == selected_race
]

# Calculate median lap times for each compound in this race
race_tyre_times = (
    selected_race_data.groupby("compound")["lap_duration"]
    .median()
    .sort_values()
)

# Display the race-specific chart
st.bar_chart(race_tyre_times)

# Explain the limitations of the comparison
st.caption(
    "Median lap duration in seconds for each tyre compound "
    "within the selected race. These comparisons are descriptive "
    "and do not control for driver differences, tyre age, "
    "race disruptions or changing weather."
)


# --------------------------------------------------
# SECTION 5: INTERACTIVE WEATHER ANALYSIS
# --------------------------------------------------

st.header("🌡️ Weather Conditions and Lap Times")

# Let users choose which weather variable to explore
selected_weather = st.selectbox(
    "Choose a weather variable:",
    [
        "Track Temperature",
        "Air Temperature",
        "Humidity",
        "Wind Speed"
    ]
)

# Match the displayed labels to the dataset columns
weather_columns = {
    "Track Temperature": "track_temperature",
    "Air Temperature": "air_temperature",
    "Humidity": "humidity",
    "Wind Speed": "wind_speed"
}

# Find the dataset column selected by the user
weather_column = weather_columns[selected_weather]

# Display the median value of the selected weather variable
st.metric(
    f"Median {selected_weather}",
    f"{f1_data[weather_column].median():.1f}"
)

# Keep records with valid weather values and lap times
weather_data = f1_data[
    [weather_column, "lap_duration"]
].dropna().copy()

# Set a suitable interval size for each weather variable
interval_sizes = {
    "track_temperature": 5,
    "air_temperature": 2,
    "humidity": 10,
    "wind_speed": 1
}

# Get the interval size for the selected variable
interval_size = interval_sizes[weather_column]

# Group weather measurements into intervals
weather_data["weather_range"] = (
    weather_data[weather_column] // interval_size
    * interval_size
)

# Calculate median lap duration for each weather interval
weather_lap_times = (
    weather_data.groupby("weather_range")["lap_duration"]
    .median()
    .sort_index()
)

# Display a chart that changes when the weather selection changes
st.line_chart(
    weather_lap_times,
    x_label=selected_weather,
    y_label="Median Lap Duration (seconds)"
)

# Explain the weather chart and its limitations
st.caption(
    f"Median lap duration across {selected_weather.lower()} "
    f"intervals. These are descriptive associations and do not "
    f"control for circuit differences or other racing conditions."
)

# --------------------------------------------------
# SECTION 6: MACHINE LEARNING MODEL PERFORMANCE
# --------------------------------------------------

st.header("🤖 Machine Learning Model Performance")

# Display the cross-validation results from our research
model_results = pd.DataFrame({
    "Model": [
        "Linear Regression (Tyres + Circuit)",
        "Gradient Boosting (Tyres + Circuit)",
        "Random Forest (Tyres + Circuit)",
        "Linear Regression (Tyres + Weather + Circuit)",
        "Gradient Boosting (Tyres + Weather + Circuit)"
    ],
    "Mean MAE (seconds)": [
        5.71,
        6.40,
        7.69,
        6.14,
        7.24
    ]
})

# Sort models from lowest prediction error to highest
model_results = model_results.sort_values(
    "Mean MAE (seconds)"
)

# Display the model comparison chart
st.bar_chart(
    model_results.set_index("Model")
)

# Explain how to interpret model performance
st.caption(
    "Mean Absolute Error (MAE) from race-grouped "
    "cross-validation. Lower values indicate better "
    "predictive accuracy. These are rounded research results."
)

# Highlight the best-performing model
st.success(
    "Best-performing model: Linear Regression "
    "(Tyres + Circuit), with a mean MAE of 5.71 seconds."
)

# --------------------------------------------------
# SECTION 7: LAP TIME PREDICTION
# --------------------------------------------------

# Import joblib to load our saved machine learning model
import joblib

# Add a heading for our prediction feature
st.header("🏎️ Formula 1 Lap Time Prediction")

# Load the Linear Regression model trained in Jupyter
lap_prediction_model = joblib.load(
    "lapd_prediction_model.joblib"
)

# Confirm that the trained model is ready to use
st.success("Machine learning prediction model loaded successfully! 🏁")


# Create the circuit column from the race name
# using the same circuit labels as our trained model
f1_data["circuit"] = (
    f1_data["race_name"]
    .str.replace(r"^\d{4}\s+", "", regex=True)
    .str.strip()
)

# Get the available circuits for the dropdown

# Use the exact circuit names from our trained machine learning model
# This ensures the dropdown matches the model's training data
circuit_options = [
    "Austin",
    "Baku",
    "Barcelona",
    "Budapest",
    "Imola",
    "Jeddah",
    "Las Vegas",
    "Lusail",
    "Marina Bay",
    "Melbourne",
    "Mexico City",
    "Miami Gardens",
    "Monaco",
    "Montréal",
    "Monza",
    "Sakhir",
    "Shanghai",
    "Silverstone",
    "Spa-Francorchamps",
    "Spielberg",
    "Suzuka",
    "São Paulo",
    "Yas Island",
    "Zandvoort"
]



selected_circuit = st.selectbox(
    "Select a circuit:",
    options=circuit_options
)

# Let users choose a tyre compound
compound_options = sorted(
    f1_data["compound"].dropna().unique()
)

selected_compound = st.selectbox(
    "Select a tyre compound for prediction:",
    options=compound_options
)

# Let users enter the number of laps on the tyre
selected_tyre_age = st.number_input(
    "Tyre age (laps):",
    min_value=0,
    max_value=100,
    value=5,
    step=1
)

# Explain what information the model uses
st.caption(
    "The prediction model uses circuit, tyre compound "
    "and estimated tyre age. Weather conditions are "
    "analysed separately and are not prediction inputs."
)

# --------------------------------------------------
# MAKE A LAP-TIME PREDICTION
# --------------------------------------------------

# Add a button that runs our trained machine learning model
if st.button("🏁 Predict Lap Time"):

    # Create one row containing the user's selected inputs
    prediction_inputs = pd.DataFrame({
        "circuit": [selected_circuit],
        "compound": [selected_compound],
        "tyre_age": [selected_tyre_age]
    })

    # Use our saved model to predict the lap duration
    predicted_lap_time = lap_prediction_model.predict(
        prediction_inputs
    )[0]
    
    # Convert the predicted lap time into minutes and seconds
    minutes = int(predicted_lap_time // 60)
    seconds = predicted_lap_time % 60

    # Display the prediction in Formula 1 lap-time format
    st.metric(
    "Predicted Lap Time",
    f"{minutes}:{seconds:05.2f}"
    )

    # Also show the original prediction in seconds
    st.caption(
        f"Equivalent to {predicted_lap_time:.2f} seconds."
    )


    # Explain what the prediction represents
    st.caption(
        "This is a model-estimated lap duration based on "
        "circuit, tyre compound and estimated tyre age. "
        "Actual lap times may differ due to driver performance, "
        "weather, traffic and race conditions."
    )

# --------------------------------------------------
# PREDICTION ACCURACY INFORMATION
# --------------------------------------------------

# Explain the model's measured cross-validation accuracy
st.info(
    "📊 Model accuracy: The selected Linear Regression model "
    "achieved a mean absolute error (MAE) of approximately "
    "5.71 seconds during race-grouped cross-validation. "
    "This describes average prediction error, not a guaranteed "
    "error margin for individual predictions."
)

# Explain the model's important limitations
st.caption(
    "Predictions are estimates based on historical 2023–2025 "
    "Formula 1 data. Accuracy may vary across circuits and "
    "racing conditions, especially for circuits not represented "
    "in a training fold."
)
