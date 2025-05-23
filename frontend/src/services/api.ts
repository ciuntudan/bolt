// Modified: frontend/src/services/api.ts

import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to add authorization header
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add a response interceptor to handle common errors and token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If the error is 401 and we haven't already tried to refresh the token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Try to refresh the token
        const refreshToken = localStorage.getItem('refresh_token');
        
        if (refreshToken) {
          const response = await axios.post(`${API_URL}/token/refresh/`, {
            refresh: refreshToken,
          });
          
          // If refresh successful, update tokens and retry
          if (response.status === 200) {
            localStorage.setItem('access_token', response.data.access);
            
            // Update original request with new token
            originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
            return api(originalRequest);
          }
        }
      } catch (refreshError) {
        // If refresh fails, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      }
    }
    
    return Promise.reject(error);
  }
);

// Auth API functions
export const authAPI = {
  register: async (name: string, email: string, password: string) => {
    const response = await api.post('/register/', {
      username: email,
      email: email,
      first_name: name,
      password: password,
      password2: password,
    });
    return response.data;
  },
  
  login: async (email: string, password: string) => {
    const response = await api.post('/login/', {
      username: email,
      password: password,
    });
    return response.data;
  },
  
  logout: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      await api.post('/logout/', { refresh: refreshToken });
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/user/');
    return response.data;
  },
};

export default api;