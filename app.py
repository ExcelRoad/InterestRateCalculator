import streamlit as st
import pandas as pd

# Function to calculate compound interest
def calculate_compound_interest(initial, rate, deposit, periods):
    results = []
    total_interest = 0.0
    total_amount = initial

    for period in range(1, periods + 1):
        interest = total_amount * (rate / 100)
        total_interest += interest
        total_amount += interest + deposit
        results.append({"תקופה": period, "סכום בסוף": total_amount, "ריבית בסוף": interest})

    return pd.DataFrame(results), total_amount, total_interest

# Set RTL Direction
st.markdown(
    """
    <style>
    body {
        direction: rtl;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title
st.title("מחשבון ריבית")

# User Inputs in one column
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])  # First column is 1 unit, second column is 2 units, third column is 1 unit

    with col1:
        # Text inputs for user data
        initial_amount_text = st.text_input("סכום התחלתי", value="0.00")
        rate_period = st.selectbox("תקופת הריבית", ["חודשי", "שנתי"])
        rate_text = st.text_input(f"ריבית {rate_period} (%)", value="0.00")
        monthly_deposit_text = st.text_input("הפקדה חודשית (אופציונלי)", value="0.00")
        number_of_periods_text = st.text_input(f"מספר תקופות ({rate_period})", value="1")

        # Convert text inputs to numbers
        try:
            initial_amount = float(initial_amount_text.replace(",", ""))
            rate = float(rate_text.replace(",", ""))
            monthly_deposit = float(monthly_deposit_text.replace(",", ""))
            number_of_periods = int(number_of_periods_text.replace(",", ""))
        except ValueError:
            initial_amount = rate = monthly_deposit = number_of_periods = 0.0

        # Validation checks
        if initial_amount <= 0:
            st.error("סכום התחלתי חייב להיות גדול מ-0")
        elif rate <= 0:
            st.error("הריבית חייבת להיות גדולה מ-0")
        elif number_of_periods <= 0:
            st.error("מספר התקופות חייב להיות גדול מ-0")
        else:
            # Move button to the bottom of the first column
            if st.button("חשב", key="button_col1"):  # Button only in the first column
                # Use the user input directly for periods
                periods = number_of_periods
                rate_per_period = rate / 12 if rate_period == "חודשי" else rate

                results_df, final_amount, total_interest = calculate_compound_interest(initial_amount, rate_per_period, monthly_deposit, periods)

                # Display Results in the second column
                with col2:
                    # Display Table with formatted numbers
                    st.subheader("טבלת תוצאות")
                    formatted_results = results_df.style.format({
                        "תקופה": "{:.0f}",
                        "סכום בסוף": "{:,.2f}",
                        "ריבית בסוף": "{:,.2f}"
                    })
                    st.dataframe(formatted_results)

                    # Display Line Chart
                    st.subheader("צמיחה לאורך זמן")
                    st.line_chart(results_df.set_index("תקופה")["סכום בסוף"])

                # Display Summary in the third column
                with col3:
                    st.subheader("סיכום")
                    st.metric(label="סכום סופי", value=f"{final_amount:,.2f}")
                    st.metric(label="סך הריבית שנצברה", value=f"{total_interest:,.2f}")

                    # Calculate Total Rate in Percent
                    total_rate_percent = (total_interest / initial_amount) * 100 if initial_amount > 0 else 0.0
                    st.metric(label="סך שיעור הריבית (%)", value=f"{total_rate_percent:.2f}%")

    with col2:
        pass  # Leave second column empty for results after the button is pressed

    with col3:
        pass  # Leave third column empty for summary metrics after the button is pressed
