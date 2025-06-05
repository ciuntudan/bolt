export interface WorkoutTemplate {
  id: number;
  name: string;
  description: string;
  muscle_groups: string;
  difficulty_level: string;
  estimated_duration: number;
}

export interface CompletedWorkout {
  id: number;
  workout_template: WorkoutTemplate;
  scheduled_date: string;
  completed_date: string;
  duration_minutes: number;
  notes: string;
  is_completed: boolean;
} 