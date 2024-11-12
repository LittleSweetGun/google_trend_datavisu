import streamlit as st

st.set_page_config(page_title="WhaT", page_icon=':chart_with_upwards_trend:', layout='centered')

st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📈 What's Trending 📈</h1>", unsafe_allow_html=True)
# Welcome Text with styling
st.markdown("<div class='description'><p>Welcome to the <b>WhaT</b> app, your portal to explore and understand searches trends all around the world.</p></div>", unsafe_allow_html=True)

# Main Content
st.markdown("<h2 class='section-title'>🌍 Explore Popular Search Trends</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='description'>
<p>This app is designed to help you dive deep into Google Trends data, allowing you to explore trending topics across different cities, countries and over time. Whether you’re interested in current trending searches, historical data or trends by location, this app provides an intuitive and insightful way to access and analyze Google Trends information.</p>
</div>
""", unsafe_allow_html=True)

# Features
st.markdown("<h2 class='section-title'>📊 Website Features</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='description'>
<ul>
    <li><b>Trending Now</b>: Discover the latest popular search topics worldwide or by country.</li>
    <li><b>Trend by Cities</b>: Examine in which cities people are searching for the same things as you.</li>
    <li><b>Trends by Countries</b>: Explore in which countries people have the same interests as you.</li>
    <li><b>Trends Over Time</b>: Analyze how topics have risen or fallen in popularity over time.</li>
</ul>
Each section provides a unique perspective into the patterns and interests that are shaping the world today.
</div>
""", unsafe_allow_html=True)

# Instructions
st.markdown("<h2 class='section-title'>🛠️ How to Use</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='description'>
<ul>
    <li><b>Navigate</b> through the sections (Trending Now, Cities, Countries, Over Time) using the sidebar.</li>
    <li><b>Visualize</b> the data in different formats, such as line charts, bar charts, and heatmaps, to see how trends evolve.</li>
    <li><b>Interact</b> with the data by choosing specific regions, timeframes, and topics of interest.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Goal Section
st.markdown("<h2 class='section-title'>🎯 Goal of the Website</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='description'>
<p>The goal of this app is to make <b>Google Trends data accessible and insightful</b> for users across various fields. It’s designed for anyone interested in gaining a deeper understanding of global and regional trends—from marketers and researchers to curious minds wanting to stay up-to-date with popular culture.</p>
</div>
""", unsafe_allow_html=True)

# Footer note
st.markdown("""
<div class='note'>
<p><b>Note:</b> All trend data, sourced from Serpapi's Google Trends and Google Trends Now API, may reflect search patterns in real-time or over specific historical periods. This app aims to provide valuable insights into user interests and behavior based on Google search data.</p>
</div>
""", unsafe_allow_html=True)
