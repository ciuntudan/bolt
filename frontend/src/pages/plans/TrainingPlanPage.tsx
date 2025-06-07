import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Calendar, Dumbbell, Clock, ChevronDown, ChevronUp, 
  Check, RefreshCw, Play, Pause, RotateCcw, CheckCircle, Award, X 
} from 'lucide-react';
import axios from '../../utils/axios';

interface Exercise {
  id: number;
  name: string;
  sets: number;
  reps: string;
  weight: string;
  notes?: string;
  order: number;
  completed: boolean;
}

interface TrainingDay {
  id: number;
  day_of_week: number;
  name: string;
  description: string;
  duration_minutes: number;
  completed: boolean;
  exercises: Exercise[];
  updated_at: string;
}

interface TrainingWeek {
  id: number;
  week_number: number;
  name: string;
  description: string;
  workouts: TrainingDay[];
  completed?: boolean;
  duration_minutes?: number;
}

interface TrainingPlan {
  id: number;
  name: string;
  description: string;
  goal: string;
  difficulty: string;
  duration_weeks: number;
  training_style: string;
  equipment_available: string[];
  include_deload_weeks: boolean;
  experience_years: number;
  injuries_limitations: string[];
  preferred_exercises: string[];
  excluded_exercises: string[];
  cardio_preferences: {
    type: string[];
    duration: number;
    frequency: number;
  };
  weeks: TrainingWeek[];
  created_at: string;
  updated_at: string;
  stats?: {
    weekly_workouts_completed: number;
    weekly_workouts_total: number;
    volume_progress_percentage: number;
    program_adherence_percentage: number;
    current_streak: number;
  };
  achievements?: {
    id: number;
    title: string;
    description: string;
    date_achieved: string;
    type: 'gold' | 'silver' | 'bronze';
  }[];
}

interface ApiResponse {
    data: TrainingPlan;
}

const TrainingPlanPage: React.FC = () => {
  const [trainingPlans, setTrainingPlans] = useState<TrainingPlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedWeek, setExpandedWeek] = useState<number>(1);
  const [activeWorkout, setActiveWorkout] = useState<number | null>(null);
  const [timerRunning, setTimerRunning] = useState(false);
  const [timerSeconds, setTimerSeconds] = useState(0);
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(0);
  const [currentSetIndex, setCurrentSetIndex] = useState(0);
  const [completedExercises, setCompletedExercises] = useState<string[]>([]);
  const [showGenerateModal, setShowGenerateModal] = useState(false);
  const [planPreferences, setPlanPreferences] = useState({
    goal: 'strength',
    difficulty: 'intermediate',
    duration_weeks: 8,
    days_per_week: 4,
    preferred_workout_duration: 60,
    training_style: 'traditional',
    equipment_available: ['barbell', 'dumbbell', 'cables', 'bodyweight'] as string[],
    include_deload_weeks: false,
    experience_years: 0,
    injuries_limitations: [] as string[],
    preferred_exercises: [] as string[],
    excluded_exercises: [] as string[],
    cardio_preferences: {
      type: ['running', 'cycling', 'rowing'] as string[],
      duration: 20,
      frequency: 2
    }
  });
  const [planToRegenerate, setPlanToRegenerate] = useState<number | null>(null);

  useEffect(() => {
    fetchTrainingPlans();
  }, []);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (timerRunning) {
      interval = setInterval(() => {
        setTimerSeconds(prev => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [timerRunning]);

  const fetchTrainingPlans = async () => {
    try {
      const response = await axios.get('/training-plans/');
      setTrainingPlans(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch training plans');
      console.error('Error fetching training plans:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRegeneratePlan = (planId: number) => {
    setPlanToRegenerate(planId);
    setShowGenerateModal(true);
  };

  const handleGeneratePlan = async () => {
    try {
      setLoading(true);
      let response: ApiResponse;
      
      // Separate the data into plan preferences and generation preferences
      const { days_per_week, preferred_workout_duration, ...planData } = planPreferences;
      
      if (planToRegenerate) {
        response = await axios.post(`/training-plans/${planToRegenerate}/regenerate/`, {
          ...planData,
          days_per_week,
          preferred_workout_duration
        });
      } else {
        response = await axios.post('/training-plans/generate/', {
          ...planData,
          days_per_week,
          preferred_workout_duration
        });
      }
      
      // Update the training plans state
      if (planToRegenerate) {
        setTrainingPlans(prevPlans => 
          prevPlans.map(plan => plan.id === planToRegenerate ? response.data : plan)
        );
      } else {
        setTrainingPlans(prevPlans => [...prevPlans, response.data]);
      }
      
      setError(null);
      setShowGenerateModal(false);
      setPlanToRegenerate(null);
    } catch (err: any) {
      console.error('Error with training plan:', err);
      setError(err.response?.data?.error || 'Failed to generate training plan');
    } finally {
      setLoading(false);
    }
  };

  const handleCloseModal = () => {
    setShowGenerateModal(false);
    setPlanToRegenerate(null);
  };

  const toggleWeek = (weekId: number) => {
    setExpandedWeek(expandedWeek === weekId ? 0 : weekId);
  };

  const startWorkout = (workoutId: number) => {
    setActiveWorkout(workoutId);
    setTimerSeconds(0);
    setCurrentExerciseIndex(0);
    setCurrentSetIndex(0);
    setCompletedExercises([]);
  };

  const toggleTimer = () => {
    setTimerRunning(!timerRunning);
  };

  const resetTimer = () => {
    setTimerSeconds(0);
  };

  const completeExercise = async (exerciseId: number) => {
    try {
      await axios.patch(`/exercises/${exerciseId}/`, {
        completed: true
      });
      
      // Update local state
      setTrainingPlans(prevPlans => {
        return prevPlans.map(plan => ({
          ...plan,
          weeks: plan.weeks.map(week => ({
            ...week,
            workouts: week.workouts.map(workout => ({
              ...workout,
              exercises: workout.exercises.map(exercise => 
                exercise.id === exerciseId 
                  ? { ...exercise, completed: true }
                  : exercise
              )
            }))
          }))
        }));
      });
      
      if (!completedExercises.includes(exerciseId.toString())) {
        setCompletedExercises([...completedExercises, exerciseId.toString()]);
      }
    } catch (err) {
      console.error('Error completing exercise:', err);
    }
  };

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
  };

  // Find active workout details
  const activeWorkoutDetails = activeWorkout 
    ? trainingPlans
        .flatMap(plan => plan.weeks)
        .flatMap(week => week.workouts)
        .find(workout => workout.id === activeWorkout)
    : null;

  const completeWorkout = async (workoutId: number) => {
    try {
        setLoading(true);
        const response = await axios.post(`/workouts/${workoutId}/complete/`);
        
        // Update the workout in the training plans state
        setTrainingPlans(prevPlans => 
            prevPlans.map(plan => ({
                ...plan,
                weeks: plan.weeks.map(week => ({
                    ...week,
                    workouts: week.workouts.map(workout =>
                        workout.id === workoutId ? response.data : workout
                    )
                }))
            }))
        );
        
        // Show success message
        setError(null);
        
        // Reset active workout
        setActiveWorkout(null);
        setTimerSeconds(0);
        setCurrentExerciseIndex(0);
        setCurrentSetIndex(0);
        setCompletedExercises([]);
        
    } catch (err) {
        setError('Failed to complete workout');
        console.error('Error completing workout:', err);
    } finally {
        setLoading(false);
    }
};

  const GeneratePlanModal = () => (
    <div className={`fixed inset-0 bg-black bg-opacity-50 z-50 ${showGenerateModal ? 'block' : 'hidden'}`}>
      <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg p-6 w-[800px] max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">
            {planToRegenerate ? 'Regenerate Training Plan' : 'Generate New Training Plan'}
          </h2>
          <button
            onClick={handleCloseModal}
            className="text-gray-400 hover:text-gray-500"
          >
            <X className="h-5 w-5" />
          </button>
        </div>
        
        <div className="grid grid-cols-2 gap-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Goal</label>
              <select
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={planPreferences.goal}
                onChange={(e) => setPlanPreferences({...planPreferences, goal: e.target.value})}
              >
                <option value="strength">Strength</option>
                <option value="hypertrophy">Muscle Growth</option>
                <option value="endurance">Endurance</option>
                <option value="weight_loss">Weight Loss</option>
                <option value="powerlifting">Powerlifting</option>
                <option value="crossfit">CrossFit Style</option>
                <option value="athletic">Athletic Performance</option>
                <option value="rehabilitation">Rehabilitation</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Days per Week</label>
              <select
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={planPreferences.days_per_week}
                onChange={(e) => setPlanPreferences({...planPreferences, days_per_week: parseInt(e.target.value)})}
              >
                {[1, 2, 3, 4, 5, 6].map(days => (
                  <option key={days} value={days}>{days} {days === 1 ? 'day' : 'days'}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Workout Duration</label>
              <select
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={planPreferences.preferred_workout_duration}
                onChange={(e) => setPlanPreferences({...planPreferences, preferred_workout_duration: parseInt(e.target.value)})}
              >
                {[30, 45, 60, 75, 90].map(duration => (
                  <option key={duration} value={duration}>{duration} minutes</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Training Style</label>
              <select
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={planPreferences.training_style}
                onChange={(e) => setPlanPreferences({...planPreferences, training_style: e.target.value})}
              >
                <option value="traditional">Traditional</option>
                <option value="supersets">Supersets</option>
                <option value="circuit">Circuit Training</option>
                <option value="pyramid">Pyramid Sets</option>
                <option value="dropsets">Drop Sets</option>
                <option value="german_volume">German Volume Training</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Experience Level</label>
              <select
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={planPreferences.difficulty}
                onChange={(e) => setPlanPreferences({...planPreferences, difficulty: e.target.value})}
              >
                <option value="beginner">Beginner (0-1 years)</option>
                <option value="intermediate">Intermediate (1-3 years)</option>
                <option value="advanced">Advanced (3-5 years)</option>
                <option value="elite">Elite (5+ years)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Program Duration</label>
              <select
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={planPreferences.duration_weeks}
                onChange={(e) => setPlanPreferences({...planPreferences, duration_weeks: parseInt(e.target.value)})}
              >
                <option value="4">4 weeks</option>
                <option value="8">8 weeks</option>
                <option value="12">12 weeks</option>
                <option value="16">16 weeks</option>
              </select>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Equipment Available</label>
              <div className="mt-2 space-y-2">
                {[
                  { value: 'barbell', label: 'Barbell' },
                  { value: 'dumbbell', label: 'Dumbbells' },
                  { value: 'cables', label: 'Cable Machine' },
                  { value: 'bodyweight', label: 'Bodyweight' },
                  { value: 'machines', label: 'Weight Machines' },
                  { value: 'kettlebell', label: 'Kettlebells' },
                  { value: 'resistance_bands', label: 'Resistance Bands' }
                ].map(({ value, label }) => (
                  <label key={value} className="flex items-center">
                    <input
                      type="checkbox"
                      className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                      checked={planPreferences.equipment_available.includes(value)}
                      onChange={(e) => {
                        const newEquipment = e.target.checked
                          ? [...planPreferences.equipment_available, value]
                          : planPreferences.equipment_available.filter(eq => eq !== value);
                        setPlanPreferences({...planPreferences, equipment_available: newEquipment});
                      }}
                    />
                    <span className="ml-2 text-gray-700">{label}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Injuries/Limitations</label>
              <div className="mt-2 space-y-2">
                {[
                  { value: 'shoulder', label: 'Shoulder Issues' },
                  { value: 'knee', label: 'Knee Problems' },
                  { value: 'back', label: 'Back Pain' },
                  { value: 'hip', label: 'Hip Mobility Issues' },
                  { value: 'wrist', label: 'Wrist Problems' },
                  { value: 'ankle', label: 'Ankle Issues' }
                ].map(({ value, label }) => (
                  <label key={value} className="flex items-center">
                    <input
                      type="checkbox"
                      className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                      checked={planPreferences.injuries_limitations.includes(value)}
                      onChange={(e) => {
                        const newLimitations = e.target.checked
                          ? [...planPreferences.injuries_limitations, value]
                          : planPreferences.injuries_limitations.filter(l => l !== value);
                        setPlanPreferences({...planPreferences, injuries_limitations: newLimitations});
                      }}
                    />
                    <span className="ml-2 text-gray-700">{label}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Cardio Preferences</label>
              <div className="mt-2 space-y-3">
                <div>
                  <label className="text-xs text-gray-600">Type</label>
                  <div className="space-y-2">
                    {[
                      { value: 'running', label: 'Running' },
                      { value: 'cycling', label: 'Cycling' },
                      { value: 'rowing', label: 'Rowing' },
                      { value: 'swimming', label: 'Swimming' },
                      { value: 'hiit', label: 'HIIT' },
                      { value: 'walking', label: 'Walking' }
                    ].map(({ value, label }) => (
                      <label key={value} className="flex items-center">
                        <input
                          type="checkbox"
                          className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                          checked={planPreferences.cardio_preferences.type.includes(value)}
                          onChange={(e) => {
                            const newTypes = e.target.checked
                              ? [...planPreferences.cardio_preferences.type, value]
                              : planPreferences.cardio_preferences.type.filter(t => t !== value);
                            setPlanPreferences({
                              ...planPreferences,
                              cardio_preferences: {
                                ...planPreferences.cardio_preferences,
                                type: newTypes
                              }
                            });
                          }}
                        />
                        <span className="ml-2 text-gray-700">{label}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="text-xs text-gray-600">Duration (minutes)</label>
                  <select
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    value={planPreferences.cardio_preferences.duration}
                    onChange={(e) => setPlanPreferences({
                      ...planPreferences,
                      cardio_preferences: {
                        ...planPreferences.cardio_preferences,
                        duration: parseInt(e.target.value)
                      }
                    })}
                  >
                    <option value="15">15 minutes</option>
                    <option value="20">20 minutes</option>
                    <option value="30">30 minutes</option>
                    <option value="45">45 minutes</option>
                    <option value="60">60 minutes</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs text-gray-600">Sessions per Week</label>
                  <select
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    value={planPreferences.cardio_preferences.frequency}
                    onChange={(e) => setPlanPreferences({
                      ...planPreferences,
                      cardio_preferences: {
                        ...planPreferences.cardio_preferences,
                        frequency: parseInt(e.target.value)
                      }
                    })}
                  >
                    <option value="1">1 session</option>
                    <option value="2">2 sessions</option>
                    <option value="3">3 sessions</option>
                    <option value="4">4+ sessions</option>
                  </select>
                </div>
              </div>
            </div>

            <div>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                  checked={planPreferences.include_deload_weeks}
                  onChange={(e) => setPlanPreferences({...planPreferences, include_deload_weeks: e.target.checked})}
                />
                <span className="ml-2 text-gray-700">Include deload weeks</span>
              </label>
              {planPreferences.include_deload_weeks && (
                <p className="mt-1 text-sm text-gray-500">
                  A deload week will be added every 4 weeks to help with recovery
                </p>
              )}
            </div>
          </div>
        </div>
        
        <div className="mt-6 flex justify-end space-x-3">
          <button
            onClick={handleCloseModal}
            className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            onClick={handleGeneratePlan}
            className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
          >
            {planToRegenerate ? 'Regenerate Plan' : 'Generate Plan'}
          </button>
        </div>
      </div>
    </div>
  );

  // Update the plan display to include regenerate button
  const renderPlanHeader = (plan: TrainingPlan) => (
    <div className="flex items-center justify-between mb-4 p-4 bg-white rounded-lg shadow">
      <div>
        <h3 className="text-lg font-medium text-gray-900">{plan.name}</h3>
        <p className="text-sm text-gray-500">{plan.description}</p>
        <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
          <span className="flex items-center">
            <Calendar className="h-4 w-4 mr-1" />
            {plan.duration_weeks} weeks
          </span>
          <span className="flex items-center">
            <Dumbbell className="h-4 w-4 mr-1" />
            {plan.difficulty}
          </span>
          <span className="flex items-center">
            <Award className="h-4 w-4 mr-1" />
            {plan.goal}
          </span>
        </div>
      </div>
      <div className="flex items-center space-x-2">
        <button
          onClick={() => handleRegeneratePlan(plan.id)}
          className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          disabled={loading && planToRegenerate === plan.id}
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${loading && planToRegenerate === plan.id ? 'animate-spin' : ''}`} />
          Regenerate
        </button>
      </div>
    </div>
  );

  // Calculate aggregated stats across all plans
  const calculateAggregatedStats = () => {
    if (!trainingPlans.length) return null;

    const currentPlan = trainingPlans[0]; // Use the most recent plan
    const completedWorkouts = currentPlan.weeks
      .flatMap(week => week.workouts)
      .filter(workout => workout.completed)
      .length;
    
    const totalWorkouts = currentPlan.weeks
      .flatMap(week => week.workouts)
      .length;

    // Calculate streak
    let streak = 0;
    const workouts = currentPlan.weeks
      .flatMap(week => week.workouts)
      .sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime());
    
    for (const workout of workouts) {
      if (workout.completed) {
        streak++;
      } else {
        break;
      }
    }

    return {
      weekly_workouts_completed: completedWorkouts,
      weekly_workouts_total: totalWorkouts,
      volume_progress_percentage: Math.round((completedWorkouts / totalWorkouts) * 100),
      program_adherence_percentage: Math.round((completedWorkouts / totalWorkouts) * 100),
      current_streak: streak
    };
  };

  // Get achievements for the current plan
  const getCurrentAchievements = () => {
    if (!trainingPlans.length) return [];

    const currentPlan = trainingPlans[0];
    const stats = calculateAggregatedStats();
    
    const achievements = [];

    // Add streak achievement if applicable
    if (stats && stats.current_streak >= 7) {
      achievements.push({
        id: 1,
        title: 'Consistency Champion',
        description: `${stats.current_streak} day workout streak!`,
        date_achieved: new Date().toISOString(),
        type: 'gold' as const
      });
    }

    // Add volume achievement if applicable
    if (stats && stats.volume_progress_percentage > 80) {
      achievements.push({
        id: 2,
        title: 'Volume Master',
        description: 'Completed over 80% of planned volume',
        date_achieved: new Date().toISOString(),
        type: 'silver' as const
      });
    }

    // Add adherence achievement if applicable
    if (stats && stats.program_adherence_percentage > 90) {
      achievements.push({
        id: 3,
        title: 'Program Dedication',
        description: 'Over 90% program adherence',
        date_achieved: new Date().toISOString(),
        type: 'bronze' as const
      });
    }

    return achievements;
  };

  return (
    <div className="bg-gray-50 pt-8 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Your Training Plan</h1>
          <p className="mt-2 text-gray-600">
            AI-powered workouts designed specifically for your goals and experience level.
          </p>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-md">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div>
            {trainingPlans.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-500 mb-4">No training plans found.</p>
                <button
                  onClick={() => setShowGenerateModal(true)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Generate New Plan
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Workout plan (left side) */}
                <div className="lg:col-span-2">
                  {!activeWorkout ? (
                    // Weekly workout plans
                    <div className="space-y-6">
                      {trainingPlans.map((plan) => (
                        <div key={plan.id} className="bg-white rounded-lg shadow overflow-hidden">
                          {renderPlanHeader(plan)}
                          <div className="divide-y divide-gray-200">
                            {plan.weeks.map((week) => (
                              <div key={week.id} className="bg-white overflow-hidden">
                                <button
                                  className="w-full px-6 py-4 flex items-center justify-between text-left"
                                  onClick={() => toggleWeek(week.id)}
                                >
                                  <div className="flex items-center">
                                    <Dumbbell className="h-5 w-5 text-gray-500 mr-2" />
                                    <span className="font-medium text-gray-900">{week.name}</span>
                                  </div>
                                  {expandedWeek === week.id ? (
                                    <ChevronUp className="h-5 w-5 text-gray-500" />
                                  ) : (
                                    <ChevronDown className="h-5 w-5 text-gray-500" />
                                  )}
                                </button>
                                
                                {expandedWeek === week.id && (
                                  <motion.div
                                    initial={{ opacity: 0, height: 0 }}
                                    animate={{ opacity: 1, height: 'auto' }}
                                    exit={{ opacity: 0, height: 0 }}
                                    transition={{ duration: 0.3 }}
                                  >
                                    <div className="px-6 pb-4">
                                      <div className="space-y-2">
                                        {week.workouts.map((workout) => (
                                          <div 
                                            key={workout.id}
                                            className={`p-4 rounded-lg border ${
                                              workout.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200 hover:border-blue-200 hover:bg-blue-50'
                                            } transition-colors duration-200`}
                                          >
                                            <div className="flex items-center justify-between">
                                              <div>
                                                <div className="flex items-center">
                                                  {workout.completed && (
                                                    <Check className="h-5 w-5 text-green-500 mr-1" />
                                                  )}
                                                  <span className="text-sm font-medium text-gray-500">Day {workout.day_of_week}</span>
                                                </div>
                                                <h3 className="text-lg font-medium text-gray-900">{workout.name}</h3>
                                                <div className="flex items-center mt-1 text-sm text-gray-500">
                                                  <Clock className="h-4 w-4 mr-1" />
                                                  {workout.duration_minutes} minutes
                                                </div>
                                              </div>
                                              <button
                                                onClick={(e) => {
                                                  e.stopPropagation();
                                                  startWorkout(workout.id);
                                                }}
                                                className={`px-4 py-2 rounded-md text-sm font-medium ${
                                                  workout.completed
                                                    ? 'bg-green-100 text-green-800 hover:bg-green-200'
                                                    : 'bg-blue-100 text-blue-800 hover:bg-blue-200'
                                                }`}
                                              >
                                                {workout.completed ? 'View Workout' : 'Start Workout'}
                                              </button>
                                            </div>
                                          </div>
                                        ))}
                                      </div>
                                    </div>
                                  </motion.div>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    // Active workout view
                    <div className="bg-white rounded-lg shadow">
                      <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
                        <div>
                          <h2 className="text-xl font-bold text-gray-900">
                            {activeWorkoutDetails?.name}
                          </h2>
                          <p className="text-sm text-gray-500">{activeWorkoutDetails?.description}</p>
                        </div>
                        <button
                          onClick={() => setActiveWorkout(null)}
                          className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                        >
                          Back to Plan
                        </button>
                      </div>
                      
                      <div className="px-6 py-4">
                        {/* Workout timer */}
                        <div className="mb-6 bg-gray-50 rounded-lg p-4 flex items-center justify-between">
                          <div>
                            <h3 className="text-sm font-medium text-gray-500">Workout Timer</h3>
                            <p className="text-2xl font-bold text-gray-900">{formatTime(timerSeconds)}</p>
                          </div>
                          <div className="flex space-x-2">
                            <button
                              onClick={toggleTimer}
                              className="p-2 rounded-full bg-blue-100 text-blue-600 hover:bg-blue-200"
                            >
                              {timerRunning ? <Pause size={20} /> : <Play size={20} />}
                            </button>
                            <button
                              onClick={resetTimer}
                              className="p-2 rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200"
                            >
                              <RotateCcw size={20} />
                            </button>
                          </div>
                        </div>
                        
                        {/* Exercise list */}
                        <div className="space-y-4">
                          {activeWorkoutDetails?.exercises.map((exercise, index) => (
                            <div 
                              key={index}
                              className={`p-4 rounded-lg border ${
                                completedExercises.includes(exercise.id.toString()) 
                                  ? 'bg-green-50 border-green-200' 
                                  : 'bg-white border-gray-200'
                              }`}
                            >
                              <div className="flex items-center justify-between mb-2">
                                <h3 className="text-lg font-medium text-gray-900">{exercise.name}</h3>
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    completeExercise(exercise.id);
                                  }}
                                  className={`p-1 rounded-full ${
                                    completedExercises.includes(exercise.id.toString())
                                      ? 'bg-green-100 text-green-600'
                                      : 'bg-gray-100 text-gray-400 hover:bg-gray-200'
                                  }`}
                                >
                                  <CheckCircle size={20} />
                                </button>
                              </div>
                              
                              <div className="flex flex-wrap items-center text-sm text-gray-600 gap-4">
                                <div className="bg-gray-100 px-3 py-1 rounded-full">
                                  {exercise.sets} sets
                                </div>
                                <div className="bg-gray-100 px-3 py-1 rounded-full">
                                  {exercise.reps} reps
                                </div>
                                <div className="bg-gray-100 px-3 py-1 rounded-full">
                                  {exercise.weight}
                                </div>
                              </div>
                              
                              {/* Set tracker */}
                              <div className="mt-4 flex space-x-2">
                                {Array.from({ length: exercise.sets }).map((_, setIndex) => (
                                  <button
                                    key={setIndex}
                                    className={`w-8 h-8 rounded-full flex items-center justify-center text-sm ${
                                      setIndex < currentSetIndex || completedExercises.includes(exercise.id.toString())
                                        ? 'bg-green-500 text-white'
                                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                    }`}
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      if (index === currentExerciseIndex) {
                                        setCurrentSetIndex(setIndex + 1);
                                        if (setIndex + 1 >= exercise.sets) {
                                          completeExercise(exercise.id);
                                          setCurrentExerciseIndex(currentExerciseIndex + 1);
                                          setCurrentSetIndex(0);
                                        }
                                      }
                                    }}
                                  >
                                    {setIndex + 1}
                                  </button>
                                ))}
                              </div>
                            </div>
                          ))}
                        </div>
                        
                        {/* Complete workout button */}
                        <div className="mt-8 flex flex-col space-y-4">
                          <button
                            onClick={() => activeWorkout && completeWorkout(activeWorkout)}
                            className="w-full flex justify-center items-center px-4 py-3 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-green-600 hover:bg-green-700 disabled:opacity-50"
                            disabled={loading || completedExercises.length < (activeWorkoutDetails?.exercises.length || 0)}
                          >
                            {loading ? (
                              <>
                                <RefreshCw className="animate-spin h-5 w-5 mr-2" />
                                Completing Workout...
                              </>
                            ) : (
                              <>
                                <CheckCircle className="h-5 w-5 mr-2" />
                                Complete Workout
                              </>
                            )}
                          </button>
                          
                          <button
                            onClick={() => setActiveWorkout(null)}
                            className="w-full flex justify-center items-center px-4 py-3 border border-gray-300 rounded-md shadow-sm text-base font-medium text-gray-700 bg-white hover:bg-gray-50"
                          >
                            Save Progress & Exit
                          </button>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
                
                {/* Sidebar (right side) */}
                <div className="space-y-8">
                  {/* Training stats */}
                  <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-lg font-medium text-gray-900 mb-4">Your Training Stats</h2>
                    
                    {calculateAggregatedStats() && (
                      <div className="space-y-4">
                        <div>
                          <div className="flex justify-between mb-2">
                            <span className="text-sm font-medium text-gray-700">Weekly Workouts</span>
                            <span className="text-sm font-medium text-blue-600">
                              {calculateAggregatedStats()?.weekly_workouts_completed}/
                              {calculateAggregatedStats()?.weekly_workouts_total} completed
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2.5">
                            <div 
                              className="bg-blue-600 h-2.5 rounded-full" 
                              style={{ 
                                width: `${Math.round((calculateAggregatedStats()?.weekly_workouts_completed || 0) / 
                                  (calculateAggregatedStats()?.weekly_workouts_total || 1) * 100)}%` 
                              }}
                            ></div>
                          </div>
                        </div>
                        
                        <div>
                          <div className="flex justify-between mb-2">
                            <span className="text-sm font-medium text-gray-700">Volume Progress</span>
                            <span className="text-sm font-medium text-green-600">
                              {calculateAggregatedStats()?.volume_progress_percentage}% completed
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2.5">
                            <div 
                              className="bg-green-600 h-2.5 rounded-full" 
                              style={{ width: `${calculateAggregatedStats()?.volume_progress_percentage}%` }}
                            ></div>
                          </div>
                        </div>
                        
                        <div>
                          <div className="flex justify-between mb-2">
                            <span className="text-sm font-medium text-gray-700">Program Adherence</span>
                            <span className="text-sm font-medium text-purple-600">
                              {calculateAggregatedStats()?.program_adherence_percentage}%
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2.5">
                            <div 
                              className="bg-purple-600 h-2.5 rounded-full" 
                              style={{ width: `${calculateAggregatedStats()?.program_adherence_percentage}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    )}
                    
                    <div className="mt-6 pt-6 border-t border-gray-200">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-500">Current streak</p>
                          <p className="font-medium text-gray-900">
                            {calculateAggregatedStats()?.current_streak || 0} days
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Achievements */}
                  <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-lg font-medium text-gray-900 mb-4">Recent Achievements</h2>
                    
                    <div className="space-y-4">
                      {getCurrentAchievements().map((achievement) => (
                        <div key={achievement.id} className="flex items-start">
                          <div className="flex-shrink-0">
                            <div className={`p-2 rounded-full ${
                              achievement.type === 'gold' 
                                ? 'bg-yellow-100' 
                                : achievement.type === 'silver'
                                ? 'bg-gray-100'
                                : 'bg-orange-100'
                            }`}>
                              <Award className={`h-6 w-6 ${
                                achievement.type === 'gold'
                                  ? 'text-yellow-600'
                                  : achievement.type === 'silver'
                                  ? 'text-gray-600'
                                  : 'text-orange-600'
                              }`} />
                            </div>
                          </div>
                          <div className="ml-3">
                            <h3 className="text-sm font-medium text-gray-900">{achievement.title}</h3>
                            <p className="text-xs text-gray-500">{achievement.description}</p>
                            <p className="text-xs text-gray-400 mt-1">
                              {new Date(achievement.date_achieved).toLocaleDateString()}
                            </p>
                          </div>
                        </div>
                      ))}
                      
                      {getCurrentAchievements().length === 0 && (
                        <p className="text-sm text-gray-500 text-center py-4">
                          Complete workouts to earn achievements!
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
      {GeneratePlanModal()}
    </div>
  );
};

export default TrainingPlanPage;