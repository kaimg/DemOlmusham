import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext'; // Make sure to adjust the path to AuthContext based on your project structure

const Navbar = () => {
  const { auth, logout } = useContext(AuthContext); // Assuming you have these in your context

  return (
    <nav className="bg-gray-800 p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-white text-lg font-bold">Meykhana Platform</Link>
        <div>
          <Link to="/" className="text-gray-300 hover:text-white px-3">Home</Link>
          {auth ? (
            <>
              <Link to="/upload" className="text-gray-300 hover:text-white px-3">Upload Video</Link>
              <button onClick={logout} className="text-gray-300 hover:text-white px-3">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-gray-300 hover:text-white px-3">Login</Link>
              <Link to="/register" className="text-gray-300 hover:text-white px-3">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
