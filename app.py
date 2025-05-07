import streamlit as st

# Title
st.title("📊 Position Size Calculator")

# --- Input Fields ---
# Account balance
account_balance = st.number_input("Account Balance ($)", value=2700.00, min_value=0.0, step=100.0, format="%.2f")

# Risk per trade
risk_percent = st.radio(
    "Risk per Trade (%)",
    options=[0.5, 1, 1.5, 2, 3, 5],
    format_func=lambda x: f"{x}%",
    index=1
)

# Calculated risk in dollars
risk_dollars = (risk_percent / 100) * account_balance
st.markdown(f"**Risk Amount ($):** ${risk_dollars:,.2f}")

# Stop loss %
stop_loss_percent = st.number_input("Stop Loss (%)", value=3.00, min_value=0.01, max_value=100.0, step=0.1, format="%.2f")

# Fees %
fees_percent = st.number_input("Fees (%)", value=0.10, min_value=0.00, max_value=100.0, step=0.01, format="%.2f")

# Risk-to-Reward ratio
rr_ratio = st.number_input("Risk:Reward Ratio", value=2.0, min_value=0.01, step=0.1, format="%.2f")

# Leverage
leverage = st.radio("Leverage", options=[1, 2, 3, 4, 5, 10], format_func=lambda x: f"{x}x", index=0)

# --- Calculations ---
# Effective risk % includes stop loss and fees
total_risk_percent = stop_loss_percent + fees_percent
position_size = (risk_dollars / total_risk_percent) * 100  # Calculate position size in $
adjusted_position_size = position_size / leverage  # Adjust for leverage

# Calculate profit if TP hit
reward_percent = stop_loss_percent * rr_ratio
gross_profit = (position_size * reward_percent) / 100
net_profit = gross_profit - ((fees_percent / 100) * position_size)

# --- Output Fields ---
st.markdown(f"### 🧮 Results")
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
