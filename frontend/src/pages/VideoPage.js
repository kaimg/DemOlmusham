import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const VideoPage = () => {
  const { id } = useParams();
  const [video, setVideo] = useState(null);
  const [comments, setComments] = useState([]);
  const [comment, setComment] = useState('');

  useEffect(() => {
    fetch(`/api/videos/${id}`)
      .then(response => response.json())
      .then(data => {
        setVideo(data.video);
        setComments(data.comments);
      });
  }, [id]);

  const handleCommentSubmit = (e) => {
    e.preventDefault();
    fetch(`/api/videos/${id}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ body: comment }),
    })
    .then(response => response.json())
    .then(data => {
      setComments([...comments, data]);
      setComment('');
    });
  };

  if (!video) return <div>Loading...</div>;

  return (
    <div className="container mx-auto mt-8">
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <div className="relative">
          <video id="custom-video" className="w-full h-64" controls>
            <source src={`/uploads/${video.file_path}`} type="video/mp4" />
          </video>
        </div>
        <div className="p-4">
          <h2 className="text-2xl font-bold mb-2">{video.title}</h2>
          <p className="text-gray-700 mb-4">{video.description}</p>
          <h3 className="text-xl font-bold mb-2">Comments</h3>
          <ul>
            {comments.map(comment => (
              <li key={comment.id} className="mb-2">
                <strong>{comment.user.username}:</strong> {comment.body}
              </li>
            ))}
          </ul>
          <form onSubmit={handleCommentSubmit} className="mt-4">
            <textarea
              className="w-full border rounded p-2 mb-2"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              required
            ></textarea>
            <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">Submit</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default VideoPage;
