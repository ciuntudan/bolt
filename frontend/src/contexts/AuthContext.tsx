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

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  updateProfile: (profileData: Partial<User['profile']>) => void;
}

export const AuthContext = createContext<AuthContextValue | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.get('/auth/user/');
        setUser(response.data);
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      setUser(null);
      setIsAuthenticated(false);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await axios.post('/auth/login/', {
        username: email,
        password: password,
      });

      const { access, refresh, user } = response.data;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;

      setUser(user);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        await axios.post('/auth/logout/', { refresh: refreshToken });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      delete axios.defaults.headers.common['Authorization'];
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  const updateProfile = (profileData: Partial<User['profile']>) => {
    if (user) {
      setUser({
        ...user,
        profile: {
          ...user.profile,
          ...profileData
        }
      });
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, isAuthenticated, login, logout, updateProfile }}>
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