import { useState, useEffect } from 'react';
import api from '../services/api';

export interface ProgressData {
  body_metrics: {
    date: string;
    weight: number;
    body_fat: number;
    muscle_mass: number;
  }[];
  strength_metrics: {
    date: string;
    exercise: string;
    weight: number;
  }[];
  workout_metrics: {
    date: string;
    duration: number;
    intensity: string;
    calories_burned: number;
  }[];
  nutrition_metrics: {
    date: string;
    calories: number;
    protein: number;
    carbs: number;
    fats: number;
    water: number;
  }[];
  achievements: {
    title: string;
    description: string;
    date: string;
    icon: string;
    color: string;
  }[];
}

export const useProgress = (timeRange: string = '7W') => {
  const [data, setData] = useState<ProgressData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProgressData = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/auth/progress/metrics/?time_range=${timeRange}`);
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch progress data');
      console.error('Progress data fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProgressData();
  }, [timeRange]);

  return { data, loading, error, refetch: fetchProgressData };
}; 