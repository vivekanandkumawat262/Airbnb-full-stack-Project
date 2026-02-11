from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///vivek.sqlite'
app.config['SECRET_KEY'] = 'your_secret_key'


db.init_app(app)

 

@app.route("/")
def Home():
    return render_template("home1.html")

if __name__ == "__main__":
    app.run(debug=True)

 