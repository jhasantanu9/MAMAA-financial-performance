# overview.py
import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.cache_data
def main (companies_df, daily_df):

    # Create two columns with different proportions for title and select box
    col01, col02 = st.columns([4, 2])

    with col02:
        # The select box for selecting the company symbol
        symbol = st.selectbox("Select Company", daily_df['symbol'].unique())

    with col01:
        # Title that updates based on the selected company symbol
        st.title(f"{symbol}")

    # Filter the data based on the selected symbol
    filtered_df = daily_df[daily_df['symbol'] == symbol]
    company_info = companies_df[companies_df['symbol'] == symbol].iloc[0]


    # Create a candlestick plot with volume
    fig = go.Figure(data=[
        go.Candlestick(x=filtered_df['date'],
                        open=filtered_df['open'],
                        high=filtered_df['high'],
                        low=filtered_df['low'],
                        close=filtered_df['close'],
                        increasing_line_color='#00FF00', 
                        decreasing_line_color='#FF0000'),
        go.Bar(x=filtered_df['date'], y=filtered_df['volume'], 
                marker_color='skyblue', name='Volume', yaxis='y2')
    ])

    # Update layout for the candlestick chart and volume
    fig.update_layout(
        title=f'Candlestick Chart for {symbol}',
        yaxis_title='Price',
        yaxis2=dict(title='Volume', overlaying='y', side='right', showgrid=False),
        xaxis_rangeslider_visible=True,
        xaxis_rangeslider_thickness=0.1,
        xaxis_rangeslider_bgcolor='white',
        xaxis_tickformat='%d %b %Y',  
        xaxis_tickangle=0,
        xaxis_rangeselector=dict(
            buttons=list([
                dict(count=7, label='1w', step='day', stepmode='backward'),
                dict(count=1, label='1m', step='month', stepmode='backward'),
                dict(count=3, label='3m', step='month', stepmode='backward'),
                dict(count=6, label='6m', step='month', stepmode='backward'),
                dict(count=1, label='YTD', step='year', stepmode='todate'),
                dict(count=1, label='1y', step='year', stepmode='backward'),
                dict(step='all')
            ])
        ),
        yaxis2_showspikes=True, 
    )

    # Create a three-column layout with equal proportions
    col1, col2 = st.columns([6,6])

    # Display the company description and financial metrics in the first column
    with col1:
        st.subheader(f"**Name:** {company_info['Name']}")
        st.write(f"**Sector:** {company_info['Sector']}")
        st.write(f"**Industry:** {company_info['Industry']}")
        st.write(f"**Market Capitalization:** {company_info['MarketCapitalization']}")
        st.write(f"**Description:** {company_info['Description']}")

    # Display the plot in the second column
    with col2:
        st.plotly_chart(fig, use_container_width=True)

    # Create the column for financial metrics
    col3 = st.columns([1])[0] 

    with col3:
        st.subheader("Financial Metrics")

        # Define the metrics dictionary
        metrics = {
            "EBITDA": f"{company_info['EBITDA']}",
            "P/E Ratio": f"{company_info['PERatio']}",
            "PEG Ratio": f"{company_info['PEGRatio']}",
            "Book Value": f"{company_info['BookValue']:}",
            "Dividend Per Share": f"{company_info['DividendPerShare']}",
            "Dividend Yield": f"{company_info['DividendYield']}",
            "EPS": f"{company_info['EPS']}",
            "Revenue Per Share (TTM)": f"{company_info['RevenuePerShareTTM']}",
            "Profit Margin": f"{company_info['ProfitMargin']}",
            "Operating Margin (TTM)": f"{company_info['OperatingMarginTTM']}",
            "Return on Assets (TTM)": f"{company_info['ReturnOnAssetsTTM']}",
            "Return on Equity (TTM)": f"{company_info['ReturnOnEquityTTM']}",
            "Revenue (TTM)": f"{company_info['RevenueTTM']}",
            "Gross Profit (TTM)": f"{company_info['GrossProfitTTM']}",
            "Diluted EPS (TTM)": f"{company_info['DilutedEPSTTM']}",
            "Quarterly Earnings Growth (YoY)": f"{company_info['QuarterlyEarningsGrowthYOY']}",
            "Quarterly Revenue Growth (YoY)": f"{company_info['QuarterlyRevenueGrowthYOY']}",
            "Analyst Target Price": f"${company_info['AnalystTargetPrice']}",
            "Analyst Rating (Strong Buy)": f"{company_info['AnalystRatingStrongBuy']}",
            "Analyst Rating (Buy)": f"{company_info['AnalystRatingBuy']}",
            "Analyst Rating (Hold)": f"{company_info['AnalystRatingHold']}",
            "Analyst Rating (Sell)": f"{company_info['AnalystRatingSell']}",
            "Analyst Rating (Strong Sell)": f"{company_info['AnalystRatingStrongSell']}",
            "Trailing P/E": f"{company_info['TrailingPE']}",
            "Forward P/E": f"{company_info['ForwardPE']}",
            "Price to Sales Ratio (TTM)": f"{company_info['PriceToSalesRatioTTM']}",
            "Price to Book Ratio": f"{company_info['PriceToBookRatio']}",
            "EV to Revenue": f"{company_info['EVToRevenue']}",
            "EV to EBITDA": f"{company_info['EVToEBITDA']}",
            "Beta": f"{company_info['Beta']}",
            "52 Week High": f"${company_info['52WeekHigh']}",
            "52 Week Low": f"${company_info['52WeekLow']}",
            "50-Day Moving Avg": f"${company_info['50DayMovingAverage']}",
            "200-Day Moving Avg": f"${company_info['200DayMovingAverage']}",
        }

    # Convert the metrics dictionary to a DataFrame and transpose it
    metrics_df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])
    st.dataframe(metrics_df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()