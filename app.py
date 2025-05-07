import streamlit as st

# Set up the page layout and remove Streamlit's default header
st.set_page_config(page_title="Position Size Calculator", layout="centered", initial_sidebar_state="collapsed")

# Custom CSS to remove margins, padding, and compact the app further
st.markdown("""
    <style>
        .css-18e3th9 {  /* Adjust the title font size (hide it) */
            display: none;
        }
        .css-1v3fvcr {  /* Input fields and buttons padding */
            padding: 0.2rem;
        }
        .css-ffhzg2 {  /* Reduce the height of buttons */
            height: 2rem;
        }
        .css-h6ntur {  /* Adjust markdown header size */
            font-size: 1.25rem;
        }
        .css-k9y4e6 {  /* Input labels font size */
            font-size: 1rem;
        }
        /* Make the layout more compact */
        .stApp {
            padding-top: 0rem;
            padding-bottom: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Input Fields ---
account_balance = st.number_input(
    "Account Balance ($)",
    value=2700.00,
    min_value=0.0,
    step=100.0,
    format="%.2f",
    help="Total capital in your trading account"
)

risk_percent = st.number_input(
    "Risk per Trade (%)",
    value=3.0,
    step=0.5,
    format="%.2f",
    help="How much of your account you're willing to risk on one trade"
)

# Calculated risk in dollars
risk_dollars = (risk_percent / 100) * account_balance
st.markdown(f"**Risk Amount ($):** ${risk_dollars:,.2f}")

# Stop Loss and Fees % (Stacked for mobile)
stop_loss_percent = st.number_input(
    "Stop Loss (%)",
    value=3.00,
    min_value=0.01,
    max_value=100.0,
    step=0.1,
    format="%.2f",
    help="How much price can move against you before you exit the trade"
)

# Default fees set to 0.20
fees_percent = st.number_input(
    "Fees (%)",
    value=0.20,
    min_value=0.00,
    max_value=100.0,
    step=0.01,
    format="%.2f",
    help="Trading fees charged by your broker (in % of position size)"
)

# Risk-to-Reward Ratio (Default set to 3)
rr_ratio = st.number_input(
    "Risk:Reward Ratio",
    value=3.0,
    min_value=0.01,
    step=0.1,
    format="%.2f",
    help="How much you aim to gain for every $1 risked"
)

# Leverage
leverage = st.number_input(
    "Leverage",
    value=1,
    min_value=1,
    step=1,
    format="%d",
    help="Leverage allows you to control a larger position with less capital (does not change risk)"
)

# --- Calculations ---
total_risk_percent = stop_loss_percent + fees_percent
position_size = (risk_dollars / total_risk_percent) * 100  # Position size in $
adjusted_position_size = position_size / leverage  # Adjust for leverage

reward_percent = stop_loss_percent * rr_ratio
gross_profit = (position_size * reward_percent) / 100
net_profit = gross_profit - ((fees_percent / 100) * position_size)

# --- Output Fields ---
st.markdown(f"**Required Position Size:** ${adjusted_position_size:,.2f}")
st.markdown(f"**Profit if Take-Profit is Hit:** ${net_profit:,.2f} (after fees)")

# Optional: Expand section for explanation
with st.expander("ℹ️ How calculations work"):
    st.markdown("""
    - **Risk Amount ($)** = Account Balance × Risk %
    - **Position Size** = Risk Amount ÷ (Stop Loss % + Fees %)
    - **Adjusted Position Size** = Position Size ÷ Leverage
    - **Profit (TP hit)** = (Position Size × Stop Loss % × R:R) − Fees
    """)
