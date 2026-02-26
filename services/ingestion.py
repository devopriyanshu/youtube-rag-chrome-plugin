from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.documents import Document

video_id1 = 'VpBrWzfinpk'
video_id = 'ExvEIOWB-H0'


def fetch_transcript(video_id: str):
    ytt_api = YouTubeTranscriptApi()
    fetched_transcript= ytt_api.fetch(video_id, languages = ['en'])

    # transcript = " ".join([snippet.text for snippet in fetched_transcript])
    # for snippet in fetched_transcript:
    #     print(snippet.text)
    documents = []

    for snippet in fetched_transcript:
        documents.append(
            Document(
                page_content=snippet.text,
                metadata={
                    "video_id":video_id,
                    "start":snippet.start,
                    "duration":snippet.duration
                }
            )  
        )
    return documents    
