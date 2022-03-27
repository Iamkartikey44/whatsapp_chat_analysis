from wordcloud import WordCloud
from urlextract import URLExtract
from collections import Counter
import matplotlib.pyplot as plt
import emoji as emj
import re
import pandas as pd 
extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    num_messages = df.shape[0]
    words=[]
    for i in df['messages']:
        words.extend(i.split())
    num_media = df[df['messages']=='<Media omitted>\n'].shape[0]#Number of media messages
    links=[]
    for message in df['messages']:
        links.extend(extract.find_urls(message))



    return num_messages,len(words),num_media,len(links)
def active_user(df):
    x = df['users'].value_counts().head()
    #percentage of message by all users
    df = round((df['users'].value_counts()/ df.shape[0])*100,2).reset_index().rename(columns = {'index':'name','user':'percentage_message'})
    return x,df
def create_wordcloud(user,df):
    f = open('hinglish.txt','r')
    stop_wrods = f.read()
    if user != 'Overall':
        df = df[df['users']==user]
    
    temp = df[df['messages']!= '<Media ommitted/n']
    def remove_stopword(text):
        y=[]
        for word in text.lower().split():
            if word not in stop_wrods:
                y.append(word)
        return " ".join(y)        
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['messages'] = temp['messages'].apply(remove_stopword) 
    df_wc = wc.generate(temp['messages'].str.cat(sep=' '))
    return df_wc
def most_common_words(user,df):
    f = open('hinglish.txt','r')
    stop_wrods = f.read()
    if user != 'Overall':
        df = df[df['users']==user]
   
    temp = df[df['messages']!= '<Media ommitted/n']
    words=[]
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_wrods:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df            

def emoji(user,df):
    if user != 'Overall':
        df = df[df['users']==user]
        
    emojis=[]
    for message in df['messages']:
        emojis.extend([c for c in message if c in emj.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))       
    return emoji_df

def monthly_timeline(user,df):
    if user != 'Overall':
        df = df[df['users']==user]
    timeline  = df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ "-" +str(timeline['year'][i]))
    timeline['time']  = time
    return timeline        


def daily_timeline(user,df):
    if user != 'Overall':
        df = df[df['users']==user]
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline

def week_activity(user,df):
    if user != 'Overall':
        df = df[df['users']==user]
    return df['day_name'].value_counts()    
    
def monthly_activity(user,df):
    if user != 'Overall':
        df = df[df['users']==user]
    return df['month'].value_counts() 

def activity_heatmap(user,df):
    if user != 'Overall':
        df = df[df['users']==user]
    activity = df.pivot_table(index='day_name',columns='period',values='messages',aggfunc='count').fillna(0)
    return activity  
def sentiment_analysis(df):
    a= sum(df['positive'])
    b = sum(df['negative'])
    c = sum(df['neutral'])
    if (a>b) and (a>c):
        return("Positive 😊 ")
    if (b>a) and (b>c):
        return("Negative 😠 ")
    if (c>a) and (c>b):
        return ("Neutral 🙂 ")
