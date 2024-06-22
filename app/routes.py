from flask import Blueprint, request, jsonify, send_from_directory, current_app
from .models import Video, Comment, User
from . import db, bcrypt
from flask_login import current_user
import os
from werkzeug.utils import secure_filename
from .jwt_utils import encode_auth_token, token_required

main = Blueprint('main', __name__)

@main.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'})

@main.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        token = encode_auth_token(user.id)
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials!'}), 401

@main.route('/api/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({'message': f'Hello, user {current_user}'})


@main.route('/api/videos', methods=['GET'])
def get_videos():
    videos = Video.query.all()
    return jsonify([video.to_dict() for video in videos])

@main.route('/api/videos/<int:video_id>', methods=['GET'])
def get_video(video_id):
    video = Video.query.get_or_404(video_id)
    comments = Comment.query.filter_by(video_id=video_id).all()
    return jsonify({
        'video': video.to_dict(),
        'comments': [comment.to_dict() for comment in comments]
    })

@main.route('/api/upload', methods=['POST'])
def upload_video():
    title = request.form['title']
    description = request.form['description']
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    video = Video(title=title, description=description, file_path=filename, user_id=current_user.id)
    db.session.add(video)
    db.session.commit()

    return jsonify(video.to_dict())

@main.route('/api/videos/<int:video_id>/comments', methods=['POST'])
def post_comment(video_id):
    body = request.json['body']
    comment = Comment(body=body, video_id=video_id, user_id=current_user.id)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict())

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
