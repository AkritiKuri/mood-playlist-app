import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Mood Playlist", page_icon="🎧", layout="centered")

# Load and clean dataset
df = pd.read_csv("big_mood_songs.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "").str.replace("_", "")

# Simple mood classifier from text
def detect_mood(text):
    text = text.lower()
    if any(word in text for word in ['happy', 'joy', 'excited', 'fun', 'smile']):
        return 'Happy'
    elif any(word in text for word in ['sad', 'lonely', 'depressed', 'frustrated','cry', 'blue']):
        return 'Sad'
    elif any(word in text for word in ['angry', 'mad', 'furious', 'rage']):
        return 'Angry'
    elif any(word in text for word in ['calm', 'relaxed', 'peaceful', 'zen']):
        return 'Calm'
    elif any(word in text for word in ['energetic', 'motivated', 'power', 'pump']):
        return 'Energetic'
    elif any(word in text for word in ['slow', 'gloomy', 'moody', 'dark']):
        return 'Melancholy'
    else:
        return 'Happy'  # Default fallback mood

# CSS for dark mode
st.markdown("""
    <style>
        body {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .song-card {
            background-color: #2e2e2e;
            padding: 1em;
            margin-bottom: 1em;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(255,255,255,0.05);
        }
        h1, h2, h3 {
            color: #ffffff;
        }
        .stSelectbox > div {
            color: #000;
        }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1 style='text-align:center;'>🎧 Mood-Based Playlist Generator</h1>", unsafe_allow_html=True)

# Mood source toggle
mode = st.radio("🎯 How would you like to select your mood?", ["Select from dropdown", "Type how you feel"])

# Mood selection
if mode == "Select from dropdown":
    moods = sorted(df['mood'].unique())
    selected_mood = st.selectbox("Select your mood:", moods)
else:
    user_input = st.text_input("Type your current feeling (e.g., I feel lonely today):")
    if user_input:
        selected_mood = detect_mood(user_input)
        st.success(f"✅ Detected mood: **{selected_mood}**")
    else:
        st.warning("Please type something to detect your mood.")
        selected_mood = None

# Show playlist if mood is selected
if selected_mood:
    filtered = df[df['mood'].str.lower() == selected_mood.lower()]
    st.markdown(f"### 🎶 Playlist for **'{selected_mood}'** mood:")
    for _, row in filtered.iterrows():
        st.markdown(f"""
        <div class="song-card">
            <strong>{row['songname']}</strong> by <em>{row['artist']}</em><br>
            <a href="{row['youtubelink']}" target="_blank">▶️ Listen on YouTube</a>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("🎵 Built with love & logic using Streamlit 💖")
