import { useState, useEffect } from 'react';
import axios from '../utils/axios';

export interface DashboardData {
  weight_change: number;
  strength_increase: number;
  workout_consistency: number;
  goal_progress: number;
  training_stats?: {
    weekly_workouts_completed: number;
    weekly_workouts_total: number;
    volume_progress_percentage: number;
    program_adherence_percentage: number;
    current_streak: number;
  };
  recent_achievements: {
    id: number;
    title: string;
    description: string;
    date: string;
    type: 'gold' | 'silver' | 'bronze';
  }[];
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
}

export const useDashboard = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/progress/summary/');
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch dashboard data');
      console.error('Dashboard data fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  return { data, loading, error, refetch: fetchDashboardData };
}; 