import xml.etree.ElementTree as ET
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    CouldNotRetrieveTranscript
)
def extract_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ['www.youtube.com', 'youtube.com']:
        if query.path == '/watch':
            return parse_qs(query.query).get('v', [None])[0]
        if query.path.startswith('/embed/'):
            return query.path.split('/')[2]
        if query.path.startswith('/v/'):
            return query.path.split('/')[2]
    return None

def get_best_transcript(video_id):
    try:
        # Try manual English transcript first
        return YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except NoTranscriptFound:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Try all generated transcripts until one works
            for transcript in transcript_list:
                if transcript.is_generated:
                    try:
                        return transcript.fetch()
                    except (ET.ParseError, CouldNotRetrieveTranscript):
                        # If this transcript fails to fetch properly, try next
                        continue
            return "not allowed"
        except (NoTranscriptFound, CouldNotRetrieveTranscript, TranscriptsDisabled):
            return "not allowed"
    except TranscriptsDisabled:
        return "not allowed"

def print_transcript_from_url(url):
    transcript_val = ""
    try:
        video_id = extract_video_id(url)
        if not video_id:
            print("Invalid YouTube URL")
            return

        result = get_best_transcript(video_id)

        if isinstance(result, str):
            print(result)
        else:
            for entry in result:
                try:
                    if isinstance(entry, dict):
                        start = entry.get("start")
                        text = entry.get("text", "")
                    else:
                        start = getattr(entry, "start", None)
                        text = getattr(entry, "text", "")

                    if start is not None and text:
                        transcript_val += f"{start}\t{text}\n"
                except Exception as e:
                    print(f"Error processing transcript entry: {e}")
    except Exception as e:
        transcript_val = ""

    return transcript_val.strip()

def get_transcript_val(url):
    transcript_val = print_transcript_from_url(url)
    if len(transcript_val)<10 or len(transcript_val.strip())<8:
        transcript_val = print_transcript_from_url(url)
    if len(transcript_val) < 10 or len(transcript_val.strip()) < 8:
        transcript_val = print_transcript_from_url(url)
    if len(transcript_val) < 10 or len(transcript_val.strip()) < 8:
        transcript_val = "Caption not found"

    return  transcript_val



if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=n99Ph-XbdeI"
    print(get_transcript_val(url))
