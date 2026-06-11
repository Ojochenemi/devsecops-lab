# Just addint a comment.
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
PREFIX = os.environ.get("GREETING_PREFIX", "Hello")

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/greet")
def greet():
    name = request.args.get("name", "World")
    return jsonify(message=f"{PREFIX}, {name}!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
# test bad code
def bad_function():
    user_input = "test"
    eval(user_input)
