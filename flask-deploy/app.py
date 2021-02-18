
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Flask Project which will be deploy on nginx!</h1>"


@app.route("/new")
def hello_new():
    return "<h1 style='color:blue'>New Flask Project which will be deploy on nginx!</h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
