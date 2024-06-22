import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import UploadPage from './pages/UploadPage';
import { AuthProvider, AuthContext } from './context/AuthContext';
import './index.css';

const ProtectedRoute = ({ element }) => {
  const { auth } = React.useContext(AuthContext);
  return auth ? element : <Navigate to="/login" />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/upload" element={<ProtectedRoute element={<UploadPage />} />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
