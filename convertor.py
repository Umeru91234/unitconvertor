import streamlit as st
import requests

# Conversion Functions
def convert_length(value, from_unit, to_unit):
    units = {"Meters": 1, "Kilometers": 0.001, "Miles": 0.000621371, "Feet": 3.28084, "Centimeters": 100, "Inches": 39.3701, "Yards": 1.09361}
    return value * (units[to_unit] / units[from_unit])

def convert_weight(value, from_unit, to_unit):
    units = {"Kilograms": 1, "Pounds": 2.20462, "Ounces": 35.274, "Grams": 1000, "Tons": 0.001}
    return value * (units[to_unit] / units[from_unit])

def convert_temperature(value, from_unit, to_unit):
    if from_unit == "Celsius":
        return value * 9/5 + 32 if to_unit == "Fahrenheit" else value + 273.15
    elif from_unit == "Fahrenheit":
        return (value - 32) * 5/9 if to_unit == "Celsius" else ((value - 32) * 5/9) + 273.15
    elif from_unit == "Kelvin":
        return value - 273.15 if to_unit == "Celsius" else (value - 273.15) * 9/5 + 32
    return value

def convert_currency(value, from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url).json()
    rates = response.get("rates", {})
    return value * rates.get(to_currency, 1)

def convert_time(value, from_unit, to_unit):
    units = {"Seconds": 1, "Minutes": 1/60, "Hours": 1/3600, "Days": 1/86400}
    return value * (units[to_unit] / units[from_unit])

# Streamlit UI with Animated Sidebar
st.set_page_config(page_title="Unit Converter", layout="centered")

# Custom CSS for Sidebar Animation
st.markdown(
    """
    <style>
        .sidebar .sidebar-content {
            background: linear-gradient(45deg, #6a11cb, #2575fc);
            color: white;
            padding: 10px;
            transition: 0.5s;
        }
        .sidebar .sidebar-content:hover {
            box-shadow: 0px 0px 20px rgba(255, 255, 255, 0.8);
        }
        .stRadio > label {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation
st.sidebar.title("Unit Converter")
category = st.sidebar.radio("Select Conversion Type", ["Length", "Weight", "Temperature", "Currency", "Time"])

# Conversion Logic
st.title(f"{category} Converter")

value = st.number_input("Enter value", min_value=0.0, format="%.2f")

if category == "Length":
    units = ["Meters", "Kilometers", "Miles", "Feet", "Centimeters", "Inches", "Yards"]
    convert_function = convert_length
elif category == "Weight":
    units = ["Kilograms", "Pounds", "Ounces", "Grams", "Tons"]
    convert_function = convert_weight
elif category == "Temperature":
    units = ["Celsius", "Fahrenheit", "Kelvin"]
    convert_function = convert_temperature
elif category == "Currency":
    units = ["USD", "EUR", "GBP", "INR", "JPY", "CAD", "AUD"]
    convert_function = convert_currency
elif category == "Time":
    units = ["Seconds", "Minutes", "Hours", "Days"]
    convert_function = convert_time

from_unit = st.selectbox("From", units)
to_unit = st.selectbox("To", units)

if st.button("Convert"):
    result = convert_function(value, from_unit, to_unit)
    st.success(f"Converted Value: {result:.4f} {to_unit}")
