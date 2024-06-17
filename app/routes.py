from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, send_from_directory
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import User, Video, Comment
from app.forms import VideoForm, CommentForm

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    comment_form = CommentForm()
    videos = Video.query.order_by(Video.timestamp.desc()).all()
    recent_comments = Comment.query.order_by(Comment.timestamp.desc()).limit(5).all()
    return render_template('index.html', comment_form=comment_form, videos=videos, recent_comments=recent_comments)

@main.route('/forum')
def forum():
    comment_form = CommentForm()
    videos = Video.query.order_by(Video.timestamp.desc()).all()
    recent_comments = Comment.query.order_by(Comment.timestamp.desc()).limit(5).all()
    return render_template('forum.html', comment_form=comment_form, videos=videos, recent_comments=recent_comments)

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = VideoForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(file_path)
        video = Video(
            title=form.title.data,
            description=form.description.data,
            file_path=filename,  # Store only the filename
            user_id=current_user.id
        )
        db.session.add(video)
        db.session.commit()
        flash('Your video has been uploaded.')
        return redirect(url_for('main.index'))
    return render_template('upload.html', form=form)

@main.route('/video/<int:video_id>', methods=['GET', 'POST'])
def video(video_id):
    video = Video.query.get_or_404(video_id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(
            body=comment_form.body.data,
            user_id=current_user.id,
            video_id=video.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted.')
        return redirect(url_for('main.video', video_id=video.id))
    return render_template('video.html', video=video, comment_form=comment_form)

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

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
    return redirect(url_for('main.video', video_id=video_id))
