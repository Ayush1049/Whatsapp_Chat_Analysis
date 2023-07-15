import re
import pandas as pd

def preprocess(data):
    pattern = '\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s*[ap]m\s-\s'
    message = re.split(pattern, data)[1:]
    date = re.findall(pattern, data)
    date = [d.strip(' ') for d in date]

    df = pd.DataFrame({'user_message': message, 'message_date': date})
    # converting date string into datetime format to perform built-in function of pandas datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p -')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user_name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    peroid=[]
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            peroid.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            peroid.append(str('00') + "-" + str(hour+1))
        else:
            peroid.append(str(hour) + "-" + str(hour+1))
    df['peroid'] = peroid        

    return df
