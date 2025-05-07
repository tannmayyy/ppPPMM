import streamlit as st

# Mapping of display names to actual column names
column_mapping = {
    "date_ref": "trade_date",
    "amount_ref": "trade_amount",
    "id_ref": "trade_id"
}

# Sidebar selection
selected_display_column = st.sidebar.selectbox("Select a column", list(column_mapping.keys()))

# Get actual column name
actual_column_name = column_mapping[selected_display_column]

st.write(f"Selected Display Column: {selected_display_column}")
st.write(f"Mapped Backend Column: {actual_column_name}")