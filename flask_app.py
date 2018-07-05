
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

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

###############
# DATA MODELS #
###############

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
        return render_template("comments.html", comments=Comment.query.all())

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


@app.route("/delete", methods=["POST"])
def delete():
    try:
        content = request.form.get("content")
        comment = Comment.query.filter_by(content=content).first()
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return "Could not delete this comment! {}".format(e)



