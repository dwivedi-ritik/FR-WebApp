from flask import Flask, render_template, request, flash , redirect, send_file , url_for , send_from_directory
from flask_login import  login_required , login_user , logout_user , current_user 
from werkzeug.security import generate_password_hash , check_password_hash

from extensions import db , login_manager , SECRET_KEY , DB_URI
from models import User
from face_reco import start_capturing
from utils import get_date

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["UPLOAD_FOLDER"] = "Attendence lists"
db.init_app(app)

login_manager.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect("user")

    return render_template("index.html" , current_user=current_user)


@app.route("/login" , methods=["GET" , "POST"]) 
def login():
    if request.method == "POST":
        email = request.form.get("email") 
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash("No email registered")
 
        elif not check_password_hash(user.password, password):
            flash("Password mismatched")
        
        else:
            login_user(user)
            return redirect(url_for('profile'))

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email") 
        name = request.form.get("name")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email is already registered")
        else:
            try:
                hashed_password = generate_password_hash(password)
                new_user = User(email=email , password=hashed_password , name=name)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('profile'))
            except Exception:
                flash("Error occured during creating user")

    return render_template("signup.html")


@app.route("/user" , methods=["GET" , "POST"])
@login_required
def profile():
    if request.method == "POST":
        return redirect(url_for("attendance"))
    name = current_user.name
    return render_template("profile.html" , name=name.title())

@app.route("/user/attendance")
@login_required
def attendance():
    user_folder = f"./Attendence lists/{current_user.id}"
    start_capturing(user_folder=user_folder)
    file_url = get_date()
    return render_template("attendance.html" , name=current_user.name.title() , file_url=file_url)

@app.route("/user/download/<string:file_url>")
@login_required
def download(file_url):
    return send_from_directory( app.config["UPLOAD_FOLDER"] + "/" + str(current_user.id)  , file_url , as_attachment=True)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
