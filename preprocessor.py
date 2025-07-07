import re
import pandas as pd
def listtostr(s):
    str1=" "
    for i in s:
        str1 += i
    return str1

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w\w\s-\s'
    messages = re.split(pattern, data)
    m1 = re.findall(pattern, data)
    pat = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}'
    dates = re.findall(pat, listtostr(m1))
    while (len(messages) != len(dates)):
        if len(messages) > len(dates):
            for i in range(len(messages) - len(dates)):
                messages.pop()
        else:
            for i in range(len(messages) - len(dates)):
                dates.pop()
    df = pd.DataFrame({'user_messages': messages, 'message_date': dates})
    df['messages_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    # seperate users and messages
    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_messages'], inplace=True)
    df.drop(columns=['date'], inplace=True)
    df['year'] = df['messages_date'].dt.year
    df['Month'] = df['messages_date'].dt.month_name()
    df['Day'] = df['messages_date'].dt.day
    df['Hour'] = df['messages_date'].dt.hour
    df['Minute'] = df['messages_date'].dt.minute
    df['Month_num'] = df['messages_date'].dt.month
    df['date'] = df['messages_date'].dt.date
    df['day'] = df['messages_date'].dt.day_name()
    period = []
    for hour in df[['day', 'Hour']]['Hour']:
        if hour == 12:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df





