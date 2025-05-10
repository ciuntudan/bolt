// Common types for the application

export type User = {
    id: string;
    name: string;
    email: string;
    avatar?: string;
  };
  
  export type WorkoutExercise = {
    name: string;
    sets: number;
    reps: string;
    weight: string;
  };
  
  export type Workout = {
    id: string;
    day: string;
    title: string;
    completed: boolean;
    exercises: WorkoutExercise[];
    duration: string;
  };
  
  export type MealIngredient = {
    name: string;
    amount: string;
    calories: number;
    protein: number;
  };
  
  export type MealNutrition = {
    calories: number;
    protein: number;
    carbs: number;
    fat: number;
  };
  
  export type Meal = {
    type: string;
    time: string;
    title: string;
    description: string;
    ingredients: MealIngredient[];
    nutrition: MealNutrition;
    image: string;
  };
  
  export type DailyMeals = {
    day: string;
    meals: Meal[];
    totals: MealNutrition;
  };
  
  export type ProgressMetric = {
    date: string;
    [key: string]: string | number;
  };
  
  export type Achievement = {
    id: number;
    title: string;
    description: string;
    date: string;
    icon: string;
    color: string;
  };
  
  export type UserGoal = {
    id: string;
    type: 'weight' | 'strength' | 'bodyFat' | 'custom';
    title: string;
    current: number;
    target: number;
    unit: string;
    startDate: string;
    targetDate: string;
    progress: number;
  };
  
  export type UserProfile = {
    name: string;
    email: string;
    age: number;
    height: string;
    weight: number;
    gender: string;
    goals: string[];
    fitnessLevel: string;
    dietaryPreferences: string[];
    allergies: string[];
    medicalConditions: string[];
    activityLevel: string;
    workoutFrequency: string;
    workoutDuration: string;
    sleepAverage: string;
    stressLevel: string;
    profession: string;
    dateJoined: string;
  };