from flask import Flask, render_template, request
from google import genai
from pydantic import BaseModel
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/gemini", methods = ["POST"])
def gemini():
    class Recipe(BaseModel):
        recipe_name: str
        ingredients: list[str]

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    food_love = request.form["food_love"]
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{food_love}を使った料理を教えてください",
        config={
            "response_mime_type": "application/json",
            "response_schema": list[Recipe],
        },
    )
    # Use the response as a JSON string.
    print(response.text)

    return response.text