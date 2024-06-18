import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    fetch('/api/videos')
      .then(response => response.json())
      .then(data => setVideos(data));
  }, []);

  return (
    <div className="container mx-auto mt-8">
      <h1 className="text-3xl font-bold mb-6">Welcome to Meykhana Video Platform</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {videos.map(video => (
          <div key={video.id} className="bg-white shadow-md rounded-lg overflow-hidden">
            <video className="w-full h-48" controls>
              <source src={`/uploads/${video.file_path}`} type="video/mp4" />
            </video>
            <div className="p-4">
              <h2 className="text-xl font-bold mb-2">
                <Link to={`/video/${video.id}`}>{video.title}</Link>
              </h2>
              <p className="text-gray-700">{video.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
