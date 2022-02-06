from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, Post_Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Blog'
app.config['SQLALCHEMY_TRACK_MODIFACTION'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oops"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# Home
@app.route('/')
def home():
    return render_template("home.html")

# list all users
@app.route('/user')
def user_list():
    u = User.query.all()
    return render_template("user.html", u=u)

# list all tags
@app.route('/tag')
def Tag_list():
    t = Tag.query.all()
    return render_template("tag.html", t=t)

# details of user
@app.route('/user/<user_id>')
def user_detail(user_id):
    u = User.query.get_or_404(user_id)
    return render_template("user_details.html", u=u)

# Create Tag
@app.route('/tag/create')
def create_tag():
    return render_template("create_tag.html")

# Edit Tag
@app.route('/tag/<tag_id>/edit')
def edit_tag(tag_id):
    tg = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tg=tg)

@app.route('/tag/<tag_id>/')
def Tag_detail(tag_id):
    tg = Tag.query.get_or_404(tag_id)
    return render_template("tag_details.html", tg=tg)

# create a new user
@app.route('/user/create')
def create_user():
    return render_template("create_user.html")

# edit user info
@app.route('/user/<user_id>/edit')
def edit_user(user_id):
    u = User.query.get_or_404(user_id)
    return render_template("edit_user.html", u=u)

# make a post
@app.route('/user/<user_id>/post')
def user_post(user_id):
    u = User.query.get_or_404(user_id)
    t = Tag.query.all()
    k = list(t)
    return render_template("post.html", u=u, t=t, list=len(k))

# Post Details
@app.route('/user/<user_id>/post/<post_id>')
def post_detail(post_id, user_id):
    p = Post.query.get_or_404(post_id)
    u = User.query.get_or_404(user_id)

    #gets all tags


    return render_template("post_details.html", p=p, u=u)

# Edit post
@app.route('/user/<user_id>/post/<post_id>/edit')
def Edit_Post(post_id, user_id):
    p = Post.query.get_or_404(post_id)
    u = User.query.get_or_404(user_id)
    return render_template("edit_post.html", p=p, u=u)

# post create user
@app.route('/user/create', methods = ["POST"])
def submit_user():
    fname = request.form["Fname"]
    lname = request.form["Lname"]
    img = request.form["Img"]
    u = User(first_name=fname, last_name=lname, image=img)
    db.session.add(u)
    db.session.commit()
    return redirect("/")

# post delete user
@app.route('/user/<user_id>', methods = ["POST"])
def Delete_detail(user_id):
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect("/")

# post edit user
@app.route('/user/<user_id>/edit', methods = ["POST"])
def Submit_edit(user_id):
    u = User.query.get_or_404(user_id)
    fname = request.form["Fname"]
    lname = request.form["Lname"]
    img = request.form["Img"]
    u.first_name = fname
    u.last_name = lname
    u.image = img
    db.session.add(u)
    db.session.commit()
    return redirect(f"/user/{u.id}")

# submit post
@app.route('/user/<user_id>/post', methods = ["POST"])
def submit_post(user_id):
    tag = Tag.query.all()
    Post_id = user_id
    Title = request.form["Title"]
    Content = request.form["Content"]
    p = Post(post_id=int(Post_id), title=Title.upper(), content=Content)
    db.session.add(p)
    db.session.commit()
    for i in range(0,len(list(tag))):
        temp = request.form[f"T{i}"]
        if temp == "on":
            pt = Post_Tag(post_id=p.id, tag_id=tag[i].id)
            db.session.add(pt)
            db.session.commit()
    return redirect(f"/user/{user_id}")

# delete Post >>>>> Todo fix error >>> deleting user not post
@app.route('/user/<user_id>/post/<post_id>', methods =["POST"])
def Delete_post(post_id,user_id):
    u = User.query.get_or_404(user_id)
    Post.query.filter_by(id = post_id).delete()
    db.session.commit()
    return redirect(f"/user/{u.id}")

# edit post post
@app.route('/user/<user_id>/post/<post_id>/edit', methods =["POST"])
def P_Edit_post(post_id,user_id):
    u = User.query.get_or_404(user_id)
    p = Post.query.get_or_404(post_id)
    Post_id = user_id
    Title = request.form["Title"]
    Content = request.form["Content"]
    p.title = Title.upper()
    p.content = Content
    db.session.add(p)
    db.session.commit()
    return redirect(f"/user/{u.id}/post/{p.id}")

# create tag
@app.route('/tag/create', methods =["POST"])
def P_create_tag():
    name = request.form["Tag"]
    t = Tag(name = name.upper())
    db.session.add(t)
    db.session.commit()
    return redirect("/tag")

# Edit tag post
@app.route('/tag/<tag_id>/edit', methods =["POST"])
def P_Edit_tag(tag_id):
    tg = Tag.query.get_or_404(tag_id)
    name = request.form["Tag"]
    tg.name = name.upper()
    db.session.commit()
    return redirect(f"/tag/{tag_id}")

# Delete Tag
@app.route('/tag/<tag_id>', methods = ["POST"])
def P_Delete_tag(tag_id):
    tg = Tag.query.get_or_404(tag_id)
    Tag.query.filter_by(id = tag_id).delete()
    db.session.commit()
    return redirect("/tag")




