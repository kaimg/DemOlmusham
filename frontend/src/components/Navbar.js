import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-gray-800 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-white text-lg font-bold">Meykhana Platform</Link>
        <div>
          <Link to="/" className="text-gray-300 hover:text-white px-3">Home</Link>
          <Link to="/upload" className="text-gray-300 hover:text-white px-3">Upload Video</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
