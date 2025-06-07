import axios from 'axios';

// Define types
export interface Profile {
  avatar: string | null;
  age: number;
  height: number;
  weight: number;
  gender: 'male' | 'female' | 'other';
  fitness_level: 'beginner' | 'intermediate' | 'advanced';
}

export interface ProfileData {
  age: number;
  height: number;
  weight: number;
  gender: string;
  fitness_level: string;
}

const API_URL = 'http://127.0.0.1:8000/api';

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include access token
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

// Handle 401 errors with token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        const response = await api.post('/auth/refresh/', {
          refresh: refreshToken,
        });

        if (response.status === 200) {
          const { access } = response.data;
          localStorage.setItem('access_token', access);
          api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
          
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        delete api.defaults.headers.common['Authorization'];

        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: async (name: string, email: string, password: string, profileData: ProfileData) => {
    const [firstName, ...lastNameParts] = name.split(' ');
    const lastName = lastNameParts.join(' ');

    const response = await api.post('/auth/register/', {
      username: email,
      email: email,
      first_name: firstName,
      last_name: lastName,
      password: password,
      password2: password,
      ...profileData
    });

    // Store tokens immediately
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;

    return {
      access: response.data.access,
      refresh: response.data.refresh,
      user: response.data.user,
    };
  },

  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login/', {
      username: email,
      password: password,
    });

    // Store tokens immediately
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;

    return {
      access: response.data.access,
      refresh: response.data.refresh,
      user: response.data.user,
    };
  },

  logout: async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        await api.post('/auth/logout/', { refresh: refreshToken });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      delete api.defaults.headers.common['Authorization'];
    }
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/user/');
    return response.data;
  },

  // Profile API
  getProfile: async () => {
    const response = await api.get('/auth/profile/');
    return response.data;
  },

  updateProfile: async (profileData: Partial<Profile>) => {
    const response = await api.put('/auth/profile/', profileData);
    return response.data;
  },
};

export default api;