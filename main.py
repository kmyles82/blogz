from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime)
    body = db.Column(db.Text)

@app.route('/blog')
def index():
    posts = Blog.query.order_by(Blog.date_posted.asc()).all()

    return render_template('blog.html', posts=posts)

@app.route('/post')
def post(post_id):
    post = Blog.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)

@app.route('/newpost')
def add():
    return render_template('newpost.html')

@app.route('/newpost', methods=['POST'])
def addpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if title == '' or body == '':
            flash("Title or body cannot be empty")
            return render_template('newpost.html')

    post = Blog(title=title,  body=body, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect('blog')

if __name__ == '__main__':
    app.run(debug=True)