import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.write('Whatsapp Chat Analyzer') 

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    #Read files as bytes
    byte_data = uploaded_file.getvalue()
    #To print data from uploaded file first we have to convert it to strings form byte
    #To convert byte to string
    data = byte_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    #To display the table data frame you have created in jupyter
    #st.dataframe(df)

    #Fetching unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_users = st.sidebar.multiselect("Show analysis wrt", user_list)

    if st.sidebar.button("Start Analysis"):
        #Finding total messages, word, media
        num_msg, words, user_word_count, media, links, user_link = helper.fetch_stats(selected_users, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        if "Overall" in num_msg:
            with col1:
                st.write("Total Messages")
                st.header(num_msg["Overall"])
        with col1:
            for user, count1 in num_msg.items():
                if user != "Overall":
                    st.write(f"Total Messages ({user})")
                    st.header(count1)
        with col2:
            if "Overall" in num_msg:
                st.write("Total Word_Count")
                st.header(words)

            for user, count2 in user_word_count.items():
                st.write(f"Total Word_Count ({user})")
                st.header(count2)
                

        if "Overall" in num_msg:
                with col3:
                    st.write("Total Media_Count")
                    st.header(media["Overall"])

        with col3:
                for user, count3 in media.items():
                    if user != "Overall":
                        st.write(f"Total Media_Count ({user})")
                        st.header(count3)
                        
        if "Overall" in num_msg:
            with col4:
                st.write("Total Link Shared")
                st.header(links)
        
        with col4:
            for user, count4 in user_link.items():
                if user != "Overall":
                    st.write(f"Total Link Shared({user})")
                    st.header(count4)                    
        
        #monthly analysis
        timeline = helper.monthly_analysis(selected_users, df)
        st.header("Monthly Analysis")
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        
        #daily analysis
        daily = helper.daily_analysis(selected_users, df)
        st.header("Daily Analysis")
        fig, ax = plt.subplots()
        ax.plot(daily['only_date'], daily['message'], color="red")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        
        #Most active days
        st.header("Most active Days")
        busy_day = helper.week_activity(selected_users, df)
        fig, ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values,color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        
        #Most Active Months
        st.header("Most Active Months")
        busy_month = helper.monthly_activity(selected_users, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values, color="orange")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        
        #Heatmap
        user_heatmap = helper.activity_heatmap(selected_users, df)
        st.header("Most Active Hour")
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap) 
        st.pyplot(fig)
        
        #finding the most active users in the group
        st.header("Most Active User")
        x, new_df = helper.most_active_user(selected_users, df)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)
        with col1:
            ax.bar(x.index, x.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

        #Creating WordCLoud
        st.header("WordCloud")
        df_wc = helper.create_wordcloud(selected_users,df)
        #Displaying Wordcloud
        fig, ax = plt.subplots()
        ax = plt.imshow(df_wc)
        st.pyplot(fig)
        
        #Most common words used by each user and overall
        n_df = helper.most_common_words(selected_users, df)
        st.header("Most Common Words")
        col1,col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            ax.barh(n_df[0], n_df[1])
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            st.dataframe(n_df)

        #Most used emojis
        emoji_df = helper.emoji_analysis(selected_users, df)
        #creating a new top_emoji_df dataframe to store exact top5 most used emojis
        top_emoji_df = emoji_df.head(5)
        st.header("Emoji Analysis")
        c1, c2 = st.columns(2) 
        with c1:
            fig, ax = plt.subplots()
            #To show pie chart for top5 most used emojis
            #ax.pie(top_emoji_df[1], labels=top_emoji_df[0], autopct='%1.1f%%')
            #ax.axis('equal')
            #To show bar graph
            ax.bar(top_emoji_df[0],top_emoji_df[1])
            st.pyplot(fig)
        with c2:
            st.dataframe(emoji_df)        