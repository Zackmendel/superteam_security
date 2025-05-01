# summary.py
import streamlit as st
import pandas as pd
from collections import Counter
import re 
import plotly.express as px


def render_metric_box(label: str, value: str):
    st.markdown(
        f"""
        <div style="
            background-color: #424b43;
            border: 2px solid #111212;
            border-radius: 30px;
            padding: 30px 20px;
            color: white;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        ">
            <div style="
                font-size: 1.3em;
                color: #B7e493;
                margin-bottom: 10px;
                font-weight: 600;
                word-wrap: break-word;
            ">
                {label}
            </div>
            <div style="
                font-size: 3em;
                font-weight: 700;
                color: #ffffff;
                word-wrap: break-word;
            ">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Helper function to parse loss string to float value
# Adapted from home.py's severity calculation but returns a number
def parse_loss_value(loss_str):
    """Parses the loss string (e.g., '$326 M', '$661 K', '—') into a float value."""
    if not isinstance(loss_str, str):
        return 0.0
    # Standardize, remove '$', handle unicode space if present, handle '—'
    loss_str = loss_str.replace("$", "").replace(" ", "").replace(",", "").replace("—", "0").strip()
    value = 0.0
    try:
        if loss_str.endswith(" M"):
            value = float(loss_str.replace(" M", "")) * 1_000_000
        elif loss_str.endswith(" B"): # Handle Billions if necessary
             value = float(loss_str.replace(" B", "")) * 1_000_000_000
        elif loss_str.endswith(" K"): # Handle Thousands
            value = float(loss_str.replace(" K", "")) * 1_000
        elif loss_str != "0": # Handle plain numbers if any, ensure it's not just '0'
            value = float(loss_str)
        # If it's '0' or parsing failed, value remains 0.0
    except ValueError:
        # st.warning(f"Could not parse loss value: {loss_str}") # Optional warning
        value = 0.0 # Default to 0 if parsing fails
    return value

def display_summary(incident_data, display_metric_func):
    """
    Calculates and displays summary statistics for Solana security incidents.

    Args:
        incident_data (list): The list of incident dictionaries from home.py.
        display_metric_func (callable): The function from home.py to display styled metrics.
    """
    st.markdown("## Overall Statistics")

    if not incident_data:
        st.warning("No incident data available to summarize.")
        return

    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(incident_data)

    # --- Calculate Metrics ---
    total_incidents = len(df)

    # Calculate total loss
    df['Loss Value'] = df['Loss (approx.)'].apply(parse_loss_value)
    total_loss_usd = df['Loss Value'].sum()

    # Format total loss for display
    if total_loss_usd >= 1_000_000_000:
        formatted_loss = f"${total_loss_usd / 1_000_000_000:.2f} B"
    elif total_loss_usd >= 1_000_000:
        formatted_loss = f"${total_loss_usd / 1_000_000:.2f} M"
    elif total_loss_usd >= 1_000:
        formatted_loss = f"${total_loss_usd / 1_000:.2f} K"
    else:
        formatted_loss = f"${total_loss_usd:.2f}" # Display smaller amounts directly

    # Calculate average severity
    avg_severity = df['Severity Score'].mean() if 'Severity Score' in df.columns and not df.empty else 0

    # --- Display Metrics using the styled function from home.py ---
    col1, col2, col3 = st.columns(3)
    with col1:

        # Pass unique keys for each metric
        label1 = "Total Incidents"
        value1 = total_incidents
        render_metric_box(label1, value1)


    with col2:
        
        label1 = "Total Loss (Approx)"
        value1 = formatted_loss
        render_metric_box(label1, value1)


    with col3:

        label1 = "Average Severity"
        value1 = f"{avg_severity:.1f}"
        render_metric_box(label1, value1)
# --------------------------------------------------------------------------------------------------------------------
    st.markdown("---")

    # --- Incidents by Type ---
    st.markdown("## Incidents by Year, Month and Day")



    #  Read data into DataFrame
    csva = pd.read_csv("csv_files/summary/heat_map.csv")
    col_1, col_2 = st.columns(2, gap='large')
    with col_1:

        # Optional: enforce order of months
        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        csva["MONTH_NAME"] = pd.Categorical(csva["MONTH_NAME"], categories=month_order, ordered=True)

        # Filter records with positive incidence
        df_pos = csva[csva["INCIDENCE"] > 0]

        # Group and count
        heatmap_data = df_pos.groupby(["MONTH_NAME", "YEARS"]).size().reset_index(name='INCIDENT_COUNT')

        # Pivot for heatmap
        pivot_df = heatmap_data.pivot(index="MONTH_NAME", columns="YEARS", values="INCIDENT_COUNT").fillna(0)

        # Plotly heatmap
        fig = px.imshow(
            pivot_df,
            labels=dict(x="Year", y="Month", color="Incidence Count"),
            x=pivot_df.columns,
            y=pivot_df.index,
            text_auto=True,
            color_continuous_scale='Reds'
        )

        st.title("Incidence Heatmap")
        st.plotly_chart(fig)

    with col_2:


        # -----------------------------------------------------------------------------------------------------------------------

        # Group by DAY_NAME and sum the incidence
        bar_data = csva.groupby("DAY_NAME", as_index=False)["INCIDENCE"].sum()

        # Sort days logically
        day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        bar_data["DAY_NAME"] = pd.Categorical(bar_data["DAY_NAME"], categories=day_order, ordered=True)
        bar_data = bar_data.sort_values("DAY_NAME")

        # Create bar chart
        fig = px.bar(
            bar_data,
            x="DAY_NAME",
            y="INCIDENCE",
            color="DAY_NAME",
            labels={"DAY_NAME": "Day of Week", "INCIDENCE": "Total Incidence"},
            title="Total Incidence by Day of the Week"
        )

        # Streamlit display
        st.title("Incidences by Day")
        st.plotly_chart(fig)
    # -----------------------------------------------------------------------------------------------------------------------------
    st.markdown("---")


    csvb = pd.read_csv("csv_files/summary/incidence_loss.csv")

    col_1, col_2 = st.columns([2,1], gap='large')
    with col_1:

        # Create bar chart
        fig = px.bar(
            csvb,
            x="INCIDENT",
            y="LOSS_USD",
            color="INCIDENT",
            labels={"INCIDENT": "Incidence", "LOSS_USD": "Total Loss (USD)"},
            title="Loss by Incidence"
        )

        # Streamlit display
        st.title("Loss by Incidence")
        st.plotly_chart(fig)

    with col_2:

        # Filter for rows where there was an incident and a valid loss
        df_filtered = csva[(csva["INCIDENCE"] > 0) & (csva["LOSS_USD"] != "null")].copy()
        df_filtered["LOSS_USD"] = pd.to_numeric(df_filtered["LOSS_USD"])

        # Group by year and sum the losses
        loss_by_year = df_filtered.groupby("YEARS", as_index=False)["LOSS_USD"].sum()

        # Plot
        fig = px.bar(
            loss_by_year,
            x="YEARS",
            y="LOSS_USD",
            color="YEARS",
            labels={"YEARS": "Year", "LOSS_USD": "Total Loss (USD)"},
            title="Total Loss by Year"
        )

        st.plotly_chart(fig)


    # -----------------------------------------------------------------------------------------------------------------------------
    st.markdown("---")


    csvc = pd.read_csv("csv_files/summary/frequency.csv")

    col_1, col_2, col_3 = st.columns(3, gap='large')
    with col_1:

        # Create bar chart
        fig = px.bar(
            csvc,
            x="CATEGORY",
            y="INCIDENCE",
            color="CATEGORY",
            labels={"CATEGORY": "Category", "INCIDENCE": "Incidence"},
            title="Frequency of Exploit Category"
        )

        # Streamlit display
        st.plotly_chart(fig)

    with col_2:

        # Create bar chart
        fig1 = px.bar(
            csvc,
            x="CATEGORY",
            y="LOSS_USD",
            color="CATEGORY",
            labels={"CATEGORY": "Category", "INCIDENCE": "Incidence"},
            title="Loss by Category"
        )

        # Streamlit display
        st.plotly_chart(fig1)

    with col_3:

        # Create bar chart
        fig2 = px.bar(
            csvc,
            x="CATEGORY",
            y=["MAX_TIME_BTW_INC", "AVG_TIME_BTW_INC", "MIN_TIME_BTW_INC"],
            barmode='group',
            title="Max, Avg & Min Time Between Incidence"
        )

        # Streamlit display
        st.plotly_chart(fig2)




    # -----------------------------------------------------------------------------------------------------------------------------
    st.markdown("---")


    # --- Incidents by Type ---
    st.markdown("## Incidents by Type")
    if 'Type' in df.columns:
        type_counts = df['Type'].value_counts().reset_index()
        type_counts.columns = ['Incident Type', 'Count']

        col_chart, col_table = st.columns([1, 1]) # Display chart and table side-by-side
        with col_chart:
             st.markdown("##### Count by Type (Chart)")
             # Use Incident Type as index for the chart
             chart_data = type_counts.set_index('Incident Type')
             st.bar_chart(chart_data['Count'])
        with col_table:
             st.markdown("##### Count by Type (Table)")
             st.dataframe(type_counts, use_container_width=True, hide_index=True)
    else:
        st.info("Incident 'Type' data not available.")


    st.markdown("---")

    # --- Incidents by Tag ---
    st.markdown("## Incidents by Tag")
    if 'Tags' in df.columns:
        # Ensure tags are lists and handle potential non-list entries gracefully
        all_tags_list = [tag for tags in df['Tags'] if isinstance(tags, list) for tag in tags]
        if all_tags_list:
             tag_counts = Counter(all_tags_list)
             tag_counts_df = pd.DataFrame(tag_counts.items(), columns=['Tag', 'Count']).sort_values('Count', ascending=False)

             col_chart_tag, col_table_tag = st.columns([1, 1])
             with col_chart_tag:
                 st.markdown("##### Count by Tag (Top 15)")
                 # Limit chart to top N tags for readability
                 top_n = 15
                 chart_data_tag = tag_counts_df.head(top_n).set_index('Tag')
                 st.bar_chart(chart_data_tag['Count'])
             with col_table_tag:
                 st.markdown("##### Count by Tag (Table)")
                 st.dataframe(tag_counts_df, use_container_width=True, hide_index=True)
        else:
             st.info("No tags found in the incident data.")
    else:
        st.info("Incident 'Tags' data not available.")

    # --- (Optional) Loss Over Time ---
    st.markdown("---")
    st.markdown("## Loss Over Time (Approx.)")
    if 'Parsed Date' in df.columns and 'Loss Value' in df.columns:
         # Ensure dates are valid and sort
         df_time = df[['Parsed Date', 'Loss Value']].copy()
         # Ensure 'Parsed Date' is datetime
         df_time['Parsed Date'] = pd.to_datetime(df_time['Parsed Date'], errors='coerce')
         df_time = df_time.dropna(subset=['Parsed Date']) # Remove rows where date parsing failed
         df_time = df_time.sort_values('Parsed Date')

         if not df_time.empty:
             # Set date as index for charting
             df_time = df_time.set_index('Parsed Date')
             st.line_chart(df_time['Loss Value'])
         else:
             st.info("No valid date/loss data to plot.")
    else:
         st.info("Required 'Parsed Date' or 'Loss Value' columns not available for time series plot.")