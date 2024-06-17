from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.models import User, Video, Comment
from app.forms import VideoForm, CommentForm

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = VideoForm()
    comment_form = CommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
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
    videos = Video.query.order_by(Video.timestamp.desc()).all()
    recent_comments = Comment.query.order_by(Comment.timestamp.desc()).limit(5).all()
    return render_template('index.html', form=form, comment_form=comment_form, videos=videos, recent_comments=recent_comments)

@main.route('/upload_video', methods=['POST'])
@login_required
def upload_video():
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
    flash('Error in uploading video')
    return redirect(url_for('main.index'))

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
