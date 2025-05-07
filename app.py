import streamlit as st

# Title
st.title("📊 Position Size Calculator")

# --- Input Fields ---

# Account Balance and Risk % (in two columns)
col1, col2 = st.columns(2)
with col1:
    account_balance = st.number_input(
        "Account Balance ($)",
        value=2700.00,
        min_value=0.0,
        step=100.0,
        format="%.2f",
        help="Total capital in your trading account"
    )

with col2:
    risk_percent = st.radio(
        "Risk per Trade (%)",
        options=[0.5, 1, 1.5, 2, 3, 5],
        format_func=lambda x: f"{x}%",
        index=1,
        horizontal=True,
        help="How much of your account you're willing to risk on one trade"
    )

# Calculated risk in dollars
risk_dollars = (risk_percent / 100) * account_balance
st.markdown(f"**Risk Amount ($):** ${risk_dollars:,.2f}")

# Stop Loss and Fees % (in two columns)
col3, col4 = st.columns(2)
with col3:
    stop_loss_percent = st.number_input(
        "Stop Loss (%)",
        value=3.00,
        min_value=0.01,
        max_value=100.0,
        step=0.1,
        format="%.2f",
        help="How much price can move against you before you exit the trade"
    )

with col4:
    fees_percent = st.number_input(
        "Fees (%)",
        value=0.10,
        min_value=0.00,
        max_value=100.0,
        step=0.01,
        format="%.2f",
        help="Trading fees charged by your broker (in % of position size)"
    )

# Risk-to-Reward Ratio
rr_ratio = st.number_input(
    "Risk:Reward Ratio",
    value=2.0,
    min_value=0.01,
    step=0.1,
    format="%.2f",
    help="How much you aim to gain for every $1 risked"
)

# Leverage (horizontal radio buttons)
leverage = st.radio(
    "Leverage",
    options=[1, 2, 3, 4, 5, 10],
    format_func=lambda x: f"{x}x",
    index=0,
    horizontal=True,
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
st.markdown("### 🧮 Results")
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
