import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page title
st.title("Solar Pile Tolerance Measurement App")

# Initialize or load dataset
if "pile_data" not in st.session_state:
    st.session_state.pile_data = pd.DataFrame(columns=[
        "Pile ID", "Planned X (m)", "Planned Y (m)", "Planned Height (m)",
        "Installed X (m)", "Installed Y (m)", "Installed Height (m)",
        "X Deviation (m)", "Y Deviation (m)", "Height Deviation (m)", "Tolerance Status"
    ])

# User input section
st.header("Enter Pile Measurement Data")

pile_id = st.text_input("Pile ID")
planned_x = st.number_input("Planned X (m)", value=0.0, step=0.1)
planned_y = st.number_input("Planned Y (m)", value=0.0, step=0.1)
planned_height = st.number_input("Planned Height (m)", value=2.5, step=0.1)
installed_x = st.number_input("Installed X (m)", value=0.0, step=0.1)
installed_y = st.number_input("Installed Y (m)", value=0.0, step=0.1)
installed_height = st.number_input("Installed Height (m)", value=2.5, step=0.1)

if st.button("Add Measurement"):
    # Compute deviations
    x_deviation = installed_x - planned_x
    y_deviation = installed_y - planned_y
    height_deviation = installed_height - planned_height

    # Determine tolerance status
    tolerance_status = "In Tolerance"
    if abs(x_deviation) > 0.3 or abs(y_deviation) > 0.3 or abs(height_deviation) > 0.2:
        tolerance_status = "Out of Tolerance"

    # Append data
    new_entry = pd.DataFrame([{
        "Pile ID": pile_id,
        "Planned X (m)": planned_x,
        "Planned Y (m)": planned_y,
        "Planned Height (m)": planned_height,
        "Installed X (m)": installed_x,
        "Installed Y (m)": installed_y,
        "Installed Height (m)": installed_height,
        "X Deviation (m)": x_deviation,
        "Y Deviation (m)": y_deviation,
        "Height Deviation (m)": height_deviation,
        "Tolerance Status": tolerance_status
    }])

    st.session_state.pile_data = pd.concat([st.session_state.pile_data, new_entry], ignore_index=True)
    st.success("Pile measurement added successfully!")

# Display stored pile data
st.header("Pile Measurement Data")
st.dataframe(st.session_state.pile_data)

# Visualization
st.header("Deviation Analysis")

if not st.session_state.pile_data.empty:
    fig, ax = plt.subplots()
    color_map = st.session_state.pile_data["Tolerance Status"].apply(lambda x: "red" if x == "Out of Tolerance" else "green")
    
    ax.scatter(st.session_state.pile_data["Planned X (m)"], st.session_state.pile_data["Planned Y (m)"], color="blue", label="Planned Position", marker="o")
    ax.scatter(st.session_state.pile_data["Installed X (m)"], st.session_state.pile_data["Installed Y (m)"], color=color_map, label="Installed Position", marker="x")

    for i in range(len(st.session_state.pile_data)):
        ax.plot([st.session_state.pile_data.loc[i, "Planned X (m)"], st.session_state.pile_data.loc[i, "Installed X (m)"]],
                [st.session_state.pile_data.loc[i, "Planned Y (m)"], st.session_state.pile_data.loc[i, "Installed Y (m)"]],
                color="gray", linestyle="dotted")

    ax.set_xlabel("X Position (m)")
    ax.set_ylabel("Y Position (m)")
    ax.set_title("Planned vs Installed Solar Pile Positions")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Height deviation bar chart
    st.subheader("Height Deviation per Pile")
    fig2, ax2 = plt.subplots()
    ax2.bar(st.session_state.pile_data["Pile ID"], st.session_state.pile_data["Height Deviation (m)"], 
            color=["green" if abs(x) <= 0.2 else "red" for x in st.session_state.pile_data["Height Deviation (m)"]])
    ax2.axhline(y=0.2, color='gray', linestyle='dashed', label="Tolerance Limit (+0.2m)")
    ax2.axhline(y=-0.2, color='gray', linestyle='dashed', label="Tolerance Limit (-0.2m)")
    ax2.set_xlabel("Pile ID")
    ax2.set_ylabel("Height Deviation (m)")
    ax2.set_title("Height Deviation per Pile")
    ax2.legend()
    ax2.grid(axis="y")
    st.pyplot(fig2)

# Report Export
st.header("Download Report")
if st.button("Export Data as CSV"):
    csv_data = st.session_state.pile_data.to_csv(index=False).encode("utf-8")
    st.download_button(label="Download CSV", data=csv_data, file_name="solar_pile_tolerance_report.csv", mime="text/csv")
