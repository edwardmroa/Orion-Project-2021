from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def dashboard():
    
    return "Home"


if (__name__=="__main__"):
    app.run(debug=True)