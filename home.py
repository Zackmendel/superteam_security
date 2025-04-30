import streamlit as st
import pandas as pd
from datetime import datetime
import importlib 
import re 


# --- Configuration ---
APP_TITLE = "🔐 Solana Security Explorer"
HOME_VIEW_NAME = "Home"

# ------------------------------
# Incident Data with Tags
# ------------------------------
incident_data = [
    {"Date": "Feb 2, 2022", "Project / Service": "Wormhole Bridge", "Loss (approx.)": "$326 M", "Type": "Major hack", "Description": "Signature-verification bug allowed minting of 120,000 ETH on Solana.", "Tags": ["bridge", "supply inflation"]},
    {"Date": "Mar 23, 2022", "Project / Service": "Cashio (Saber Cash)", "Loss (approx.)": "$52 M", "Type": "Major hack", "Description": "Bypassed unverified-account checks to drain treasury.", "Tags": ["stablecoin", "frontend"]},
    {"Date": "Jul 2, 2022", "Project / Service": "Crema Finance", "Loss (approx.)": "$8.78 M", "Type": "Flash-loan exploit", "Description": "Price-oracle manipulation to inflate collateral.", "Tags": ["defi", "oracle", "flash loan"]},
    {"Date": "Jul 28, 2022", "Project / Service": "Nirvana Finance", "Loss (approx.)": "$3.5 M", "Type": "Flash-loan exploit", "Description": "Price-oracle manipulation.", "Tags": ["defi", "oracle", "flash loan"]},
    {"Date": "Aug 2, 2022", "Project / Service": "Slope Wallet", "Loss (approx.)": "$5.2 M", "Type": "Key-leak", "Description": "Backend stored private keys in plaintext; ~9,229 wallets drained.", "Tags": ["wallet"]},
    {"Date": "Aug 29, 2022", "Project / Service": "OptiFi", "Loss (approx.)": "$661 K", "Type": "Logic bug", "Description": "Margin-engine error allowed unauthorized withdrawals.", "Tags": ["defi", "smart contract"]},
    {"Date": "Oct 11, 2022", "Project / Service": "Mango Markets", "Loss (approx.)": "$100 M", "Type": "Flash-loan/oracle hack", "Description": "Inflated collateral prices, then withdrew loans.", "Tags": ["oracle", "defi"]},
    {"Date": "Oct 12, 2022", "Project / Service": "Tulip Protocol", "Loss (approx.)": "$2.5 M", "Type": "Oracle manipulation", "Description": "Follow-on of Mango exploit via shared price feeds.", "Tags": ["oracle", "defi"]},
    {"Date": "Oct 12, 2022", "Project / Service": "UXD Protocol", "Loss (approx.)": "$20 M", "Type": "Oracle manipulation", "Description": "Similar vector as Mango/Tulip.", "Tags": ["oracle", "defi"]},
    {"Date": "Nov 2, 2022", "Project / Service": "Solend", "Loss (approx.)": "$1.26 M", "Type": "Oracle-price attack", "Description": "Manipulated SOL/USD feed to trigger liquidations.", "Tags": ["oracle", "defi"]},
    {"Date": "Dec 16, 2022", "Project / Service": "Raydium", "Loss (approx.)": "$5.5 M", "Type": "Malware/key theft", "Description": "Trojan on developer’s machine drained pools.", "Tags": ["dex", "key compromise"]},
    {"Date": "Jan 12, 2023", "Project / Service": "Solana Mobile (app)", "Loss (approx.)": "—", "Type": "API bug", "Description": "Debug endpoint exposed private user data; patched within hours.", "Tags": ["mobile", "api"]},
    {"Date": "Apr 15, 2022", "Project / Service": "Phantom Wallet", "Loss (approx.)": "—", "Type": "Clipboard hijack bug", "Description": "Malicious sites could replace copied addresses; patched.", "Tags": ["wallet", "security"]},
    {"Date": "Aug 7, 2023", "Project / Service": "Cypher Protocol", "Loss (approx.)": "$1 M", "Type": "Logic-bug exploit", "Description": "Order-matching vulnerability; contracts frozen.", "Tags": ["defi", "smart contract"]},
    {"Date": "Sep 14, 2023", "Project / Service": "Jupiter Aggregator", "Loss (approx.)": "—", "Type": "Routing bug", "Description": "Underpriced swap routes could be front-run; fixed pre-exploit.", "Tags": ["dex", "routing"]},
    {"Date": "Nov 2, 2023", "Project / Service": "Solflare Wallet", "Loss (approx.)": "—", "Type": "Cross-site scripting", "Description": "XSS in wallet extension UI; patched.", "Tags": ["wallet", "security"]},
    {"Date": "Dec 20, 2023", "Project / Service": "Marinade Finance", "Loss (approx.)": "—", "Type": "Oracle lag issue", "Description": "Delayed price feeds risked liquidation; mitigated via guardian set.", "Tags": ["defi", "oracle"]},
    {"Date": "Jan 18, 2024", "Project / Service": "Serum DEX", "Loss (approx.)": "—", "Type": "Order-book bug", "Description": "Market-order logic could match at stale prices; no major losses reported.", "Tags": ["dex", "order book"]}
]

# Convert and sort by date
for incident in incident_data:
    try:
        incident["Parsed Date"] = datetime.strptime(incident["Date"], "%b %d, %Y")
    except ValueError:
        st.error(f"Error parsing date for incident: {incident['Project / Service']}")
        incident["Parsed Date"] = datetime.min 

incident_data = sorted(incident_data, key=lambda x: x.get("Parsed Date", datetime.min)) # Use .get for safety

# ------------------------------
# Severity Score Calculation
# ------------------------------
def calculate_severity(incident):
    base_score = 0
    type_weights = {
        "Major hack": 5,
        "Flash-loan/oracle hack": 4,
        "Key-leak": 3,
        "API validation bug": 1,
        "Flash-loan exploit": 4, 
        "Oracle manipulation": 4, 
        "Logic bug": 3,         
        "Malware/key theft": 5, 
        "API bug": 1,           
        "Smart-contract bug": 3,
        "Clipboard hijack bug": 1,
        "Logic-bug exploit": 3, 
        "Routing bug": 1,       
        "Cross-site scripting": 1,
        "Oracle lag issue": 1,  
        "Order-book bug": 1,    
        "Token-mint vulnerability": 2, 
        "Hot-wallet hack": 5    
    }
    base_score += type_weights.get(incident["Type"], 0)

    # Estimate severity by loss
    loss_str = incident["Loss (approx.)"].replace("$", "").replace(" M", "M").replace("—", "0").strip() # Added strip
    if "M" in loss_str:
        try:
            loss_val = float(loss_str.replace("M", ""))
            if loss_val > 200:
                base_score += 5
            elif loss_val > 50:
                base_score += 3
            elif loss_val > 10:
                base_score += 2
            # Add more granular scoring for smaller losses if needed
            elif loss_val > 1: # $1M to $10M
                base_score += 1
            # Loss < $1M might add 0 or a fraction, currently adds 0 via the else below
            # else: # Loss $0M to $1M - could add 0 or a tiny score if desired
            # base_score += 0
        except ValueError: # Handle cases where conversion to float fails
            pass
    elif loss_str == "0":
         pass # No loss, no score added from loss
    # If loss_str is not "$... M" and not "—", it's not handled by this loss logic.
    # You might want to add specific handling for "K" (Thousands) if needed.

    # You could add more scoring criteria here (e.g., impact, complexity)

    incident["Severity Score"] = base_score

for incident in incident_data:
    calculate_severity(incident)

# ------------------------------
# Streamlit Config
# ------------------------------
st.set_page_config(page_title="Solana Security Incidents", layout="wide")



# ------------------------------
# --- Reusable Styled Metric Function ---
def display_styled_metric(label, value, key=None):
    """
    Renders a metric-like structure using st.markdown with inline styles.
    Includes curved edges and centralized content.

    Args:
        label (str): The label text for the metric.
        value (str): The value text for the metric (can be formatted like '$100M').
        key (str, optional): An optional unique key for the component. Defaults to None.
    """
    # Use a unique key if called multiple times within dynamic loops/containers,
    # though for simple calls within a column, Streamlit often handles it.
    # The key parameter is good practice for robustness.

    styled_html = f"""
    <div style="
        background-color: #424b43; /* Your desired background color */
        border: 3px solid #111212; /* Your desired border */
        padding: 20px; /* Adjust padding as needed (px is often more predictable than %) */
        border-radius: 10px; /* Curved edges */
        color: white; /* Text color for the container */
        overflow-wrap: break-word; /* Wrap long text */
        text-align: center; /* Center text horizontally if not using flex alignment */
        height: 100%; /* Optional: Helps make columns the same height */
        display: flex; /* Use flexbox for layout */
        flex-direction: column; /* Stack label and value vertically */
        justify-content: center; /* Vertically center content in the flex container */
        align-items: center; /* Horizontally center content in the flex container */
    ">
        <div style="
            color: #B7e493; /* Your desired label color */
            font-size: 1.1em; /* Adjust font size for label */
            margin-bottom: 5px; /* Space between label and value */
            overflow-wrap: break-word;
            white-space: break-spaces; /* Allows text to wrap on spaces */
        ">{label}</div>
        <div style="
            font-size: 2em; /* Adjust font size for value */
            font-weight: bold; /* Make value bold */
            color: white; /* Your desired value color */
            overflow-wrap: break-word;
        ">{value}</div>
    </div>
    """
    # Pass the key to st.markdown if provided, though it's less common for non-interactive markdown
    st.markdown(styled_html, unsafe_allow_html=True)


# ------------------------------
# Style & Theme
# ------------------------------
st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    h1 {color: #2c3e50; text-align: center; margin-bottom: 30px;}
    h2, h3 {color: #34495e;}
    table {font-size: 15px;}
    .stButton > button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        padding: 6px 12px;
        transition: background-color 0.3s ease;
        margin-right: 5px; /* Add some space between buttons */
    }
    .stButton > button:hover {
        background-color: #2980b9;
    }
    .block-container {padding-top: 2rem;}

    /* Style for the interactive table rows */
    /* Targets the div wrapping st.container in columns */
    div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stHorizontalBlock"]) {
         border-bottom: 1px solid #ecf0f1; /* Add subtle row separation */
         padding: 5px 0; /* Add padding */
    }

    </style>
""", unsafe_allow_html=True)

# --- Helper function to sanitize project names into valid module names ---
def sanitize_module_name(name):
    """Converts a project name string into a valid Python module name."""
    # Replace spaces, parentheses, and common separators with underscores
    name = re.sub(r'[()\s/\\-]+', '_', name)
    # Remove any characters that are not alphanumeric or underscore
    name = re.sub(r'\W+', '', name) # Removed +, keeping only alphanum and underscore
    # Convert to lowercase
    name = name.lower()
     # Replace multiple underscores with a single one
    name = re.sub(r'__+', '_', name)
    # Remove leading/trailing underscores
    name = name.strip('_')
    # Ensure it's not empty and doesn't start with a number (add 'p_' prefix if it does)
    if not name:
         return "default_incident" # Or handle error appropriately
    if name[0].isdigit():
        name = 'p_' + name
    return name

# ------------------------------
# Navigation State Handling
# ------------------------------
# Initialize session state if not already done
if "page" not in st.session_state:
    st.session_state["page"] = HOME_VIEW_NAME

# Initialize navigation options after incident_data is processed
project_names = [incident["Project / Service"] for incident in incident_data]
navigation_options = [HOME_VIEW_NAME] + project_names

# Extract all unique tags from incident_data
all_tags = sorted(list(set(tag for incident in incident_data for tag in incident.get("Tags", [])))) # Added .get for safety

# Sidebar Navigation
st.sidebar.title(APP_TITLE)

# Tag Filter - applies to the "Home" view
# This filter doesn't change the navigation, just filters the Home table
tag_filter = st.sidebar.multiselect("Filter by Tags (Home View)", options=all_tags)

# Navigation using Radio buttons
# Use the session state value as the default/current value for the radio
# This ensures the radio reflects the current page, whether set by radio or table button
current_page = st.session_state["page"] # Get current state

# Find the index for the current page, default to 0 (Home) if not found
try:
    default_index = navigation_options.index(current_page)
except ValueError:
    default_index = 0 # Fallback to Home if state is something unexpected

selected_page_from_radio = st.sidebar.radio(
    "Go to",
    options=navigation_options,
    index=default_index, # Set the radio's initial/current state from session state
    key="sidebar_nav" # Unique key for the radio button
)

# --- State Update Logic ---
# If the radio button's selection differs from the current session state, update the state
# This handles navigation initiated by the radio button itself
if selected_page_from_radio != current_page:
     st.session_state["page"] = selected_page_from_radio
     st.rerun() # Trigger rerun

# Note: Table button clicks (in the Home page section) also update st.session_state["page"]
# and call st.rerun(). This combined approach allows both widgets to control navigation.

# --- Main Content Area ---

# Display content based on selected page in session state (which is updated by both nav methods)
current_page = st.session_state["page"] # Re-get state in case it was just updated

if current_page == HOME_VIEW_NAME:
    st.title("📜 Solana Security Incidents - Chronological Table")

    df = pd.DataFrame(incident_data)
    df.insert(0, "S/N", range(1, len(df) + 1))
    df_display = df.copy() # Start with a copy

    # Apply tag filter if any tags are selected
    if tag_filter:
        df_display = df_display[df_display["Tags"].apply(lambda tags: any(tag in tags for tag in tag_filter))]

    # Select and reorder columns for the display table
    display_columns = ["S/N", "Date", "Project / Service", "Loss (approx.)", "Type", "Severity Score", "Tags"]
    df_display = df_display[display_columns]

    if df_display.empty: # Check after filtering
        st.info("No incidents match the selected tags.")
    else:
        # Use st.columns for the custom header
        header_cols = st.columns([0.05, 0.15, 0.25, 0.15, 0.15, 0.1, 0.15])
        header_titles = ["S/N", "Date", "Project / Service", "Loss (approx.)", "Type", "Severity", "Tags"]
        for col, title in zip(header_cols, header_titles):
             col.markdown(f"**{title}**") # Make header bold

        st.markdown("---") # Separator below header

        # Display rows using columns and buttons for navigation
        for i, row in df_display.iterrows():
            # Use the same column widths as the header
            cols = st.columns([0.05, 0.15, 0.25, 0.15, 0.15, 0.1, 0.15])

            # Column 1: S/N
            cols[0].markdown(row["S/N"])
            # Column 2: Date
            cols[1].markdown(row["Date"])

            # Column 3: Project / Service - This column contains the button
            # --- BUTTON LOGIC ---
            # Ensure the button's key is unique per row (using S/N)
            # Clicking the button updates the session state and triggers a rerun
            if cols[2].button(row["Project / Service"], key=f"btn_{row['S/N']}"):
                st.session_state["page"] = row["Project / Service"] # Update state to the project name
                st.rerun() # Trigger Streamlit rerun
            # --- END BUTTON LOGIC ---

            # Column 4: Loss
            cols[3].markdown(row["Loss (approx.)"])
            # Column 5: Type
            cols[4].markdown(row["Type"])
            # Column 6: Severity
            cols[5].markdown(row["Severity Score"])
            # Column 7: Tags
            cols[6].markdown(", ".join(row["Tags"]))

# ------------------------------
# Incident Detail Page
# ------------------------------
elif current_page in project_names:
    # Display details for a specific project
    st.title(f"🔍 Incident Detail - {current_page}")

    # Find the selected incident data
    selected_incident = next((item for item in incident_data if item["Project / Service"] == current_page), None)

    if selected_incident:
        # --- Display Basic Details from Data ---
        # st.subheader(selected_incident["Project / Service"]) # Title already used above
        col1, col2 = st.columns([1,2])
        with col1:
            st.markdown(f"**📅 Date:** {selected_incident['Date']}")
            st.markdown(f"**💥 Type:** {selected_incident['Type']}")
            st.markdown(f"**💸 Loss (approx.):** {selected_incident['Loss (approx.)']}")
        with col2:
            st.markdown(f"**⚖ Severity Score:** {selected_incident['Severity Score']}")
            st.markdown(f"**🏷 Tags:** {', '.join(selected_incident.get('Tags', []))}")
            st.markdown(f"**📖 Description:** {selected_incident['Description']}")


        st.markdown("""
            ---
        """) # Add a separator before custom content section

        # --- Attempt to load and run specific content module ---
        module_name = sanitize_module_name(current_page)

        try:
            # Dynamically import the module
            # Use importlib.util and spec_from_file_location if files are not standard modules
            # For simplicity assuming files are in the same dir and standard modules:
            module = importlib.import_module(module_name)

            # Check if the module has a specific function (e.g., display_content)
            if hasattr(module, 'display_content') and callable(module.display_content):
                 module.display_content() # Call the function in the module
            else:
                 st.info(f"Module '{module_name}' found, but no 'display_content()' function exists.")

        except ImportError:
            # The module does not exist for this project
            st.info(f"No specific content module found for {current_page} (expected '{module_name}.py').")
        except Exception as e:
            # Catch other potential errors during import or execution of the custom module
            st.error(f"An error occurred while loading specific content for {current_page}: {e}")

    else:
        st.error(f"Could not find details for {current_page}.")

    # --- Back Button ---
    # Placed at the end of the detail page logic
    if st.button("⬅ Back to Home"):
        st.session_state["page"] = HOME_VIEW_NAME
        st.rerun()

# You might want to add a final 'else' block here to handle cases
# where st.session_state["page"] is set to something unexpected
else:
    st.error(f"Unknown page state: {current_page}")
    if st.button("Go to Home"):
         st.session_state["page"] = HOME_VIEW_NAME
         st.rerun()