import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from '../utils/axios';
import { AuthContextType } from '../hooks/useAuth';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  profile: {
    avatar?: string;
    age: number;
    height: number;
    weight: number;
    gender: string;
    fitness_level: string;
  };
}

export const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('access_token'));

  const checkAuth = async () => {
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!accessToken && !refreshToken) {
      setLoading(false);
      return;
    }

    try {
      const response = await axios.get('/api/auth/user/');
      setUser(response.data);
      setIsAuthenticated(true);
      setToken(accessToken);
    } catch (error: any) {
      if (error.response?.status === 401 && refreshToken) {
        try {
          const refreshResponse = await axios.post('/api/auth/refresh/', {
            refresh: refreshToken,
          });
          
          const { access } = refreshResponse.data;
          localStorage.setItem('access_token', access);
          axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
          
          // Retry getting user data with new token
          const userResponse = await axios.get('/api/auth/user/');
          setUser(userResponse.data);
          setIsAuthenticated(true);
          setToken(access);
        } catch (refreshError) {
          handleAuthFailure();
        }
      } else {
        handleAuthFailure();
      }
    } finally {
      setLoading(false);
    }
  };

  const handleAuthFailure = () => {
    setUser(null);
    setIsAuthenticated(false);
    setToken(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    delete axios.defaults.headers.common['Authorization'];
  };

  useEffect(() => {
    checkAuth();
  }, []);

  const login = async (username: string, password: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('/api/auth/login/', { username, password });
      const { user: userData, access } = response.data;
      
      // Set the token in axios defaults
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      setUser(userData);
      setIsAuthenticated(true);
      setToken(access);
      
      // Store tokens and user data
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', response.data.refresh);
      localStorage.setItem('user', JSON.stringify(userData));
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'An error occurred during login';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        throw new Error('No refresh token found');
      }

      try {
        await axios.post('/api/auth/logout/', { refresh: refreshToken });
      } catch (error) {
        console.error('Error during logout request:', error);
        // Continue with cleanup even if the request fails
      }

      // Clean up regardless of logout request success
      setUser(null);
      setIsAuthenticated(false);
      setToken(null);
      
      // Remove the token from axios defaults
      delete axios.defaults.headers.common['Authorization'];
      
      // Clear storage
      localStorage.removeItem('user');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    } catch (err) {
      console.error('Logout error:', err);
      // Still clear everything on error
      setUser(null);
      setIsAuthenticated(false);
      setToken(null);
      localStorage.clear();
      delete axios.defaults.headers.common['Authorization'];
    }
  };

  const register = async (data: any) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('/api/auth/register/', data);
      const { user: userData, access } = response.data;
      
      // Set the token in axios defaults
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      setUser(userData);
      setIsAuthenticated(true);
      setToken(access);
      
      // Store tokens and user data
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', response.data.refresh);
      localStorage.setItem('user', JSON.stringify(userData));
    } catch (err: any) {
      const errorData = err.response?.data || {};
      const errorMessage = errorData.error || 'An error occurred during registration';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      isAuthenticated, 
      login, 
      logout, 
      register, 
      loading, 
      error,
      token
    }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};