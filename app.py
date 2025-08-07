import redis
from flask import Flask, redirect, request, url_for

app = Flask(__name__)
r = redis.Redis(host="redis", port=6379)


OPTIONS = ["Reem", "Buthaina"]


@app.route("/", methods=["GET"])
def index():
    votes = {option: int(r.get(option) or 0) for option in OPTIONS}
    return f"""
    <h1>Vote for your favorite devopes engineer</h1>
    <form method="POST" action="/vote">
        <button type="submit" name="vote" value="Reem">Reem</button>
        <button type="submit" name="vote" value="Buthaina">Buthaina</button>
    </form>
    <h2>Current Results</h2>
    <ul>
        <li>Reem: {votes['Reem']}</li>
        <li>Buthaina: {votes['Buthaina']}</li>
    </ul>
    """


@app.route("/vote", methods=["POST"])
def vote():
    option = request.form.get("vote")
    if option in OPTIONS:
        r.incr(option)
    return redirect(url_for("index"))
