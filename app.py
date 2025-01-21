from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

# Define an endpoint that returns a random number as a JSON object
@app.route("/random")
def random_number():
    import random
    response = {
        'randomNumber': random.randint(1, 100)
    }
    return response