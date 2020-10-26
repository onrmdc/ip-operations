from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "ip address:"

if __name__ =='__main__':
    app.run(debug=True)