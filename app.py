import streamlit as st
import preprocess,helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 

st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    #to read a file
    print(uploaded_file)
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    #st.text(data)
    df = preprocess.preprocess(data)

    st.dataframe(df)
    #Fetech Unique user
    user_list = df['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show Analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media,num_links = helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')
      
        col1,col2,col3,col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Link Shared")
            st.title(num_links)
        #Monthly Timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['messages'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['messages'],color='black')
        plt.xticks(rotation= 'vertical')
        st.pyplot(fig)

        #Activity Map
        st.title('Activity Map')
       
        col1,col2 = st.columns(2)

        with col1:
            st.header('Most Busy Day')
            week_activity_map = helper.week_activity(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(week_activity_map.index,week_activity_map.values,color='orange')
            st.pyplot(fig)
        with col2:
            st.header('Most Busy Month')
            month_activity_map = helper.monthly_activity(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(month_activity_map.index,month_activity_map.values,color='purple')
            st.pyplot(fig)  
        #Activity heatmap
        st.title("Activity HeatMap")
        activity_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(activity_heatmap)
        plt.yticks(rotation='horizontal')
        st.pyplot(fig)




        #Finding the most active person
        if selected_user == 'Overall':
            st.title('Most Active Users')
            x,new_df = helper.active_user(df)
            fig,ax = plt.subplots()
            
            col1,col2 = st.columns(2) 
            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        #WORLD CLOUD
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc,interpolation='bilinear')
       
        
       
        st.pyplot(fig)  
        #Fetch Most Common  Words
        most_common_df = helper.most_common_words(selected_user ,df)
        st.title('Most Common Words')
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        
        plt.xticks(rotation='vertical') 
        st.pyplot(fig)   
        #st.dataframe(most_common_df)
        #Emoji Analysis
        emoji_df = helper.emoji(selected_user,df)
        st.title("Emojis Analysis")
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            
            fig=px.treemap(emoji_df, path= [0],values = emoji_df[1].tolist(),)
            
            
            
            st.plotly_chart(fig,use_container_width=True)
        #Sentiment Analysis
        st.title("Sentiment Analysis")
        val = helper.sentiment_analysis(df)
        col1,col2 = st.columns(2)
        with col1:
            st.header('Overall Sentiment')
            st.title(val)
        with col2:
            st.header('Sentiment Graph')
            fig,ax = plt.subplots()
            ax.hist('Polarity',data=df)
            st.pyplot(fig)    

        


                            
