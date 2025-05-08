import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Calendar, Dumbbell, Clock, ChevronDown, ChevronUp, 
  Check, RefreshCw, Play, Pause, RotateCcw, CheckCircle, Award 
} from 'lucide-react';

// Sample workout weeks
const workoutPlans = [
  {
    id: 1,
    name: 'Week 1: Foundation',
    workouts: [
      {
        id: 'w1d1',
        day: 'Monday',
        title: 'Upper Body Strength',
        completed: true,
        exercises: [
          { name: 'Bench Press', sets: 3, reps: '8-10', weight: '135 lbs' },
          { name: 'Incline Dumbbell Press', sets: 3, reps: '10-12', weight: '35 lbs' },
          { name: 'Lat Pulldowns', sets: 3, reps: '10-12', weight: '120 lbs' },
          { name: 'Seated Cable Rows', sets: 3, reps: '10-12', weight: '140 lbs' },
          { name: 'Shoulder Press', sets: 3, reps: '10-12', weight: '30 lbs' }
        ],
        duration: '45 min'
      },
      {
        id: 'w1d2',
        day: 'Tuesday',
        title: 'Lower Body Focus',
        completed: true,
        exercises: [
          { name: 'Barbell Squats', sets: 3, reps: '8-10', weight: '185 lbs' },
          { name: 'Romanian Deadlifts', sets: 3, reps: '10-12', weight: '165 lbs' },
          { name: 'Leg Press', sets: 3, reps: '12-15', weight: '250 lbs' },
          { name: 'Leg Extensions', sets: 3, reps: '12-15', weight: '70 lbs' },
          { name: 'Standing Calf Raises', sets: 3, reps: '15-20', weight: '120 lbs' }
        ],
        duration: '50 min'
      },
      {
        id: 'w1d3',
        day: 'Wednesday',
        title: 'Active Recovery',
        completed: true,
        exercises: [
          { name: 'Light Jogging', sets: 1, reps: '20 min', weight: 'N/A' },
          { name: 'Dynamic Stretching', sets: 2, reps: '5 min', weight: 'N/A' },
          { name: 'Foam Rolling', sets: 1, reps: '10 min', weight: 'N/A' }
        ],
        duration: '35 min'
      },
      {
        id: 'w1d4',
        day: 'Thursday',
        title: 'Push Workout',
        completed: false,
        exercises: [
          { name: 'Incline Bench Press', sets: 3, reps: '8-10', weight: '145 lbs' },
          { name: 'Dumbbell Shoulder Press', sets: 3, reps: '10-12', weight: '35 lbs' },
          { name: 'Cable Chest Flyes', sets: 3, reps: '12-15', weight: '20 lbs' },
          { name: 'Tricep Pushdowns', sets: 3, reps: '12-15', weight: '45 lbs' },
          { name: 'Lateral Raises', sets: 3, reps: '12-15', weight: '15 lbs' }
        ],
        duration: '50 min'
      },
      {
        id: 'w1d5',
        day: 'Friday',
        title: 'Pull Workout',
        completed: false,
        exercises: [
          { name: 'Pull-Ups', sets: 3, reps: '6-8', weight: 'Bodyweight' },
          { name: 'Barbell Rows', sets: 3, reps: '8-10', weight: '135 lbs' },
          { name: 'Face Pulls', sets: 3, reps: '12-15', weight: '45 lbs' },
          { name: 'Hammer Curls', sets: 3, reps: '10-12', weight: '25 lbs' },
          { name: 'Preacher Curls', sets: 3, reps: '10-12', weight: '60 lbs' }
        ],
        duration: '45 min'
      },
      {
        id: 'w1d6',
        day: 'Saturday',
        title: 'Leg Hypertrophy',
        completed: false,
        exercises: [
          { name: 'Front Squats', sets: 3, reps: '8-10', weight: '145 lbs' },
          { name: 'Walking Lunges', sets: 3, reps: '12 per leg', weight: '25 lbs' },
          { name: 'Leg Curls', sets: 3, reps: '12-15', weight: '60 lbs' },
          { name: 'Bulgarian Split Squats', sets: 3, reps: '10 per leg', weight: '30 lbs' },
          { name: 'Seated Calf Raises', sets: 4, reps: '15-20', weight: '90 lbs' }
        ],
        duration: '55 min'
      },
      {
        id: 'w1d7',
        day: 'Sunday',
        title: 'Rest Day',
        completed: false,
        exercises: [],
        duration: '0 min'
      }
    ]
  },
  {
    id: 2,
    name: 'Week 2: Progressive Overload',
    workouts: [
      {
        id: 'w2d1',
        day: 'Monday',
        title: 'Upper Body Power',
        completed: false,
        exercises: [
          { name: 'Bench Press', sets: 4, reps: '6-8', weight: '145 lbs' },
          { name: 'Incline Dumbbell Press', sets: 3, reps: '8-10', weight: '40 lbs' },
          { name: 'Lat Pulldowns', sets: 4, reps: '8-10', weight: '130 lbs' },
          { name: 'Seated Cable Rows', sets: 3, reps: '8-10', weight: '150 lbs' },
          { name: 'Shoulder Press', sets: 3, reps: '8-10', weight: '35 lbs' }
        ],
        duration: '50 min'
      },
      // More workouts would be listed here
      {
        id: 'w2d2',
        day: 'Tuesday',
        title: 'Lower Body Power',
        completed: false,
        exercises: [
          { name: 'Barbell Squats', sets: 4, reps: '6-8', weight: '195 lbs' },
          { name: 'Romanian Deadlifts', sets: 4, reps: '8-10', weight: '175 lbs' },
          { name: 'Leg Press', sets: 3, reps: '10-12', weight: '270 lbs' },
          { name: 'Leg Extensions', sets: 3, reps: '10-12', weight: '80 lbs' },
          { name: 'Standing Calf Raises', sets: 4, reps: '12-15', weight: '130 lbs' }
        ],
        duration: '55 min'
      }
    ]
  }
];

const TrainingPlanPage: React.FC = () => {
  const [expandedWeek, setExpandedWeek] = useState<number>(1);
  const [activeWorkout, setActiveWorkout] = useState<string | null>(null);
  const [timerRunning, setTimerRunning] = useState(false);
  const [timerSeconds, setTimerSeconds] = useState(0);
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(0);
  const [currentSetIndex, setCurrentSetIndex] = useState(0);
  const [completedExercises, setCompletedExercises] = useState<string[]>([]);

  const toggleWeek = (weekId: number) => {
    setExpandedWeek(expandedWeek === weekId ? 0 : weekId);
  };

  const startWorkout = (workoutId: string) => {
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

  const completeExercise = (exerciseName: string) => {
    if (!completedExercises.includes(exerciseName)) {
      setCompletedExercises([...completedExercises, exerciseName]);
    } else {
      setCompletedExercises(completedExercises.filter(name => name !== exerciseName));
    }
  };

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
  };

  // Find active workout details
  const activeWorkoutDetails = activeWorkout 
    ? workoutPlans
        .flatMap(week => week.workouts)
        .find(workout => workout.id === activeWorkout)
    : null;

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

        {/* Main content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Workout plan (left side) */}
          <div className="lg:col-span-2">
            {!activeWorkout ? (
              // Weekly workout plans
              <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="border-b border-gray-200 px-6 py-4">
                  <h2 className="text-lg font-medium text-gray-900 flex items-center">
                    <Calendar className="mr-2 h-5 w-5 text-gray-500" />
                    Your 8-Week Strength Plan
                  </h2>
                </div>
                <div className="divide-y divide-gray-200">
                  {workoutPlans.map((week) => (
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
                                        <span className="text-sm font-medium text-gray-500">{workout.day}</span>
                                      </div>
                                      <h3 className="text-lg font-medium text-gray-900">{workout.title}</h3>
                                      <div className="flex items-center mt-1 text-sm text-gray-500">
                                        <Clock className="h-4 w-4 mr-1" />
                                        {workout.duration}
                                        <span className="mx-2">•</span>
                                        <span>{workout.exercises.length} exercises</span>
                                      </div>
                                    </div>
                                    <button
                                      onClick={() => startWorkout(workout.id)}
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
            ) : (
              // Active workout view
              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
                  <h2 className="text-xl font-bold text-gray-900">
                    {activeWorkoutDetails?.day}: {activeWorkoutDetails?.title}
                  </h2>
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
                          completedExercises.includes(exercise.name) 
                            ? 'bg-green-50 border-green-200' 
                            : 'bg-white border-gray-200'
                        }`}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="text-lg font-medium text-gray-900">{exercise.name}</h3>
                          <button
                            onClick={() => completeExercise(exercise.name)}
                            className={`p-1 rounded-full ${
                              completedExercises.includes(exercise.name)
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
                                setIndex < currentSetIndex || completedExercises.includes(exercise.name)
                                  ? 'bg-green-500 text-white'
                                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                              }`}
                              onClick={() => {
                                if (index === currentExerciseIndex) {
                                  setCurrentSetIndex(setIndex + 1);
                                  if (setIndex + 1 >= exercise.sets) {
                                    completeExercise(exercise.name);
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
                  <div className="mt-8">
                    <button
                      onClick={() => setActiveWorkout(null)}
                      className="w-full flex justify-center items-center px-4 py-3 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-blue-600 hover:bg-blue-700"
                    >
                      <CheckCircle size={20} className="mr-2" />
                      Complete Workout
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
              
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Weekly Workouts</span>
                    <span className="text-sm font-medium text-blue-600">3/6 completed</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: '50%' }}></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Volume Progress</span>
                    <span className="text-sm font-medium text-green-600">+12% this week</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-green-600 h-2.5 rounded-full" style={{ width: '65%' }}></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Program Adherence</span>
                    <span className="text-sm font-medium text-purple-600">87%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-purple-600 h-2.5 rounded-full" style={{ width: '87%' }}></div>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 pt-6 border-t border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500">Current streak</p>
                    <p className="font-medium text-gray-900">6 days</p>
                  </div>
                  <button className="p-2 rounded-md bg-blue-50 text-blue-600 hover:bg-blue-100">
                    <RefreshCw size={18} />
                  </button>
                </div>
              </div>
            </div>
            
            {/* Achievements */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Recent Achievements</h2>
              
              <div className="space-y-4">
                <div className="flex items-start">
                  <div className="flex-shrink-0">
                    <div className="p-2 bg-yellow-100 rounded-full">
                      <Award className="h-6 w-6 text-yellow-600" />
                    </div>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-gray-900">Consistency Champion</h3>
                    <p className="text-xs text-gray-500">Completed all workouts for 3 weeks straight</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="flex-shrink-0">
                    <div className="p-2 bg-green-100 rounded-full">
                      <Award className="h-6 w-6 text-green-600" />
                    </div>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-gray-900">Weight Milestone</h3>
                    <p className="text-xs text-gray-500">Bench pressed 150 lbs for the first time</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="flex-shrink-0">
                    <div className="p-2 bg-blue-100 rounded-full">
                      <Award className="h-6 w-6 text-blue-600" />
                    </div>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-gray-900">Volume King</h3>
                    <p className="text-xs text-gray-500">Increased total lifting volume by 20% this month</p>
                  </div>
                </div>
              </div>
              
              <div className="mt-4 pt-4 border-t border-gray-200">
                <button className="text-blue-600 text-sm font-medium hover:text-blue-700">
                  View all achievements
                </button>
              </div>
            </div>
            
            {/* AI recommendations */}
            <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg shadow p-6 text-white">
              <h2 className="text-lg font-medium mb-4 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 2a4 4 0 0 0-4 4v12a4 4 0 0 0 8 0V6a4 4 0 0 0-4-4z" />
                  <path d="M16 6h2a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2" />
                  <path d="M8 6H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2" />
                  <path d="M17 22h1a2 2 0 0 0 2-2v-1" />
                  <path d="M7 22H6a2 2 0 0 1-2-2v-1" />
                </svg>
                AI Training Insights
              </h2>
              
              <div className="space-y-4">
                <p className="text-white text-opacity-90">
                  Based on your recent progress, you're ready to increase your bench press weight by 5-10 lbs next week.
                </p>
                
                <p className="text-white text-opacity-90">
                  I've noticed your squat form has improved significantly. Great job maintaining proper depth!
                </p>
                
                <p className="text-white text-opacity-90">
                  Consider adding an extra rest day next week as your training volume has been high for 3 consecutive weeks.
                </p>
              </div>
              
              <button className="mt-6 w-full bg-white bg-opacity-20 hover:bg-opacity-30 text-white py-2 px-4 rounded-md text-sm font-medium transition-colors duration-200">
                Get personalized tips
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrainingPlanPage;