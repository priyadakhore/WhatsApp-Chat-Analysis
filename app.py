import streamlit as st
import matplotlib.pyplot as plt
import preprocessor as pre
import helper
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")
app_mode=st.sidebar.selectbox("Select App Mode",["Select",'Analyze',"Instructions"])
if app_mode=='Analyze':
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        # st.text(data)
        df = pre.preprocess(data)
        st.dataframe(df)
        # extract unique users
        user_list = df['user'].unique().tolist()
        user_list.remove("group_notification")
        user_list.sort()
        user_list.insert(0, "Overall")
        selected_user = st.sidebar.selectbox("Show Analysis Wrt ", user_list)
        st.title("Top Stats")
        # if st.sidebar.button("Show Analysis"):
        #     num_messages, words, num_media_msg, num_links = helper.fetch_stats(selected_user, df)
        #     overall_sentiment = helper.print_final_sentiment(df)
        #     # st.title(overall_sentiment)
        #     st.sidebar.title(overall_sentiment)
        #     col1, col2, col3, col4 = st.columns(4)
        #     with col1:
        #         st.header("Total Mesaages")
        #         st.title(num_messages)
        #     with col2:
        #         st.header("Total Words")
        #         st.title(words)
        #     with col3:
        #         st.header("Total Media Msg")
        #         st.title(num_media_msg)
        #     with col4:
        #         st.header("Links Shared")
        #         st.title(num_links)

        # Timeline
        st.title("Monthly Timeline Analysis")
        timeline = helper.monthly_Timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # Daily timeline
        st.title("Daily Timeline By Date")
        date_timeline = helper.Day_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(date_timeline['date'], date_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # Activity Map
        col11, col12 = st.columns(2)
        with col11:
            st.title("Most busy day")
            day_timeline = helper.dayName_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(day_timeline['day'], day_timeline['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col12:
            st.title("Most busy month")
            month_timeline = helper.Most_busy_month(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(month_timeline['Month'], month_timeline['message'], color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            # Activity heatmap
        st.title("Weekly Activity Heatmap")
        heatmap_table = helper.Activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heatmap_table)
        st.pyplot(fig)

        # Most busy users
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col5, col6 = st.columns(2)
            with col5:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col6:
                st.dataframe(new_df)
        # wordcloud
        st.title("WordCloud")
        df_wc = helper.create_WordCloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        # Most common words
        most_common_df = helper.most_common_words(selected_user, df)
        st.title("Most Common Words")
        col7, col8 = st.columns(2)
        with col7:
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col8:
            st.dataframe(most_common_df)

        # Emoji Analysis
        st.title("Emoji Analysis")
        Emoji_df = helper.Emoji_Analysis(selected_user, df)
        col9, col10 = st.columns(2)
        with col9:
            st.dataframe(Emoji_df)
        with col10:
            fig, ax = plt.subplots()
            ax.pie(Emoji_df[1].head(10), labels=Emoji_df[0].head(10), autopct="%0.2f")
            st.pyplot(fig)





if app_mode=='Instructions':
    st.header("How to use?")
    st.text("Open your Whatsapp.")
    st.text("Click on any Group chat or any personal chat.")
    st.text("Click on the three dots icon on top right corner.")
    st.text("Select More..")
    st.text("Select on Export Chat option.")
    st.text("Export the chat Without Media.. ")
    st.text("Save the Exported Chat as .txt File.")
    st.text("Now go to analysis section upload the .txt file of group chat and Enjoy the result.")
    st.header("Note:")
    st.text("This is fully secure we don't store any users information about chat file this is only accessible for the particular user. ")
