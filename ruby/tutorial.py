from flask import Flask

app = Flask(__name__)


# This code can be successfully run with (from ruby folder) flask --app tutorial run from the terminal
@app.route("/")  # note this is just a decorator
def hello_world():
    return "<p> Hello World </p>"  # we can return html as we have done here
