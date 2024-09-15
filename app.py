import streamlit as st
import preprocessing, helper
import matplotlib.pyplot as plt
import seaborn as sns

# Sidebar configuration
st.sidebar.title('Whatsapp Chat Analyzer')

# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a file (upload unzipped file)")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')

    # Preprocess data
    df = preprocessing.preprocess(data)

    # Store unique users in a list
    users = df['users'].unique().tolist()
    if 'group_notification' in users:
        users.remove('group_notification')
    users.sort()
    users.insert(0, 'Overall Analysis')
    selected_user = st.sidebar.selectbox('Select User', users)

    # Fetch stats
    num_msgs, words, media, links = helper.fetch_stats(selected_user, df)

    # Dashboard Layout
    if st.sidebar.button('Show Analysis'):

        # Main title
        if selected_user!='Overall Analysis':
            st.title(f'Analysis for :blue[{selected_user}]')
        else:
            st.title('Top Statistics')

        # Key Metrics
        st.markdown('### :orange[Key Metrics]')
        col1, col2, col3, col4 = st.columns(4)
        col1.metric('Total Messages', num_msgs)
        col2.metric('Total Words', len(words))
        col3.metric('Media Shared', media)
        col4.metric('Links Shared', len(links))

        # Visualization of Analytics
        st.markdown('---')
        st.markdown('### :orange[Visualization of Analytics]')

        # Most Busy Users (only for overall analysis)
        if selected_user == 'Overall Analysis':
            st.subheader('Most Busy Users')
            busy_users, new_df = helper.busy_users(df)
            col1, col2 = st.columns([2, 1])

            with col1:
                fig, ax = plt.subplots()
                ax.bar(busy_users.index, busy_users.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # Word Cloud
        st.subheader('Word Cloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis('off')
        st.pyplot(fig)

        # Most Common Words
        st.subheader('Most Common Words')
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='skyblue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji Analysis
        st.subheader('Emoji Analysis')
        emoji_df = helper.emoji_analysis(selected_user, df)

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f", colors=sns.color_palette("Set2"))
            st.pyplot(fig)

        # Monthly Timeline
        st.subheader('Monthly Timeline')
        timeline = helper.timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.subheader("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.subheader('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Most Busy Day**")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.markdown("**Most Busy Month**")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Weekly Activity Heatmap
        st.subheader("Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, ax=ax, cmap="YlGnBu", linewidths=0.5)
        st.pyplot(fig)
