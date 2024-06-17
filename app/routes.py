from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.models import User, Video, Comment
from app.forms import VideoForm, CommentForm
import re

main = Blueprint('main', __name__)

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    Supports URLs like:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    """
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    match = re.match(youtube_regex, url)
    return match.group(6) if match else None

@main.route('/', methods=['GET', 'POST'])
def index():
    comment_form = CommentForm()
    videos = Video.query.order_by(Video.timestamp.desc()).all()
    recent_comments = Comment.query.order_by(Comment.timestamp.desc()).limit(5).all()
    return render_template('index.html', comment_form=comment_form, videos=videos, recent_comments=recent_comments, extract_video_id=extract_video_id)

@main.route('/forum')
def forum():
    comment_form = CommentForm()
    videos = Video.query.order_by(Video.timestamp.desc()).all()
    recent_comments = Comment.query.order_by(Comment.timestamp.desc()).limit(5).all()
    return render_template('forum.html', comment_form=comment_form, videos=videos, recent_comments=recent_comments, extract_video_id=extract_video_id)

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = VideoForm()
    if form.validate_on_submit():
        video = Video(
            title=form.title.data,
            description=form.description.data,
            url=form.url.data,
            user_id=current_user.id
        )
        db.session.add(video)
        db.session.commit()
        flash('Your video has been uploaded.')
        return redirect(url_for('main.index'))
    return render_template('upload.html', form=form)

@main.route('/comment/<int:video_id>', methods=['POST'])
@login_required
def comment(video_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            body=form.body.data,
            user_id=current_user.id,
            video_id=video_id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted.')
    return redirect(url_for('main.index'))
