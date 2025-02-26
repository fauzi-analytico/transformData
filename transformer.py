import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Streamlit App Title
st.title("CSV Date Formatter and Time Adjuster")

# User input for adding hours (before uploading the file)
hours_to_add = st.selectbox("Select number of hours to add (1-23):", range(1, 24))

# Upload CSV File
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the data
    df = pd.read_csv(uploaded_file, dtype=str)  # Read as string to prevent number conversion

    # Display the original data
    st.write("Original Data:")
    st.dataframe(df)

    # Convert 'Created' column to datetime
    df['Created'] = pd.to_datetime(df['Created'], format='%m/%d/%Y %I:%M%p')

    # Function to format date properly (removing leading zeros)
    def format_date(dt):
        hour_12 = dt.strftime("%I").lstrip("0")  # Convert to 12-hour format and remove leading zero
        minute = dt.strftime("%M")  # Keep minute as-is
        am_pm = dt.strftime("%p")  # Get AM/PM
        return f"{dt.month}/{dt.day}/{dt.year} {hour_12}:{minute} {am_pm}"

    # Apply formatting to 'Created'
    df['Created'] = df['Created'].apply(format_date)

    # Create new column with added hours
    df['Created + Hours'] = pd.to_datetime(df['Created'], format='%m/%d/%Y %I:%M %p') + timedelta(hours=hours_to_add)

    # Apply the same formatting function to the new column
    df['Created + Hours'] = df['Created + Hours'].apply(format_date)

    # Insert the new column at column 2
    df.insert(1, 'Created + Hours', df.pop('Created + Hours'))

    # Ensure 'Phone' and 'Secondary phone number' remain as text
    phone_columns = ['Phone', 'Secondary phone number']
    for col in phone_columns:
        if col in df.columns:
            df[col] = df[col].astype(str)  # Convert to string
            df[col] = df[col].apply(lambda x: f"'{x}" if x.isnumeric() else x)  # Add single quote to force text

    # Display the modified data
    st.write("Modified Data:")
    st.dataframe(df)

    # Download the modified CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Edited CSV",
        data=csv,
        file_name=uploaded_file.name.replace('.csv', '_edited.csv'),
        mime='text/csv',
    )
else:
    st.write("Please upload a CSV file to proceed.")
