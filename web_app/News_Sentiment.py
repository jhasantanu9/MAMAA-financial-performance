# news_sentiment.py
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from urllib.request import urlopen, Request
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

def main():
    def scrape_and_analyze(tickers):
        finviz_url = 'https://finviz.com/quote.ashx?t='
        news_tables = {}

        for ticker in tickers:
            url = finviz_url + ticker
            try:
                req = Request(url=url, headers={'user-agent': 'my-app'})
                response = urlopen(req)
                html = BeautifulSoup(response, features='html.parser')
                news_table = html.find(id='news-table')
                news_tables[ticker] = news_table
            except Exception as e:
                logging.error(f"Error fetching data for ticker {ticker}: {e}")

        parsed_data = []
        for ticker, news_table in news_tables.items():
            if news_table:
                for row in news_table.findAll('tr'):
                    try:
                        link = row.find('a')
                        if link is None:
                            continue  # Skip rows without a link

                        title = link.text
                        news_url = link['href']
                        date_td = row.find('td')
                        date_data = date_td.text.split(' ') if date_td else []

                        parsed_data.append([ticker, title, news_url])
                    except Exception as e:
                        logging.error(f"Error processing row for ticker {ticker}: {e}")

        if parsed_data:
            news_df = pd.DataFrame(parsed_data, columns=['ticker', 'title', 'url'])
            analyzer = SentimentIntensityAnalyzer()
            news_df['sentiment_score'] = news_df['title'].apply(lambda x: analyzer.polarity_scores(x)['compound'])
            return news_df
        else:
            return None
        
    # Initialize session state for news data if not already present
    if 'news_df' not in st.session_state:
        st.session_state.news_df = scrape_and_analyze(['META', 'AAPL', 'MSFT', 'AMZN', 'GOOGL'])

    tickers = ['META', 'AAPL', 'MSFT', 'AMZN', 'GOOGL']

    news_df = st.session_state.news_df

    if news_df is not None and not news_df.empty:
        col1, col2 = st.columns([4,2])
        
        with col2:
            selected_ticker = st.selectbox("Select Company", tickers)
            filtered_df = news_df[news_df['ticker'] == selected_ticker]
            overall_sentiment = filtered_df['sentiment_score'].mean()
        with col1:
            st.markdown(f"""
            <div>
                <h1>Overall Sentiment for {selected_ticker}: {overall_sentiment:.2f}</h1>
            </div>
        """, unsafe_allow_html=True)

        col3, col4 = st.columns([4,2])
        with col4:
            ""
                
        with col3:
            st.write(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") 

        st.write("")
        st.write("")

        # News Headlines and Sentiment Score
        html = '''
        <style>
            .news-container {
                display: flex;
                flex-direction: column;
                gap: 10px;
                width: 100%;
            }
            .header-row {
                display: flex;
                justify-content: space-between;
                padding: 8px;
                font-weight: bold;
                border-bottom: 1px solid #ddd;
            }
            .news-item {
                display: flex;
                justify-content: space-between;
                padding: 8px;
                border-bottom: 0px solid #ddd;
            }
            .sentiment-score {
                text-align: right;
                min-width: 100px;
            }
        </style>
        <div class="news-container">
            <div class="header-row">
                <div>News Headlines</div>
                <div>Sentiment Score</div>
            </div>
        '''
        
        for _, row in filtered_df.iterrows():
            title = row['title']
            sentiment_score = row['sentiment_score']
            news_url = row['url']
            html += f'<div class="news-item"><div><a href="{news_url}" target="_blank">{title}🔗</a></div><div class="sentiment-score">{sentiment_score:.2f}</div></div>'
        
        html += '</div>'
        
        st.markdown(html, unsafe_allow_html=True)
        
        st.write("")

        # Visualization of sentiment distribution
        fig = go.Figure(data=[go.Bar(
            y=filtered_df['sentiment_score'],
            text=filtered_df['sentiment_score'].apply(lambda x: f"{x:.2f}"),
            textposition='none'
        )])
        
        fig.update_layout(
            title="Sentiment Scores for News Headlines",
            yaxis_title='Sentiment Score',
            xaxis=dict(
                showline=False, 
                showgrid=False, 
                zeroline=False,
                showticklabels=False  # Hide x-axis ticks
            ),
            yaxis=dict(showline=True, showgrid=True, zeroline=False)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write("")

    else:
        st.write("No news data available for the selected tickers.")

    st.write("Positive Sentiment")
    st.markdown("""
    * **What It Means**: Positive sentiment in stock news indicates that the news stories related to a company are generally favorable. This could include reports of strong financial performance, new product launches, partnerships, positive analyst ratings, or overall market optimism about the company.
    * **Impact on Decision**: Investors may interpret positive sentiment as a signal that the company's stock is likely to perform well in the near future, leading to potential buying opportunities. It can boost investor confidence and drive stock prices higher.
    """)

    st.write("Negative Sentiment")
    st.markdown("""
    * **What It Means**: Negative sentiment in stock news suggests that the news surrounding a company is largely unfavorable. This could involve poor financial results, legal issues, product failures, management problems, or negative market outlooks.
    * **Impact on Decision**: Negative sentiment may signal that the company's stock could face challenges, leading to potential selling or avoiding the stock. It can decrease investor confidence and put downward pressure on stock prices.
    """)

    st.write("Making Informed Decisions")
    st.markdown("""
    * **Balanced View**: Investors should use sentiment analysis as one of many tools when making decisions. Positive sentiment can indicate potential opportunities, while negative sentiment can serve as a warning. However, it's essential to consider the broader context, including financial data, industry trends, and personal investment goals, to make well-informed decisions.
    """)

if __name__ == "__main__":
    main()
