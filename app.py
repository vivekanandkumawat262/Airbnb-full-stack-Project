from flask import Flask, render_template, request, flash,redirect,url_for,session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_mail import Mail, Message
import random

app = Flask(__name__)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '23f2004577@gmail.com'
app.config['MAIL_PASSWORD'] = 'cgbrnxynglmikwuq'

mail = Mail(app)


app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///vivek.sqlite'
app.config['SECRET_KEY'] = 'your_secret_key'


db.init_app(app)

 

@app.route("/")
def Home():
    return render_template("home1.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        code = str(random.randint(100000, 999999))
        try:
            first_name = request.form['first_name'] 
            last_name = request.form['last_name']
            dob = request.form['dob']
            email = request.form['email']
            password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')


            marketing_opt_out = request.form.get('terms')
            print(marketing_opt_out)
            if marketing_opt_out:
                print("User does NOT want marketing emails")
            else:
                print("User allows marketing emails", marketing_opt_out)
                marketing_opt_out="User allows marketing emails"

            new_user = User(first_name=first_name, last_name=last_name, dob=dob, email =email , password=password,  marketing_opt_out= marketing_opt_out,verification_code=code)
            db.session.add(new_user)
            db.session.commit()
            # send email
            # msg = Message(
            #     "Your Verification Code",
            #     sender="23f2004577@gmail.com",
            #     recipients=[new_user.email]
            # )
            # msg.body = f"Your verification code is {code}"
            # print("before email sended")
            # mail.send(msg)
            # print("email sended")

            # session['verify_email'] = new_user.email

            # return redirect(url_for("verify"))
            return redirect(url_for("user_login"))
        except Exception as e:
            db.session.rollback()
            print("Error:", e)
            print("Registration failed")
            flash("Registration failed")
            return redirect(url_for("register"))

    return render_template("home1.html")

# @app.route("/verify", methods=["GET", "POST"])
# def verify():

#     if request.method == "POST":
#         code = request.form['code']
#         email = session.get('verify_email')

#         user = User.query.filter_by(email=email).first()

#         if user and user.verification_code == code:
#             user.is_verified = True
#             user.verification_code = None
#             db.session.commit()

#             flash("Account verified successfully!")
#             return redirect(url_for("user_login"))

#         flash("Invalid verification code")

#     return render_template("verify.html")




@app.route("/user_login", methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password) and user.role == "User":
            # if user.blocked:
            #     flash("Your account is blocked. Please contact the administrator.", "danger")
            #     return redirect(url_for('user_login'))
            
            # login_user(user)  # Flask-Login: Log in the user
            flash('Login successful!')
            print("sample.html")
            return redirect(url_for('user_after_dashboard', name=email))
        else:
            flash('Invalid username or password. Please try again.')
            print("user_login")
            return redirect(url_for('user_login'))

    return render_template("userdashboard.html", role='User')



@app.route("/user_dashboard", methods=['GET'])
def user_dashboard():
    return render_template("userdashboard.html")

@app.route("/user_after_dashboard/<string:name>", methods=['GET'])
def user_after_dashboard(name):
    return render_template("home1.html",name=name)




# @app.route("/testmail")
# def testmail():
#     msg = Message(
#         "Test Mail",
#         sender="23f2004577@gmail.com",
#         recipients=["vivekanandkumawat261@gmail.com"]
#     )
#     msg.body = "Mail working!"
#     mail.send(msg)
#     return "Mail sent"


def func():
    try:
        admin = User.query.filter_by(first_name="admin").first()
        print("1")
        if not admin:
            admin = User(
                first_name='admin',
                last_name='auth',
                password=generate_password_hash(
                    'admin123',
                    method='pbkdf2:sha256'
                ),
                dob=date(2000, 1, 1),   
                email='admin@gmail.com',
                role="Admin"
            )

            db.session.add(admin)
            db.session.commit()

            return "success"

        else:
            return "fail"

    except Exception as e:
        db.session.rollback()
        print("Error:", e)
        return "error"

with app.app_context():
    db.create_all()
    func()

if __name__ == "__main__":
    app.run(debug=True)

 