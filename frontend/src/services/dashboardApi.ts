import api from './api';

export interface UserProfile {
  user: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
  };
  current_weight: number;
  target_weight: number;
  height: number;
  age: number;
  gender: string;
  fitness_level: string;
  goal: string;
  created_at: string;
  updated_at: string;
}

export interface ProgressEntry {
  id: number;
  date: string;
  weight: number;
  strength_score: number;
  body_fat_percentage?: number;
  muscle_mass?: number;
  notes: string;
  created_at: string;
}

export interface Exercise {
  id: number;
  name: string;
  muscle_group: string;
  equipment_needed?: string;
  instructions: string;
  difficulty_level: string;
}

export interface WorkoutExercise {
  id: number;
  exercise: Exercise;
  sets: number;
  reps_min: number;
  reps_max: number;
  weight_suggestion?: number;
  rest_time: number;
  order: number;
}

export interface WorkoutTemplate {
  id: number;
  name: string;
  description: string;
  muscle_groups: string;
  difficulty_level: string;
  estimated_duration: number;
  exercises: WorkoutExercise[];
}

export interface UserWorkout {
  id: number;
  workout_template: WorkoutTemplate;
  scheduled_date: string;
  completed_date?: string;
  duration_minutes?: number;
  notes: string;
  is_completed: boolean;
}

export interface MealPlan {
  id: number;
  date: string;
  meal_type: string;
  meal_name: string;
  foods: string[];
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  scheduled_time: string;
  is_consumed: boolean;
}

export interface Achievement {
  id: number;
  title: string;
  description: string;
  icon: string;
  category: string;
  earned_date: string;
  is_new: boolean;
}

export interface DashboardStats {
  current_weight: number;
  target_weight: number;
  weight_change_percentage: number;
  strength_score: number;
  strength_change_percentage: number;
  current_streak: number;
  total_achievements: number;
  new_achievements: number;
}

export interface WeeklyNutrition {
  name: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
}

export interface GoalsProgress {
  weight: number;
  strength: number;
  consistency: number;
}

export interface DashboardData {
  stats: DashboardStats;
  progress_data: ProgressEntry[];
  today_workout?: UserWorkout;
  today_meals: MealPlan[];
  weekly_nutrition: WeeklyNutrition[];
  goals_progress: GoalsProgress;
  recent_achievements: Achievement[];
}

export const dashboardApi = {
  // Get dashboard overview data
  getDashboardOverview: async (): Promise<DashboardData> => {
    const response = await api.get('/dashboard/overview/');
    return response.data;
  },

  // Get user profile
  getUserProfile: async (): Promise<UserProfile> => {
    const response = await api.get('/dashboard/profile/');
    return response.data;
  },

  // Update user profile
  updateUserProfile: async (data: Partial<UserProfile>): Promise<UserProfile> => {
    const response = await api.put('/dashboard/profile/', data);
    return response.data;
  },

  // Progress entries
  getProgressEntries: async (): Promise<ProgressEntry[]> => {
    const response = await api.get('/dashboard/progress/');
    return response.data;
  },

  createProgressEntry: async (data: Omit<ProgressEntry, 'id' | 'created_at'>): Promise<ProgressEntry> => {
    const response = await api.post('/dashboard/progress/', data);
    return response.data;
  },

  // Workout templates
  getWorkoutTemplates: async (): Promise<WorkoutTemplate[]> => {
    const response = await api.get('/dashboard/workout-templates/');
    return response.data;
  },

  // User workouts
  getUserWorkouts: async (): Promise<UserWorkout[]> => {
    const response = await api.get('/dashboard/workouts/');
    return response.data;
  },

  createUserWorkout: async (data: { workout_template: number; scheduled_date: string }): Promise<UserWorkout> => {
    const response = await api.post('/dashboard/workouts/', data);
    return response.data;
  },

  completeWorkout: async (workoutId: number, data: { duration_minutes?: number; notes?: string }): Promise<void> => {
    await api.post(`/dashboard/workouts/${workoutId}/complete/`, data);
  },

  // Meal plans
  getMealPlans: async (date?: string): Promise<MealPlan[]> => {
    const params = date ? { date } : {};
    const response = await api.get('/dashboard/meals/', { params });
    return response.data;
  },

  createMealPlan: async (data: Omit<MealPlan, 'id'>): Promise<MealPlan> => {
    const response = await api.post('/dashboard/meals/', data);
    return response.data;
  },

  // Achievements
  getAchievements: async (): Promise<Achievement[]> => {
    const response = await api.get('/dashboard/achievements/');
    return response.data;
  },

  markAchievementsRead: async (): Promise<void> => {
    await api.post('/dashboard/achievements/mark-read/');
  },
};