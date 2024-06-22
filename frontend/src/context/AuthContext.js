import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['x-access-token'] = token;
      setAuth({ token });
    }
  }, []);

  const login = async (email, password) => {
    const response = await axios.post('/api/login', { email, password });
    const { token } = response.data;
    localStorage.setItem('token', token);
    axios.defaults.headers.common['x-access-token'] = token;
    setAuth({ token });
  };

  const logout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['x-access-token'];
    setAuth(null);
  };

  return (
    <AuthContext.Provider value={{ auth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };
