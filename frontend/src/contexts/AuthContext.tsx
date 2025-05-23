// Modified: frontend/src/contexts/AuthContext.tsx

import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

// Define types
type User = {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  profile: {
    avatar: string | null;
  };
};

type AuthContextType = {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
  error: string | null;
};

// Create context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider component
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check if user is already logged in
    const checkAuthStatus = async () => {
      const storedUser = localStorage.getItem('user');
      const accessToken = localStorage.getItem('access_token');
      
      if (storedUser && accessToken) {
        try {
          // Validate token by fetching current user
          const userData = await authAPI.getCurrentUser();
          setUser(userData);
        } catch (err) {
          // Token invalid, clear storage
          localStorage.removeItem('user');
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        }
      }
      
      setLoading(false);
    };
    
    checkAuthStatus();
  }, []);

  // Login function
  const login = async (email: string, password: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await authAPI.login(email, password);
      
      // Store tokens and user data
      localStorage.setItem('access_token', response.access);
      localStorage.setItem('refresh_token', response.refresh);
      localStorage.setItem('user', JSON.stringify(response.user));
      
      setUser(response.user);
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'An error occurred during login';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Register function
  const register = async (name: string, email: string, password: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await authAPI.register(name, email, password);
      
      // Store tokens and user data
      localStorage.setItem('access_token', response.access);
      localStorage.setItem('refresh_token', response.refresh);
      localStorage.setItem('user', JSON.stringify(response.user));
      
      setUser(response.user);
    } catch (err: any) {
      const errorData = err.response?.data || {};
      let errorMessage = 'Registration failed';
      
      // Process validation errors
      if (typeof errorData === 'object') {
        const errorMessages = Object.entries(errorData)
          .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
          .join('; ');
        
        if (errorMessages) {
          errorMessage = errorMessages;
        }
      }
      
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      isAuthenticated: !!user, 
      login, 
      register, 
      logout, 
      loading, 
      error 
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