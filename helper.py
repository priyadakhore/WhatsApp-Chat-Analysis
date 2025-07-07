
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extractor = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    num_messages=df.shape[0]
    words=[]
    for message in df['message']:
        words.extend(message.split())
    num_media_msg =df[df['message']=='<Media omitted>\n'].shape[0]
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    return num_messages,len(words),num_media_msg,len(links)



def most_busy_user(df):
    x = df['user'].value_counts().head()
    new_df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'Name','user':'Percentage'})
    return x,new_df
def create_WordCloud(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def Emoji_Analysis(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    Emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return Emoji_df
def monthly_Timeline(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    timeline = df.groupby(['year', 'Month_num', 'Month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline
def Day_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    date_timeline = df.groupby(['date']).count()['message'].reset_index()
    return date_timeline
def dayName_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    day_timeline = df.groupby(['day']).count()['message'].reset_index()
    return day_timeline
def Most_busy_month(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    month_timeline   = df.groupby(['Month']).count()['message'].reset_index()

    return month_timeline
def Activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    heatmap_table=df.pivot_table(index='day',columns='period',values='message',aggfunc='count').fillna(0)
    return heatmap_table
def analyze_sentiment(message):
    analysis = TextBlob(message)

    # Check if sentiment analysis is successful
    if analysis.sentiment.polarity == NotImplemented:
        return 'Invalid'

    # Classify the sentiment as positive, negative, or neutral
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'


def analyze_whatsapp_chat(chat):
    sentiments = [analyze_sentiment(message) for message in chat]

    # Calculate the overall sentiment, excluding invalid results
    valid_sentiments = [s for s in sentiments if s != 'Invalid']

    if valid_sentiments:
        overall_sentiment = max(set(valid_sentiments), key=valid_sentiments.count)
    else:
        overall_sentiment = 'No valid sentiments'

    return overall_sentiment

def print_final_sentiment(df):
    return analyze_whatsapp_chat(df['message'])
    



