import pandas as pd
import streamlit as st
import snscrape.modules.twitter as sntwitter

def analyze_sentiment(text):
    model = tweetnlp.load_model('sentiment')
    result = model.sentiment(text)
    if result == "positive":
        return 1
    elif result == "negative":
        return -1
    else:
        return 0

# Define a function to get the tweets
def get_tweets(maxTweets):
    tweets_list = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('#masscountry since:2023-02-24 until:2023-02-28').get_items()):
        if i > maxTweets:
            break
        tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.username])
    return tweets_list

# Define the Streamlit app
def main():
    st.title("Twitter Sentiment Analysis")
    max_tweets = st.slider("Select the maximum number of tweets to analyze", 100, 500000, 10000)

    # Get the tweets and create a dataframe
    tweets_list = get_tweets(max_tweets)
    df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

    # Analyze sentiment and add the sentiment column to the dataframe
    df["sentiment"] = df["Text"].apply(analyze_sentiment)

    # Display the dataframe in the app
    st.write(df)

    # Export the dataframe to a CSV file
    if st.button("Export to CSV"):
        df.to_csv('masscountry.csv', index=False)
        st.success("Data exported to masscountry.csv")
