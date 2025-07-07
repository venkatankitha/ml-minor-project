from flask import Flask, request, jsonify
import openai

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API Key
openai.api_key = "your-openai-api-key"

# Function to generate personalized questions
def generate_quiz(topic, skill_level):
    prompt = f"""
    You are an intelligent tutoring system. Create a set of 3 personalized quiz questions 
    for a user who wants to learn about "{topic}". The user's skill level is "{skill_level}". 
    Ensure the questions vary in difficulty and provide correct answers.

    Format:
    1. Question 1
       a. Option 1
       b. Option 2
       c. Option 3 (correct)
    2. Question 2
       a. Option 1
       b. Option 2 (correct)
       c. Option 3
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Route to handle quiz generation
@app.route("/generate_quiz", methods=["POST"])
def quiz():
    data = request.get_json()
    topic = data.get("topic", "general knowledge")
    skill_level = data.get("skill_level", "beginner")
    
    quiz = generate_quiz(topic, skill_level)
    return jsonify({"quiz": quiz})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)









