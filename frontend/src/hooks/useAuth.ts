import { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';

export interface User {
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

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
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

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}; 