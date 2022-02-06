from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# creates a db instance
db = SQLAlchemy()

# connects to db
def connect_db(app):
    db.app = app
    db.init_app(app)

# create db named User
class User(db.Model):

    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"id:{u.id}, first name:{u.first_name}, last name:{u.last_name}, image:{u.image}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    image = db.Column(db.String, nullable=False)
    p = db.relationship("Post" ,  backref ="u")

class Post(db.Model):

    __tablename__ = "posts"

    def __repr__(self):
        p = self
        return f"TITLE: {p.title}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE") )
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(60), nullable=False )
    time = db.Column(db.DateTime(timezone=True), server_default=func.now())
    pt = db.relationship("Post_Tag" , backref ="p")


class Post_Tag(db.Model):
    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE" ), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True )

class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15), unique=True)
    pt = db.relationship("Post_Tag" , backref ="t")