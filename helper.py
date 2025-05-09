from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import re
import emoji

extract=URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df=df[df['user'] == selected_user]

    num_messages=df.shape[0]
    words = []
    for message in df['messages']:
        words.extend(message.split())

    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]

    links=[]
    for message in df['messages']:
        links.extend(extract.find_urls(message))
    num_links = len(links)

    return num_messages, len(words),num_media_messages,num_links


def most_busy_user(df):
    x = df['user'].value_counts().head()  # Top 5 most active users (absolute count)

    percent_df = (
        df['user'].value_counts(normalize=True)
        .mul(100)
        .round(2)
        .reset_index(name='percent')
        .rename(columns={'index': 'name'})
    )

    return x, percent_df

from wordcloud import WordCloud

def create_wordcloud(selected_user, df):
    try:
        with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
            stop_words = f.read()
    except FileNotFoundError:
        stop_words = ""

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    def remove_stop_words(message):
        return " ".join([word for word in message.lower().split() if word not in stop_words])

    temp['messages'] = temp['messages'].apply(remove_stop_words)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))

    return df_wc

def most_common_words(selected_user, df):
    try:
        with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
            stop_words = f.read()
    except FileNotFoundError:
        stop_words = ""

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    words = []

    for message in temp['messages']:
        message = message.lower()
        message = re.sub(r'[^\w\s]', '', message)
        for word in message.split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['word', 'count'])
    return most_common_df



def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_counter = Counter(emojis)

    return pd.DataFrame(emoji_counter.most_common(), columns=['emoji', 'count'])


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + " " + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)
    return user_heatmap
















