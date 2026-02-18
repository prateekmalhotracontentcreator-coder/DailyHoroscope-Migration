import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminAuthContext = createContext(null);

export const useAdminAuth = () => {
  const context = useContext(AdminAuthContext);
  if (!context) {
    throw new Error('useAdminAuth must be used within AdminAuthProvider');
  }
  return context;
};

export const AdminAuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('admin_token'));

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const storedToken = localStorage.getItem('admin_token');
    if (!storedToken) {
      setLoading(false);
      return;
    }

    try {
      await axios.get(`${API}/admin/verify`, {
        headers: { Authorization: `Bearer ${storedToken}` }
      });
      setIsAuthenticated(true);
      setToken(storedToken);
    } catch (error) {
      localStorage.removeItem('admin_token');
      setIsAuthenticated(false);
      setToken(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    const response = await axios.post(`${API}/admin/login`, {
      username,
      password
    });
    
    if (response.data.success) {
      localStorage.setItem('admin_token', response.data.token);
      setToken(response.data.token);
      setIsAuthenticated(true);
      return true;
    }
    return false;
  };

  const logout = async () => {
    try {
      await axios.post(`${API}/admin/logout`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
    
    localStorage.removeItem('admin_token');
    setToken(null);
    setIsAuthenticated(false);
  };

  const getAuthHeaders = () => ({
    Authorization: `Bearer ${token}`
  });

  return (
    <AdminAuthContext.Provider value={{
      isAuthenticated,
      loading,
      token,
      login,
      logout,
      getAuthHeaders
    }}>
      {children}
    </AdminAuthContext.Provider>
  );
};
