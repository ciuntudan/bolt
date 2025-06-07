import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to add the auth token
instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle token refresh
instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If the error is 401 and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
          // No refresh token available, clear everything and redirect to login
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          delete instance.defaults.headers.common['Authorization'];
          window.location.href = '/login';
          return Promise.reject(error);
        }

        const response = await instance.post('/auth/refresh/', {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        // Update the authorization header
        instance.defaults.headers.common['Authorization'] = `Bearer ${access}`;
        originalRequest.headers.Authorization = `Bearer ${access}`;

        return instance(originalRequest);
      } catch (err) {
        // If refresh token fails, log out the user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        delete instance.defaults.headers.common['Authorization'];
        
        // Only redirect to login if we're not already there
        if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login';
        }
        return Promise.reject(err);
      }
    }

    return Promise.reject(error);
  }
);

export default instance; 