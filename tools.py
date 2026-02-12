import os
from crewai.tools import tool
import re

os.environ["OPENAI_API_KEY"] = "sk-dummy-key-not-used"

def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from YouTube URL or return the ID if already provided."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    
    return url_or_id

@tool
def yt_tool(video_url: str) -> str:
    """
    Extract transcript and information from a YouTube video.
    Useful for getting content from YouTube videos to create blog posts.
    
    Args:
        video_url: YouTube video URL or video ID
        
    Returns:
        str: The video transcript and information
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi as YTAPI
        
        video_id = extract_video_id(video_url)
        
        # Get transcript using fetch method
        transcript_obj = YTAPI().fetch(video_id)
        
        # Access the snippets attribute
        transcript_list = transcript_obj.snippets
        
        # Combine transcript text
        full_transcript = " ".join([snippet.text for snippet in transcript_list])
        
        # Limit to first 4000 characters to get more content
        if len(full_transcript) > 4000:
            full_transcript = full_transcript[:4000] + "..."
        
        return f"""
Video ID: {video_id}
Video URL: https://www.youtube.com/watch?v={video_id}

Transcript:
{full_transcript}
"""
    except Exception as e:
        return f"""
Error fetching video: {str(e)}

Please provide a valid YouTube video URL or ID. 
Example formats:
- https://www.youtube.com/watch?v=VIDEO_ID
- https://youtu.be/VIDEO_ID
- VIDEO_ID (11 character ID)
"""
