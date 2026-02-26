from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.documents import Document

def fetch_transcript(video_id: str):
    try:
        # New API usage
        transcript_list = YouTubeTranscriptApi().list(video_id)
        fetched_transcript = transcript_list.find_transcript(['en']).fetch()

        documents = []

        for snippet in fetched_transcript.snippets:
            documents.append(
                Document(
                    page_content=snippet.text,
                    metadata={
                        "video_id": video_id,
                        "start": snippet.start,
                        "duration": snippet.duration
                    }
                )
            )

        return documents

    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return []