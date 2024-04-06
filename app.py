import streamlit as st
import concurrent.futures
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

# Function to extract transcript from YouTube video
def extract_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript])
        return transcript_text
    except Exception as e:
        st.error(f"Error extracting transcript: {e}")
        return None

# Function to summarize transcript in chunks
def summarize_chunk(chunk):
    try:
        summarizer = pipeline("summarization")
        return summarizer(chunk, max_length=1024, min_length=50, length_penalty=2.0, num_beams=4, temperature=0.5)[0]["summary_text"]
    except Exception as e:
        st.error(f"Error summarizing chunk: {e}")
        return None

# Main function to run Streamlit app
def main():
    st.title("YouTube Video Summarizer by Kaaraalan AI")

    video_link = st.text_input("YouTube Video Link", "")

    if st.button("Summarize"):
        if "youtube.com" not in video_link:
            st.warning("Please enter a valid YouTube video link.")
        else:
            video_id = video_link.split("v=")[1]
            with st.spinner("Summarizing..."):
                transcript_text = extract_transcript(video_id)
                if transcript_text:
                    chunk_size = 500
                    chunks = [transcript_text[i:i + chunk_size] for i in range(0, len(transcript_text), chunk_size)]
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        summaries = list(executor.map(summarize_chunk, chunks))
                    summary_text = " ".join(summaries)
                    st.write("Summary:")
                    st.write(summary_text)

if __name__ == "__main__":
    main()
