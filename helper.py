from collections import defaultdict
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

extract = URLExtract()
def fetch_stats(selected_users, df):
    num_msg = {}
    words = []
    user_word_count = defaultdict(int)
    media = {}
    link = []
    user_link = defaultdict(int)

    if 'Overall' in selected_users:
        # Total messages count in chat
        num_msg['Overall'] = df.shape[0]
        # Calculate overall media count
        media['Overall'] = df[df['message'] == '<Media omitted>\n'].shape[0]
        # Total word count in chat
        for message in df['message']:
            words.extend(message.split())
            link.extend(extract.find_urls(message))

    for user in selected_users:
        if user != 'Overall':
            user_messages = df[df['user'] == user]
            # Total number of message count of each user
            num_msg[user] = user_messages.shape[0]
            # Total media count of each user
            media[user] = user_messages[user_messages['message'] == '<Media omitted>\n'].shape[0]
            # Total words count by each user
            for message in user_messages['message']:
                words.extend(message.split())
                user_word_count[user] += len(message.split())
                link.extend(extract.find_urls(message))
                user_link[user] += len(extract.find_urls(message))

    return num_msg, len(words), user_word_count, media, len(link), user_link

#Plotting bar graph for most active user in a group
def most_active_user(selected_users, df):
    if 'Overall' not in selected_users:
        df = df[df['user'].isin(selected_users)]
    #We will make a new_dataframe where user=group_notification and message=<media omitted>\n will not be there and there will be
    #null\n messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'null\n']    
    x = temp['user'].value_counts().head()
    #reset_index() can be used to convert list or dictionary into dataframe
    df = round((temp['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'index' : 'user', 'user' : 'percent'})
    return x, df

#Wordcloud
def create_wordcloud(selected_users, df):
    f = open('stop_hinenglish1.txt','r')
    stop_words = f.read()
    
    # sourcery skip: inline-immediately-returned-variable
    if 'Overall' not in selected_users:
        df = df[df['user'].isin(selected_users)]
    #We will make a new_dataframe where user=group_notification and message=<media omitted>\n will not be there and there will be
    #null\n messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'null\n']
    
    def remove_stopwords(message):
        y=[]
        for words in message.lower().split():
                if words not in stop_words:
                    y.append(words)
        return " ".join(y)
                    
    wc = WordCloud(width=300, height=300, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_users, df):
    
    f = open('stop_hinenglish1.txt','r')
    stop_words = f.read()
    
    if 'Overall' not in selected_users:
        df = df[df['user'].isin(selected_users)]
    
    #We will make a new_dataframe where user=group_notification and message=<media omitted>\n will not be there and there will be
    #null\n messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'null\n']
    
    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
                
    n_df = pd.DataFrame(Counter(words).most_common(20))
    return n_df  

def emoji_analysis(selected_users, df):
    if 'Overall' not in selected_users:
        df = df[df['user'].isin(selected_users)]
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))   
    return emoji_df 

def monthly_analysis(selected_users, df):
    if 'Overall' not in selected_users:
        df = df[df['user'].isin(selected_users)]
    timeline= df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_analysis(selected_users, df):
    if 'Overall' not in selected_users:
        df = df[df['user'].isin(selected_users)]
    daily = df.groupby('only_date').count()['message'].reset_index()
    return daily

def week_activity(selected_users, df):
    if 'Overall' not in selected_users:
        df = df[df['user'].isin(selected_users)]
    return df['day_name'].value_counts()

def monthly_activity(selected_users, df):
    if 'Overall' not in selected_users:
        df = df[df['user'].isin(selected_users)]
    return df['month'].value_counts() 

def activity_heatmap(selected_users, df):
    if 'Overall' not in selected_users:
        df = df[df['user'].isin(selected_users)]
    #Creating pivot table for heatmap    
    user_heatmap = df.pivot_table(index='day_name', columns='peroid', values='message', aggfunc='count').fillna(0)
    return user_heatmap    