from crewai import Crew, Process
from agents import blog_researcher, blog_writer, blog_Summary_writer
from task import research_task, write_Task, Summary_task
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from litellm.exceptions import RateLimitError
import traceback


app = Flask(__name__)
CORS(app)


@app.route("/blog_writter", methods=["POST"])
def run_blog_researcher():
    data = request.get_json()
    topic = data.get("topic")

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    crew = Crew(
        agents=[blog_researcher, blog_writer],
        tasks=[research_task, write_Task],
        process=Process.sequential,
        memory=False,
        cache=False,
        max_rpm=100,
        share_crew=True,
    )
    
    # Retry logic with exponential backoff
    max_retries = 3
    retry_delay = 15
    
    for attempt in range(max_retries):
        try:
            result = crew.kickoff(inputs={"topic": topic})
            return (
                jsonify(
                    {
                        "agent": "Blog Writer Agent",
                        "task": write_Task.description.replace("{topic}", topic),
                        "final_answer": str(result),
                    }
                ),
                201,
            )
        except Exception as e:
            error_str = str(e).lower()
            # Check if it's a rate limit error
            if "rate limit" in error_str or "ratelimiterror" in error_str or isinstance(e, RateLimitError):
                if attempt < max_retries - 1:
                    print(f"Rate limit hit. Waiting {retry_delay} seconds before retry {attempt + 2}/{max_retries}...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    return jsonify({
                        "error": "Rate limit exceeded. Please try again in a few moments.",
                        "details": str(e)
                    }), 429
            else:
                # Non-rate-limit error
                print(f"Error occurred: {str(e)}")
                traceback.print_exc()
                return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
    # If we exhausted all retries
    return jsonify({"error": "Maximum retries exceeded"}), 500


@app.route("/Summary", methods=["POST"])
def run_summary_writer():
    data = request.get_json()
    topic = data.get("topic")

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    crew = Crew(
        agents=[blog_Summary_writer],
        tasks=[Summary_task],
        process=Process.sequential,
        memory=False,
        cache=False,
        max_rpm=100,
        share_crew=True,
    )

    # Retry logic with exponential backoff
    max_retries = 3
    retry_delay = 15  # Start with 15 seconds as suggested by the error
    
    for attempt in range(max_retries):
        try:
            result = crew.kickoff(inputs={"topic": topic})
            return (
                jsonify(
                    {
                        "agent": "Video Summary Agent",
                        "task": Summary_task.description.replace("{topic}", topic),
                        "final_answer": str(result),
                    }
                ),
                200,
            )
        except Exception as e:
            error_str = str(e).lower()
            # Check if it's a rate limit error
            if "rate limit" in error_str or "ratelimiterror" in error_str or isinstance(e, RateLimitError):
                if attempt < max_retries - 1:
                    print(f"Rate limit hit. Waiting {retry_delay} seconds before retry {attempt + 2}/{max_retries}...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    return jsonify({
                        "error": "Rate limit exceeded. Please try again in a few moments.",
                        "details": str(e)
                    }), 429
            else:
                # Non-rate-limit error
                print(f"Error occurred: {str(e)}")
                traceback.print_exc()
                return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
    # If we exhausted all retries
    return jsonify({"error": "Maximum retries exceeded"}), 500


@app.route("/Research", methods=["POST"])
def run_research_writer():
    data = request.get_json()
    topic = data.get("topic")

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    crew = Crew(
        agents=[blog_researcher],
        tasks=[research_task],
        process=Process.sequential,
        memory=False,
        cache=False,
        max_rpm=100,
        share_crew=True,
    )

    # Retry logic with exponential backoff
    max_retries = 3
    retry_delay = 15  # Start with 15 seconds as suggested by the error
    
    for attempt in range(max_retries):
        try:
            result = crew.kickoff(inputs={"topic": topic})
            return (
                jsonify(
                    {
                        "agent": "Video Research Agent",
                        "task": research_task.description.replace("{topic}", topic),
                        "final_answer": str(result),
                    }
                ),
                200,
            )
        except Exception as e:
            error_str = str(e).lower()
            # Check if it's a rate limit error
            if "rate limit" in error_str or "ratelimiterror" in error_str or isinstance(e, RateLimitError):
                if attempt < max_retries - 1:
                    print(f"Rate limit hit. Waiting {retry_delay} seconds before retry {attempt + 2}/{max_retries}...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    return jsonify({
                        "error": "Rate limit exceeded. Please try again in a few moments.",
                        "details": str(e)
                    }), 429
            else:
                # Non-rate-limit error
                print(f"Error occurred: {str(e)}")
                traceback.print_exc()
                return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
    # If we exhausted all retries
    return jsonify({"error": "Maximum retries exceeded"}), 500


if __name__ == "__main__":
    app.run()
