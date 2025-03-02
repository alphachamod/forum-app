# views/forum.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Post, Topic, db
from helpers.security_helper import SecurityHelper  # Import SecurityHelper

forum_bp = Blueprint('forum', __name__)

@forum_bp.route('/')
def forum():
    topics = Topic.query.all()
    return render_template('forum.html', topics=topics)

@forum_bp.route('/topic/<int:topic_id>')
def topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    posts = topic.posts
    return render_template('topic.html', topic=topic, posts=posts)

@forum_bp.route('/new_topic', methods=['GET', 'POST'])
def new_topic():
    if request.method == 'POST':
        title = request.form['title']

        # Insecure: No Input Validation and Insecure Authorization checks
        new_topic = Topic(title=title, user_id=1)  # Hardcoded User for simplicity

        db.session.add(new_topic)
        db.session.commit()

        flash('Topic Created!', 'success')
        return redirect(url_for('forum.forum'))

    return render_template('new_topic.html')

@forum_bp.route('/new_post/<int:topic_id>', methods=['GET', 'POST'])
def new_post(topic_id):
    if request.method == 'POST':
        content = request.form['content']

        # Insecure: SQL Injection vulnerability!
        # posts = Post.query.filter(Post.content.like("what%")).all()

        # VULNERABLE
        query = "SELECT * FROM post WHERE content LIKE '%" + content + "%'"

        # Insecure: No authorization check
        new_post = Post(content=content, topic_id=topic_id, user_id=1)

        db.session.add(new_post)
        db.session.commit()

        flash('Post Created!', 'success')
        return redirect(url_for('forum.topic', topic_id=topic_id))

    return render_template('new_post.html', topic_id=topic_id)