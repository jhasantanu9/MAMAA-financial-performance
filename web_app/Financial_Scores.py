import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import streamlit.components.v1 as components
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from keras.models import load_model
from sklearn.metrics import mean_absolute_error, mean_squared_error

@st.cache_data
def create_dataset(data, time_step=60):
    X, y = [], []
    for i in range(len(data) - time_step):
        X.append(data[i:(i + time_step), 0])
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)

@st.cache_data
def predict_next_30_days(symbol, final_data):
    company_data = final_data[final_data['symbol'] == symbol][['close']]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(company_data)

    time_step = 60
    X, _ = create_dataset(scaled_data, time_step)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    model = load_model(f'{symbol}_lstm_model.h5')

    last_60_days = company_data[-60:].values
    last_60_days_scaled = scaler.transform(last_60_days)
    X_future = np.array([last_60_days_scaled])
    X_future = X_future.reshape(X_future.shape[0], X_future.shape[1], 1)

    future_predictions = []
    for _ in range(30):
        pred_price = model.predict(X_future)
        future_predictions.append(pred_price[0][0])
        pred_price_reshaped = np.array([[[pred_price[0][0]]]])
        X_future = np.append(X_future[:, 1:, :], pred_price_reshaped, axis=1)

    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

    historical_dates = company_data.index[-60:]
    future_dates = pd.date_range(start=company_data.index[-1] + pd.Timedelta(days=1), periods=30)
    
    historical_prices = company_data[-60:].reset_index(drop=True)
    future_prices_df = pd.DataFrame(future_predictions, columns=['Predicted_Close'])
    future_prices_df['date'] = future_dates

    combined_df = pd.concat([historical_prices, future_prices_df.set_index('date')], axis=0)
    
    return combined_df, historical_dates, future_dates, future_predictions

@st.cache_data
def calculate_moving_averages(df, window=50):
    df[f'ma_{window}'] = df['close'].rolling(window=window).mean()
    return df

@st.cache_data
def calculate_investment_scores(df):
    df = calculate_moving_averages(df, 10)  # Short-term SAM
    df = calculate_moving_averages(df, 50)  # Mid-term SAM
    df = calculate_moving_averages(df, 200) # Long-term SAM
    
    df['price_momentum'] = (df['close'] - df['close'].shift(1)) / df['close'].shift(1) * 100
    df['volatility_score'] = (df['high'] - df['low']) / df['close'] * 100
    df['volume_score'] = (df['volume'] - df['volume'].rolling(window=50).mean()) / df['volume'].rolling(window=50).mean() * 100
    df['ema_sma_score'] = df.apply(lambda row: 1 if row['ema'] > row['ma_50'] else -1, axis=1)
    df['rsi_score'] = df['rsi'].apply(lambda x: 2 if x < 30 else (-2 if x > 70 else 0))
    df['investment_score'] = 0.25 * df['price_momentum'] + \
                            0.25 * df['volatility_score'] + \
                            0.20 * df['volume_score'] + \
                            0.20 * df['ema_sma_score'] + \
                            0.10 * df['rsi_score']

    return df

@st.cache_data
def generate_investment_signals(df):
    df['signal'] = df['investment_score'].apply(lambda x: 'Buy' if x > 0 else ('Sell' if x < 0 else 'Hold'))
    return df

@st.cache_data
def plot_investment_score_over_time(df, symbol):
    fig = px.line(df, x='date', y='investment_score', title='Investment Score')
    return fig

@st.cache_data
def plot_signals(df, symbol):
    fig = px.scatter(df, x='date', y='investment_score', color='signal', title='Investment Signal')
    return fig

def main(merged_df, final_data):
    col1, col2 = st.columns([4, 2])
    with col2:
        selected_company = st.selectbox('Select a company:', merged_df['symbol'].unique())

    company_data = merged_df[merged_df['symbol'] == selected_company]
    company_data = calculate_investment_scores(company_data)
    company_data = generate_investment_signals(company_data)

    with col1: 
        st.header(f"Investment Analysis for {selected_company}")

    st.write("")

    col3, col4 = st.columns([3,3])
    with col3:
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

    col5, col6 = st.columns([3,3])
    with col5:
        st.plotly_chart(plot_investment_score_over_time(company_data, selected_company))

    with col6:
        st.plotly_chart(plot_signals(company_data, selected_company))

    st.markdown('#')

    st.subheader(f"Next 30-Day Closing Stock Price Prediction using Machine Learning (LSTM)")

    combined_data, historical_dates, future_dates, future_prices = predict_next_30_days(selected_company, final_data)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=historical_dates, y=combined_data['close'][:60], mode='lines', name='Historical Prices'))
    fig.add_trace(go.Scatter(x=future_dates, y=future_prices.flatten(), mode='lines+markers', name='Predicted Prices'))
    fig.update_layout(
        title= f'{selected_company}',
        yaxis_title='Closing Price')         
    st.plotly_chart(fig)

    model = load_model(f'./{selected_company}_lstm_model.h5')

    scaler = MinMaxScaler(feature_range=(0, 1))
    X_scaled = scaler.fit_transform(final_data[final_data['symbol'] == selected_company][['close']])
    X, y = create_dataset(X_scaled, time_step=60)
    
    y_pred = model.predict(X)
    y_pred_rescaled = scaler.inverse_transform(y_pred.reshape(-1, 1))
    y_actual_rescaled = scaler.inverse_transform(y.reshape(-1, 1))

    mae = mean_absolute_error(y_actual_rescaled, y_pred_rescaled)
    mse = mean_squared_error(y_actual_rescaled, y_pred_rescaled)
    
    st.markdown(
        """
        <div style='text-align: center;'>
            <h3 style='font-size: 25px;'>Model Performance</h3>
        </div>
        """, unsafe_allow_html=True
    )

    col7, col8 = st.columns([5, 3])
    with col8:
        st.markdown(
            f"""
            <div>
                <p style='padding-top:30px;font-size:16px; line-height:1.6;'>
                    <strong>Metrics below provide insight into the accuracy of the model's predictions.</strong><br>
                    <p></p>
                    <p></p>
                    <strong>Mean Absolute Error (MAE):  {mae:.2f}</strong><br> Measures the average magnitude of the errors in a set of predictions, without considering their direction. It gives an idea of how far off the model's predictions are from the actual values.<br>
                    <p></p>
                    <strong>Mean Squared Error (MSE): {mse:.2f}</strong><br> Measures the average of the squares of the errors—that is, the average squared difference between the estimated values and the actual value. MSE penalizes larger errors more than smaller ones, providing an idea of the variance in the prediction errors.
                </p>
            </div>
            """, unsafe_allow_html=True
        )
    
    with col7:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=np.arange(len(y_actual_rescaled)), y=y_actual_rescaled.flatten(), mode='lines', name='Actual Prices'))
        fig2.add_trace(go.Scatter(x=np.arange(len(y_pred_rescaled)), y=y_pred_rescaled.flatten(), mode='lines', name='Predicted Prices', line=dict(color='green')))
        fig2.update_layout(title=f'Actual vs Predicted Prices for {selected_company}', xaxis_title='Time', yaxis_title='Price')
        st.plotly_chart(fig2)

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

    components.html(html_content, height=800, scrolling=True)

if __name__ == "__main__":
    # Replace these with actual data when running the script
    merged_df = pd.DataFrame() 
    final_data = pd.DataFrame()  
    main(merged_df, final_data)