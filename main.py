from crewai import Crew, Process 
from agents import blog_researcher, blog_writer, blog_Summary_writer
from task import research_task, write_Task, Summary_task
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/blog_writter", methods=['POST'])
def run_blog_researcher():
    data = request.get_json()
    topic = data.get('topic')
    
    if not topic:
        return jsonify({"error": "Topic is required"}), 400
    
    crew = Crew(
        agents=[blog_researcher,blog_writer],
        tasks=[research_task,write_Task],
        process=Process.sequential,
        memory=False,
        cache=False,
        max_rpm=100,
        share_crew=True
    )   
    result = crew.kickoff(inputs={'topic': topic})
    return jsonify({"message": "Blog Researcher", "result": str(result)}), 201


@app.route("/Summary", methods=['POST'])
def run_summary_writer():
    data = request.get_json()
    topic = data.get('topic')
    
    if not topic:
        return jsonify({"error": "Topic is required"}), 400
    
    crew = Crew(
        agents=[blog_Summary_writer],
        tasks=[Summary_task],
        process=Process.sequential,
        memory=False,
        cache=False,
        max_rpm=100,
        share_crew=True
    )   
    result = crew.kickoff(inputs={'topic': topic})
    return jsonify({"message": "Summary writer", "result": str(result)}), 201


if __name__ == "__main__":
    app.run()
