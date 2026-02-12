from crewai import Crew,Process 
from agents import blog_researcher,blog_writer,blog_Summary_writer
from task import research_task,write_Task,Summary_task

crew=Crew(
    agents=[blog_researcher,blog_writer],
    tasks=[research_task,write_Task],
    process=Process.sequential,
    memory=False,  # Disable memory to avoid OpenAI embeddings
    cache=False,   # Disable cache to avoid OpenAI embeddings
    max_rpm=100,
    share_crew=True
)

result=crew.kickoff(inputs={'topic':"https://www.youtube.com/watch?v=_NLHFoVNlbg&list=PLoROMvodv4rNRRGdS0rBbXOUGA0wjdh1X"})
print(result)