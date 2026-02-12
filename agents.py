from crewai import Agent, LLM
from tools import yt_tool
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = LLM(
    model="groq/llama-3.1-8b-instant",  # Smaller, faster model
    api_key=os.getenv("GROQ_API_KEY")
)

blog_researcher=Agent(
    role='Blog Researcher from Youtube Videos',
    goal='Extract and analyze content from the YouTube video: {topic}',
    verbose=True,
    memory=False,
    backstory="Expert in understanding videos in AI, Data Science, Machine learning, Generative AI and extracting key insights",
    llm=llm,
    tools=[yt_tool],
    allow_delegation=True
)


blog_writer=Agent(
    role='Blog Writer',
    goal='Create a compelling blog post about the YouTube video: {topic}',
    verbose=True,
    memory=False,
    backstory=(
        "With a flair for simplifying complex topics, you craft "
        "engaging narratives that captivate and educate, bringing new "
        "discoveries to light in an accessible manner"
    ),
    llm=llm,
    tools=[yt_tool],
    allow_delegation=False
)

blog_Summary_writer = Agent(
    role='YouTube Video Summary Specialist',
    goal='Generate a clear, concise, and structured summary of the YouTube video on: {topic}',
    verbose=True,
    memory=False,
    backstory=(
        "You are an expert content summarizer specializing in transforming "
        "long-form video content into well-structured, informative, and easy-to-read summaries. "
        "You extract key insights, main arguments, important examples, and conclusions "
        "while eliminating unnecessary details. Your summaries are accurate, "
        "engaging, and professionally written."
    ),
    llm=llm,
    tools=[yt_tool],
    allow_delegation=False
)
