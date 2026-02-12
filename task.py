from crewai import Task
from tools import yt_tool
from agents import blog_researcher,blog_writer,blog_Summary_writer

research_task=Task(
    description=(
        "Extract the transcript and key information from the YouTube video: {topic}. "
        "Analyze the content and identify the main topics, key points, and important insights."
    ),
    expected_output='A comprehensive 3 paragraph summary of the video content with key insights and main topics',
    tools=[yt_tool],
    agent=blog_researcher,
)

write_Task=Task(
    description=(
        "Using the research about the YouTube video {topic}, create an engaging blog post. "
        "Write in a clear, accessible style that explains complex topics simply. "
        "Include an introduction, main content sections, and a conclusion."
    ),
    expected_output='A well structured blog post (300 - 800 words) about the video content with clear sections and engaging narrative',
    tools=[yt_tool],
    agent=blog_writer,
    async_exectuction=False,
    output_file='new-blog-post.md',
)

Summary_task = Task(
    description=(
        "Using the transcript from the YouTube video: {topic}, create a comprehensive summary. "
        "Focus on the main topics discussed, key concepts explained, and important takeaways. "
        "Write in clear, simple language that anyone can understand. "
        "Organize the summary into multiple paragraphs covering different aspects of the video."
    ),
    expected_output='A detailed summary of 200-400 words with multiple paragraphs explaining the video content in simple, accessible language',
    tools=[yt_tool],
    agent=blog_Summary_writer,
    output_file='video-summary.md',
)