#
# A simple Flask CRUD with login
#
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required, current_user
from flask_login import LoginManager, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["DEBUG"] = True

################################
# SETUP THE MySQL DATABASE ORM #
################################

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="guajiropa",
    password="bobouser23",
    hostname="guajiropa.mysql.pythonanywhere-services.com",
    databasename="guajiropa$comments",
    )
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#####################
# SETUP FLASK-LOGIN #
#####################
app.secret_key = "br55c!8525vv34fe76895"
login_manager = LoginManager()
login_manager.init_app(app)


#########################
# DATA MODELS & CLASSES #
#########################

class User(UserMixin):

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.username


# Test data for testing the login
all_users = {
    "admin": User("admin", generate_password_hash("secret")),
    "bob": User("bob", generate_password_hash("less-secret")),
    "caroline": User("caroline", generate_password_hash("completely-secret")),
}

@login_manager.user_loader
def load_user(user_id):
    return all_users.get(user_id)


class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))


###################
# ROUTING SECTION #
###################

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("comments.html", comments=Comment.query.all(),
                                timestamp=datetime.now())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    comment = Comment(content=request.form["contents"])
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/update', methods=["POST"])
def update():
    try:
        newcontent = request.form.get("newcontent")
        oldcontent = request.form.get("oldcontent")
        comment = Comment.query.filter_by(content=oldcontent).first()
        comment.content = newcontent
        db.session.commit()
    except Exception as e:
        print("Could not update book title!")
        print(e)

    return redirect(url_for('index'))


@app.route('/delete', methods=["POST"])
def delete():
    try:
        content = request.form.get("content")
        comment = Comment.query.filter_by(content=content).first()
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return "Could not delete this comment! {}".format(e)


@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    username = request.form["username"]

    if  username not in all_users:
        return render_template("login_page.html", error=True)
    user = all_users[username]

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('index'))


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))








