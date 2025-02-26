import streamlit as st
import pandas as pd
from datetime import timedelta

# Streamlit App Title
st.title("CSV Date Formatter and Time Adjuster")

# User input for adding hours (before uploading the file)
hours_to_add = st.selectbox("Select number of hours to add (1-23):", range(1, 24))

# Upload CSV File
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the data
    df = pd.read_csv(uploaded_file)

    # Display the original data
    st.write("Original Data:")
    st.dataframe(df)

    # Convert 'Created' column to datetime and reformat
    df['Created'] = pd.to_datetime(df['Created'], format='%m/%d/%Y %I:%M%p')

    # Reformat the date without leading zeros in month and day
    df['Created'] = df['Created'].dt.strftime('%-m/%-d/%Y %-I:%M %p')  # Ensure no leading zeros in month, day, and hour

    # Create new column with added hours
    df['Created + Hours'] = pd.to_datetime(df['Created'], format='%m/%d/%Y %I:%M %p') + timedelta(hours=hours_to_add)
    df['Created + Hours'] = df['Created + Hours'].dt.strftime('%-I:%M %p')  # Ensure no leading zero in hours and remove seconds

    # Insert the new column at column 2
    df.insert(1, 'Created + Hours', df.pop('Created + Hours'))

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
