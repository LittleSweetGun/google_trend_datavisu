import streamlit as st

st.set_page_config(page_title="WhaT", page_icon=':chart_with_upwards_trend:', layout='centered')


st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📈 WhaT's Trending 📈</h1>", unsafe_allow_html=True)

st.write("Welcome to **WhaT**, your ultimate portal to explore, decode and vibe with search trends across the globe 🌍")
st.write("Here, we break down data like never before! Giving you the latest trends and insights from **Google Trends** in a fun, interactive way. It's like crypto for trends: fast, fresh and futuristic 🌐✨")


st.write("### 💻 Explore Popular Search Trends")
st.write("Ready to dive deep? 🤿 This app is here to give you the **data power** to explore trending topics worldwide—from cities to countries to trends over time. No matter if you're a trendsetter, a researcher or just curious, this tool is your new best friend for understanding **WhaT**'s popping and when 🔍")


st.write("### 📊 What’s Inside the Vault of Features?")
st.write("""
- 🔥 **Trending Now**: See the hottest search topics blowing up around the globe or by country 
- ✈️ **Trends by Countries**: Find out where in the world your interests match others’
- 🇺🇸 **Trend by Around the US**: Wondering where Americans are vibing with the same topics? Dive into search trends around the United States
- 📈 **Trends Over Time**: Watch the rise and fall of trends and spot what's hot (or what's :gray[fading]) over time
""")
st.write("Every section gives you a unique lens into the trends that are making waves in real time 🌊")

st.write("### 🛠️ How to Interact with the Data?")
st.write("""
Here’s how you can ride the data wave:

- 🚣‍♀️ **Navigate** the sections using the sidebar (Trending Now, Your IOTD - Interest Of The Day - )
- 👓 **Visualize** the data in super cool charts and graphs, including line charts, histograms and sunburst 
- 🗣️ **Interact** with the data by picking your preferred country, time range and trending topics

This is where **your** interest in trends meets next-level data visualization 🔮
""")

st.write("### 🎯 The Mission of This Portal")
st.write("The goal? Simple.")
st.write("We're here to make **Google Trends** data :blue[super accessible] and :blue[insightful] for you. Whether you're a marketer looking for the next big thing, a researcher diving into data patterns or a trend lover keeping tabs on what's :red[**hot**] right now, this app is your go-to space to stay in the know. From mainstream culture to niche communities, we’ve got the pulse of global interests right at your fingertips 💥")

st.write("🌐 Welcome to the world of trend data: :blue[**transparent**] and :blue[**totally next-gen**] 🚀")

with st.expander("📝 Note to the Data-Driven"):
    st.write("All trends here are sourced straight from [Serpapi's Google Trends API](https://serpapi.com/google-trends-api) and [Google Trends Now API](https://serpapi.com/google-trends-trending-now). Trends may reflect real-time data or historical patterns. This app is all about unlocking insights into what’s driving search behavior across the world.")

st.markdown("<h1 style='text-align: center;'>Let’s Dive into the Data!</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🤿</h1>", unsafe_allow_html=True)

