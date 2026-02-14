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
    expected_output='A well structured blog post (500 - 800 words) about the video content with clear sections and engaging narrative',
    tools=[yt_tool],
    agent=blog_writer,
    async_exectuction=False,
    # output_file='new-blog-post.md',
)

Summary_task = Task(
    description=(
        "1. First, use the yt_tool to get the transcript from the YouTube video: {topic}\n"
        "2. Then, analyze the transcript and write a comprehensive summary covering:\n"
        "   - Main topics and themes discussed\n"
        "   - Key concepts and explanations\n"
        "   - Important takeaways and conclusions\n"
        "3. Write in clear, simple language organized into 3-5 paragraphs.\n"
        "4. Do NOT call any more tools after getting the transcript - just write the summary."
    ),
    expected_output=(
        'A detailed summary of 200-400 words with 3-5 well-structured paragraphs that explain '
        'the video content in simple, accessible language. The summary should be complete and ready to present.'
    ),
    tools=[yt_tool],
    agent=blog_Summary_writer,
    # output_file='video-summary.md',
)