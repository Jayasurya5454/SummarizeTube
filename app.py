import streamlit as st
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
import time

# Function to extract transcript from YouTube video
def extract_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript])
        return transcript_text
    except Exception as e:
        st.error(f"❌ Error extracting transcript: {e}")
        return None

# Function to summarize transcript
def summarize_transcript(transcript_text):
    try:
        summarizer = pipeline("summarization")
        summary = summarizer(transcript_text, max_length=1024, min_length=50, length_penalty=2.0, num_beams=4, temperature=0.5)
        return summary[0]["summary_text"]
    except Exception as e:
        st.error(f"❌ Error summarizing transcript: {e}")
        return None

# Main function to run Streamlit app
def main():
    st.title(" Kaaraalan AI YouTube Video Summarizer")

    video_link = st.text_input("🎥 YouTube Video Link", "")

    if st.button("🚀 Summarize"):
        if "youtube.com" not in video_link:
            st.warning("⚠️ Please enter a valid YouTube video link.")
        else:
            with st.spinner("Summarizing..."):
                time.sleep(3)  # Simulating some processing time
                video_id = video_link.split("v=")[1]
                transcript_text = extract_transcript(video_id)
                if transcript_text:
                    st.write("📝")
                    summary_text = summarize_transcript(transcript_text)
                    if summary_text:
                        st.write(summary_text)

if __name__ == "__main__":
    main()
