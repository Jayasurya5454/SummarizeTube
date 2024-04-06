import streamlit as st
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

# Initialize the summarization pipeline with explicit model and revision
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")

# Function to extract video ID from YouTube link
def get_video_id(link):
    return link.split("v=")[-1]

# Streamlit app title and description
st.title("YouTube Video Summarizer")
st.write("Enter the YouTube video link and get a summary of its transcript.")

# Input field for YouTube video link
video_link = st.text_input("Enter the YouTube video link:", "")

# Button to trigger summarization
if st.button("Summarize"):
    if video_link:
        # Extract video ID from the link
        video_id = get_video_id(video_link)
        
        # Get transcript of the video
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Summarize transcript in chunks
        chunk_size = 500
        summarized_text = ""
        for i in range(0, len(transcript), chunk_size):
            chunk = transcript[i:i + chunk_size]
            transcript_text = " ".join([entry["text"] for entry in chunk])
            summary = summarizer(transcript_text, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, temperature=0.5)
            summarized_text += f"Summary for chunk {i}-{i + chunk_size}:\n"
            summarized_text += summary[0]["summary_text"] + "\n\n"
        
        # Display summarized text
        st.subheader("Summarized Transcript:")
        st.write(summarized_text)
    else:
        st.warning("Please enter a YouTube video link.")
