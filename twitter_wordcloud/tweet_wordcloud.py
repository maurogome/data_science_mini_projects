import tweepy
import csv
import re
import string
import pandas as pd
import nltk as nltk
import matplotlib.pyplot as plt
from datetime import datetime
from nltk.corpus import stopwords
from wordcloud import WordCloud

nltk.download('stopwords')

# Aqui debes agregar las llaves de la API de Twitter que generaste:
consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''

def api_connection():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True)

    try:
        api.verify_credentials()
        print('Authentification succesful! \n\n')
    except:
        print('Error! \n\n')

    return api

def extract_tweets(keyword, count):
    api = api_connection()
    tweets = []
    for tweet in tweepy.Cursor(api.search, q = keyword, lang = 'es', include_rts = False).items(count):
        if (not tweet.retweeted and 'RT @' not in tweet.text):
            tweets.append(tweet.text)
    return tweets

def transform(text):
    stopWords = set(stopwords.words('spanish'))
    text = str(text)
    text = re.sub(r'@[A-Za-z0-9]+', ' ', text)
    text = re.sub(r'RT[\s]', ' ', text)
    text = re.sub(r'#', ' ', text)
    text = re.sub(r'https?:\/\/\S+', ' ', text)

    words = text.lower().split()

    re_punc = re.compile('[%s]' % re.escape(string.punctuation))
    stripped = [re_punc.sub('', w) for w in words]
    no_garbage = [w for w in stripped if not w in stopWords]

    return (" ".join(no_garbage))

def create_df(keyword, now):
    df = pd.DataFrame(data = tweets, columns = ['tweet_text'])
    path = 'tweet_ext/tweets_{}_{datetime}.csv'.format(keyword[1:], datetime = now)
    df.to_csv(path, sep = ',', index = False)

    return df


def plot_figure(wordcloud, keyword):
    img_path = 'img/wordcloud_{}_{datetime}.png'.format(keyword[1:], datetime = now)
    plt.figure(figsize = (8, 8), facecolor = 'black')
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.tight_layout(pad = 0)
    plt.savefig(img_path)
    plt.show()


if __name__ == '__main__':

    keyword = input('\nEnter the account or hashtag you want to analyse \ndon\'t forget de @ or # ex. @maurogome or #Python...\n\n')
    api = api_connection()
    tweets = extract_tweets(keyword, 1000)
    now = datetime.now().strftime('%Y_%m_%d')
    df= create_df(keyword, now)

    df['tweets_transform'] = df['tweet_text'].apply(transform)
    text = ' '.join(df.tweets_transform)
    wordcloud = WordCloud(width = 1024, height = 800, background_color = 'black', min_font_size = 14).generate(text)

    plot_figure(wordcloud, keyword)


