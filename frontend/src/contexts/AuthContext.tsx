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
  register: (data: {
    name: string;
    email: string;
    password: string;
    age: number;
    height: number;
    weight: number;
    gender: string;
    fitness_level: string;
  }) => Promise<void>;
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
      // Clear old tokens before login
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
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
    } catch (error: any) {
      console.error('Login failed:', error);
      if (error.response?.data) {
        throw new Error(Object.values(error.response.data).flat().join(', '));
      }
      throw error;
    }
  };

  const logout = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      const accessToken = localStorage.getItem('access_token');
      
      // Clean up user-specific meal plan cache before logout
      if (accessToken) {
        const userKey = `mealPlan_${btoa(accessToken).slice(0, 16)}`;
        localStorage.removeItem(userKey);
        console.log('Cleared user-specific meal plan cache on logout');
      }
      
      // Only attempt to call logout endpoint if we have both tokens
      if (refreshToken && accessToken) {
        try {
          await axios.post('/auth/logout/', { refresh: refreshToken });
        } catch (error) {
          console.error('Logout API call failed:', error);
          // Continue with cleanup even if API call fails
        }
      }
      
      // Always clean up local storage and state
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      delete axios.defaults.headers.common['Authorization'];
      setUser(null);
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Logout error:', error);
      // Ensure we still clean up even if something fails
      const accessToken = localStorage.getItem('access_token');
      if (accessToken) {
        const userKey = `mealPlan_${btoa(accessToken).slice(0, 16)}`;
        localStorage.removeItem(userKey);
      }
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      delete axios.defaults.headers.common['Authorization'];
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  const register = async (data: {
    name: string;
    email: string;
    password: string;
    age: number;
    height: number;
    weight: number;
    gender: string;
    fitness_level: string;
  }) => {
    try {
      // Clear old tokens before register
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      const [firstName, ...lastNameParts] = data.name.split(' ');
      const lastName = lastNameParts.join(' ');

      const response = await axios.post('/auth/register/', {
        username: data.email,
        email: data.email,
        password: data.password,
        password2: data.password,
        first_name: firstName,
        last_name: lastName || firstName, // Fallback if no last name
        age: data.age,
        height: data.height,
        weight: data.weight,
        gender: data.gender.toLowerCase(),
        fitness_level: data.fitness_level.toLowerCase()
      });

      const { access, refresh, user: userData } = response.data;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;

      setUser(userData);
      setIsAuthenticated(true);
    } catch (error: any) {
      console.error('Registration failed:', error);
      if (error.response?.data) {
        throw new Error(Object.values(error.response.data).flat().join(', '));
      }
      throw error;
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
    <AuthContext.Provider value={{ user, loading, isAuthenticated, login, logout, register, updateProfile }}>
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