# financial_scores.py
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import streamlit.components.v1 as components

def main(merged_df):
    # Calculate moving averages
    def calculate_moving_averages(df, window=50):
        df[f'ma_{window}'] = df['close'].rolling(window=window).mean()
        return df

    # Calculate investment score
    def calculate_investment_scores(df):
        # Calculate Moving Averages
        df = calculate_moving_averages(df, 10)  # Short-term SAM
        df = calculate_moving_averages(df, 50)  # Mid-term SAM
        df = calculate_moving_averages(df, 200) # Long-term SAM
        
        # Price Momentum
        df['price_momentum'] = (df['close'] - df['close'].shift(1)) / df['close'].shift(1) * 100

        # Volatility Score (as is)
        df['volatility_score'] = (df['high'] - df['low']) / df['close'] * 100

        # Volume Score (as is)
        df['volume_score'] = (df['volume'] - df['volume'].rolling(window=50).mean()) / df['volume'].rolling(window=50).mean() * 100

        # EMA vs SAM Score
        df['ema_sma_score'] = df.apply(lambda row: 1 if row['ema'] > row['ma_50'] else -1, axis=1)
        
        # RSI Score
        df['rsi_score'] = df['rsi'].apply(lambda x: 2 if x < 30 else (-2 if x > 70 else 0))

        # Adjusted Investment Score
        df['investment_score'] = 0.25 * df['price_momentum'] + \
                                0.25 * df['volatility_score'] + \
                                0.20 * df['volume_score'] + \
                                0.20 * df['ema_sma_score'] + \
                                0.10 * df['rsi_score']

        return df

    # Generate investment signals
    def generate_investment_signals(df):
        df['signal'] = df['investment_score'].apply(lambda x: 'Buy' if x > 0 else ('Sell' if x < 0 else 'Hold'))
        return df

    # Function to plot investment score over time
    def plot_investment_score_over_time(df, symbol):
        fig = px.line(df, x='date', y='investment_score', title='Investment Score')
        return fig

    # Function to plot the signals
    def plot_signals(df, symbol):
        fig = px.scatter(df, x='date', y='investment_score', color='signal', title='Investment Signal')
        return fig

    col1, col2 = st.columns([4, 2])
    with col2:
        # Sidebar: Select company
        selected_company = st.selectbox('Select a company:', merged_df['symbol'].unique())

    # Filter data for selected company
    company_data = merged_df[merged_df['symbol'] == selected_company]
    company_data = calculate_investment_scores(company_data)
    company_data = generate_investment_signals(company_data)

    with col1: 
        # Display current scores and explanations
        st.header(f"Investment Analysis for {selected_company}")

    st.write("")
    st.write("")

    col3, col4 = st.columns([3,3])
    with col3:
        # Display the latest values
        latest_data = company_data.iloc[-1]
        st.markdown(
            f"""
            <div style='height:350px; width:100%; background-color:#F5F5F5;color:#333333;border-radius:10px; text-align:center ;padding-top:20px'>
                <p style='font-size:25px; text-align:center; font-weight:bold;'>Current investment scores for various factors:</p>
                <p style='font-size:20px;'>Price Momentum: {latest_data['price_momentum']:.2f}%</p>
                <p style='font-size:20px;'>Volatility Score: {latest_data['volatility_score']:.2f}</p>
                <p style='font-size:20px;'>Volume Score: {latest_data['volume_score']:.2f}</p>
                <p style='font-size:20px;'>EMA vs SMA Score: {latest_data['ema_sma_score']}</p>
                <p style='font-size:20px;'>RSI Score: {latest_data['rsi_score']:.2f}</p>  
            </div>
            """, unsafe_allow_html=True
        )


    with col4:
        latest_signal = latest_data['signal']
        # Emphasize Overall Investment Score
        st.markdown(
            f"""
            <div style='height:350px; width:100%;background-color:#F5F5F5;padding:10px;border-radius:10px;text-align:center;font-size:35px;'>
                <h2 style='color:#333333;'>Overall Investment Score</h2>
                <h1 style='color:#4CAF50;'>{latest_data['investment_score']:.2f}</h1>
                <h2 style='color:#333333;'>Current Investment Signal</h2>
                <h1 style='color:#FF5722;'>{latest_signal}</h1>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown('#')

    st.subheader(f"Investment Scores and Signals Over Time for {selected_company}")

    st.write("")
    st.write("")

    #Over Time
    col5, col6 = st.columns([3,3])
    with col5:
        # Plot investment score over time
        st.plotly_chart(plot_investment_score_over_time(company_data, selected_company))

    with col6:
        # Plot signals
        st.plotly_chart(plot_signals(company_data, selected_company))

    st.markdown('#')

    html_content = """
    <div style="background-color:#f9f9f9; padding:20px; border-radius:10px;">
        <h2 style="color:#333333; text-align:center;">Calculation Process and Scores</h2>

        <h3 style="color:#4CAF50; margin-top:20px;">1. Price Momentum:</h3>
        <p style="font-size:16px; line-height:1.6;">
            Measures the percentage change in the closing price compared to the previous day.<br>
            <strong>Formula:</strong> 
            <code style="background-color:#e6e6e6; padding:2px 5px; border-radius:4px;">
                (Close<sub>today</sub> - Close<sub>yesterday</sub>) / Close<sub>yesterday</sub> * 100%
            </code><br>
            <strong>Reason:</strong> Indicates the speed at which the price is changing. Positive values signal upward momentum, while negative values signal downward momentum.
        </p>

        <h3 style="color:#4CAF50; margin-top:20px;">2. Volatility Score:</h3>
        <p style="font-size:16px; line-height:1.6;">
            Measures the range between the high and low prices as a percentage of the closing price.<br>
            <strong>Formula:</strong> 
            <code style="background-color:#e6e6e6; padding:2px 5px; border-radius:4px;">
                (High - Low) / Close * 100%
            </code><br>
            <strong>Reason:</strong> Higher volatility indicates more significant price swings, which can be a sign of increased risk.
        </p>

        <h3 style="color:#4CAF50; margin-top:20px;">3. Volume Score:</h3>
        <p style="font-size:16px; line-height:1.6;">
            Compares the current trading volume to the 50-day average volume.<br>
            <strong>Formula:</strong> 
            <code style="background-color:#e6e6e6; padding:2px 5px; border-radius:4px;">
                (Volume<sub>today</sub> - Volume<sub>50-day average</sub>) / Volume<sub>50-day average</sub> * 100%
            </code><br>
            <strong>Reason:</strong> An increase in volume might suggest stronger investor interest or potential price movement.
        </p>

        <h3 style="color:#4CAF50; margin-top:20px;">4. EMA vs SAM Score:</h3>
        <p style="font-size:16px; line-height:1.6;">
            Compares the Exponential Moving Average (EMA) to the Simple Moving Average (SMA).<br>
            <strong>Formula:</strong> 
            <code style="background-color:#e6e6e6; padding:2px 5px; border-radius:4px;">
                1 if EMA > SAM else -1
            </code><br>
            <strong>Reason:</strong> If EMA is above SAM, it indicates bullish momentum. If EMA is below SAM, it suggests bearish trends.
        </p>

        <h3 style="color:#4CAF50; margin-top:20px;">5. RSI Score:</h3>
        <p style="font-size:16px; line-height:1.6;">
            The Relative Strength Index (RSI) measures the speed and change of price movements.<br>
            <strong>Formula:</strong> 
            <code style="background-color:#e6e6e6; padding:2px 5px; border-radius:4px;">
                2 if RSI < 30 else (-2 if RSI > 70 else 0)
            </code><br>
            <strong>Reason:</strong> RSI below 30 indicates potential undervaluation (strong buy signal), while RSI above 70 suggests overvaluation (strong sell signal).
        </p>

        <h3 style="color:#4CAF50; margin-top:20px;">6. Overall Investment Score:</h3>
        <p style="font-size:16px; line-height:1.6;">
            A composite score calculated by weighting the above factors.<br>
            <strong>Formula:</strong> 
            <code style="background-color:#e6e6e6; padding:2px 5px; border-radius:4px;">
                0.25 * Price Momentum + 0.25 * Volatility Score + 0.20 * Volume Score + 0.20 * EMA vs SAM Score + 0.10 * RSI Score
            </code><br>
            <strong>Reason:</strong> Combines various factors to provide an overall indication of investment quality. Positive scores suggest better investment opportunities.
        </p>
    </div>
    """

    # Render the updated HTML content in Streamlit
    components.html(html_content, height=800, scrolling=True)



if __name__ == "__main__":
    main()
