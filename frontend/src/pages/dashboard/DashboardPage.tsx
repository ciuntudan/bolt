import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useDashboard } from '../../hooks/useDashboard';
import type { DashboardData } from '../../hooks/useDashboard';
import type { User } from '../../hooks/useAuth';
import type { CompletedWorkout } from '../../types/workout';
import { 
  ChevronRight, Dumbbell, Apple, Activity, 
  ArrowUp, ArrowDown, Calendar, Clock, Award, Target,
  Loader2, Plus, X
} from 'lucide-react';
import { motion } from 'framer-motion';
import { 
  AreaChart, Area, BarChart, Bar, XAxis, YAxis, 
  CartesianGrid, Tooltip, ResponsiveContainer, Legend 
} from 'recharts';
import axios from '../../utils/axios';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

interface WorkoutTemplate {
  id: number;
  name: string;
  description: string;
  muscle_groups: string;
  difficulty_level: string;
  estimated_duration: number;
}

const formatProgressData = (bodyMetrics: DashboardData['body_metrics'] | null | undefined, strengthMetrics: DashboardData['strength_metrics'] | null | undefined, currentWeight: number) => {
  const data = [];
  const lastSevenDays = Array.from({ length: 7 }, (_, i) => {
    const date = new Date();
    date.setDate(date.getDate() - (6 - i));
    return date.toISOString().split('T')[0];
  });

  // Sort bodyMetrics by date ascending for easier lookup
  let sortedBodyMetrics: { date: string; weight: number }[] = [];
  if (bodyMetrics && Array.isArray(bodyMetrics)) {
    sortedBodyMetrics = [...bodyMetrics].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
  }

  for (const date of lastSevenDays) {
    // Find the closest previous weight entry (on or before this date)
    let weightForDay = currentWeight;
    if (sortedBodyMetrics.length > 0) {
      // Find all entries on or before this date
      const previousEntries = sortedBodyMetrics.filter(m => m.date <= date);
      if (previousEntries.length > 0) {
        weightForDay = previousEntries[previousEntries.length - 1].weight;
      }
    }

    const dayData = {
      name: new Date(date).toLocaleDateString('en-US', { weekday: 'short' }),
      weight: weightForDay,
      strength: 0,
    };

    if (strengthMetrics && Array.isArray(strengthMetrics)) {
      const strengthRecords = strengthMetrics.filter(m => m.date.startsWith(date));
      if (strengthRecords.length > 0) {
        dayData.strength = strengthRecords.reduce((acc, curr) => acc + curr.weight, 0) / strengthRecords.length;
      }
    }

    data.push(dayData);
  }

  return data;
};

const formatNutritionData = (nutritionMetrics: DashboardData['nutrition_metrics'] | null | undefined) => {
  const lastSevenDays = Array.from({ length: 7 }, (_, i) => {
    const date = new Date();
    date.setDate(date.getDate() - (6 - i));
    return date.toISOString().split('T')[0];
  });

  return lastSevenDays.map(date => {
    let record = {
      calories: 0,
      protein: 0,
      carbs: 0,
      fats: 0
    };

    if (nutritionMetrics && Array.isArray(nutritionMetrics)) {
      const foundRecord = nutritionMetrics.find(m => m.date.startsWith(date));
      if (foundRecord) {
        record = foundRecord;
      }
    }

    return {
      name: new Date(date).toLocaleDateString('en-US', { weekday: 'short' }),
      calories: record.calories,
      protein: record.protein,
      carbs: record.carbs,
      fat: record.fats
    };
  });
};

const DashboardPage: React.FC = () => {
  const auth = useAuth();
  const { data, loading, error, refetch } = useDashboard();
  const [showWeightModal, setShowWeightModal] = useState(false);
  const [selectedDate, setSelectedDate] = useState<Date | null>(new Date());
  const [weightInput, setWeightInput] = useState('');
  const [weightError, setWeightError] = useState<string | null>(null);
  
  useEffect(() => {
    if (auth?.user?.profile?.weight) {
      setWeightInput(auth.user.profile.weight.toString());
    }
  }, [auth]);

  const formatDate = () => {
    const date = new Date();
    return new Intl.DateTimeFormat('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    }).format(date);
  };

  const handleWeightSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setWeightError(null);

    if (!weightInput || isNaN(parseFloat(weightInput)) || !selectedDate) {
      setWeightError('Please enter a valid weight and date');
      return;
    }

    try {
      // Log the weight using the correct endpoint
      await axios.post('/weight/log/', {
        date: selectedDate.toISOString().split('T')[0],
        weight: parseFloat(weightInput),
        strength_score: data?.strength_metrics[0]?.weight || 50,
        notes: 'Weight logged from dashboard'
      });

      // Update the auth context
      if (auth) {
        auth.updateProfile({ weight: parseFloat(weightInput) });
      }
      
      setShowWeightModal(false);
      setWeightInput('');
      refetch(); // Refresh dashboard data
      
      // Show success message
      const successMessage = document.createElement('div');
      successMessage.className = 'fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
      successMessage.textContent = 'Weight logged successfully!';
      document.body.appendChild(successMessage);
      setTimeout(() => successMessage.remove(), 3000);
      
    } catch (err) {
      console.error('Weight logging error:', err);
      setWeightError('Failed to log weight. Please try again.');
    }
  };

  const WeightLoggingModal = () => (
    <div className={`fixed inset-0 bg-black bg-opacity-50 z-50 ${showWeightModal ? 'block' : 'hidden'}`}>
      <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg p-6 w-[400px]">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Log Weight</h2>
          <button
            onClick={() => setShowWeightModal(false)}
            className="text-gray-400 hover:text-gray-500"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={handleWeightSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Date</label>
            <DatePicker
              selected={selectedDate}
              onChange={(date) => setSelectedDate(date)}
              maxDate={new Date()}
              dateFormat="MMMM d, yyyy"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholderText="Select date"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Weight (kg)</label>
            <input
              type="number"
              step="0.1"
              value={weightInput}
              onChange={(e) => setWeightInput(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="Enter weight in kg"
            />
          </div>

          {weightError && (
            <p className="text-sm text-red-600">{weightError}</p>
          )}

          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={() => setShowWeightModal(false)}
              className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
            >
              Log Weight
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  // If auth is not initialized yet, show loading
  if (!auth) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <div className="bg-gray-50 pt-8 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div>
               <h1 className="text-2xl font-bold text-gray-900">
                  Welcome back, {auth.user?.first_name}
              </h1>
              <p className="text-gray-500">{formatDate()}</p>
            </div>
            <div className="mt-4 md:mt-0 flex space-x-3">
              <Link 
                to="/training-plan" 
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
              >
                Today's Workout
              </Link>
              <Link 
                to="/meal-plan" 
                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-blue-600 bg-white hover:bg-gray-50"
              >
                Meal Plan
              </Link>
            </div>
          </div>
        </div>
        
        {/* Stats overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Stats overview */}
          <motion.div 
            whileHover={{ y: -5 }}
            className="bg-white rounded-lg shadow p-6"
          >
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-blue-100 text-blue-600">
                <Activity size={24} />
              </div>
              <div className="ml-4">
                <h2 className="text-sm font-medium text-gray-500">Current Weight</h2>
                <div className="flex items-center">
                  <p className="text-2xl font-bold text-gray-900">
                    {auth?.user?.profile?.weight || 0} kg
                  </p>
                  {data?.weight_change !== undefined && (
                    <span className={`flex items-center ml-2 ${data.weight_change < 0 ? 'text-green-500' : 'text-red-500'} text-sm`}>
                      {data.weight_change < 0 ? <ArrowDown size={16} /> : <ArrowUp size={16} />}
                      {Math.abs(data.weight_change).toFixed(1)}%
                    </span>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
          
          <motion.div 
            whileHover={{ y: -5 }}
            className="bg-white rounded-lg shadow p-6"
          >
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-green-100 text-green-600">
                <Dumbbell size={24} />
              </div>
              <div className="ml-4">
                <h2 className="text-sm font-medium text-gray-500">Strength Increase</h2>
                <div className="flex items-center">
                  <p className="text-2xl font-bold text-gray-900">
                    {data?.strength_increase?.toFixed(1) || '0.0'}%
                  </p>
                  <span className="flex items-center ml-2 text-green-500 text-sm">
                    <ArrowUp size={16} />
                    30d
                  </span>
                </div>
              </div>
            </div>
          </motion.div>
          
          <motion.div 
            whileHover={{ y: -5 }}
            className="bg-white rounded-lg shadow p-6"
          >
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-purple-100 text-purple-600">
                <Calendar size={24} />
              </div>
              <div className="ml-4">
                <h2 className="text-sm font-medium text-gray-500">Workout Consistency</h2>
                <div className="flex items-center">
                  <p className="text-2xl font-bold text-gray-900">
                    {data?.workout_consistency?.toFixed(0) || '0'}%
                  </p>
                  <span className="ml-2 text-purple-500 text-sm">
                    🔥
                  </span>
                </div>
              </div>
            </div>
          </motion.div>
          
          <motion.div 
            whileHover={{ y: -5 }}
            className="bg-white rounded-lg shadow p-6"
          >
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-yellow-100 text-yellow-600">
                <Award size={24} />
              </div>
              <div className="ml-4">
                <h2 className="text-sm font-medium text-gray-500">Recent Achievements</h2>
                <div className="flex items-center">
                  <p className="text-2xl font-bold text-gray-900">
                    {data?.recent_achievements?.length || 0}
                  </p>
                  <span className="flex items-center ml-2 text-yellow-500 text-sm">
                    <Target size={16} className="mr-1" />
                    New
                  </span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
        
        {/* Main content grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left column */}
          <div className="lg:col-span-8 space-y-8">
            {/* Progress charts */}
            <div className="bg-white shadow rounded-lg p-6">
              <div className="mb-6">
                <h2 className="text-lg font-medium text-gray-900">Your Progress</h2>
              </div>
              
              {loading ? (
                <div className="h-80 flex justify-center items-center">
                  <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
                </div>
              ) : error ? (
                <div className="h-80 flex justify-center items-center text-red-600">
                  {error}
                </div>
              ) : data && (
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart
                      data={formatProgressData(data.body_metrics, data.strength_metrics, auth?.user?.profile?.weight || 0)}
                      margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis yAxisId="left" orientation="left" stroke="#3B82F6" />
                      <YAxis yAxisId="right" orientation="right" stroke="#10B981" />
                      <Tooltip />
                      <Legend />
                      <Area
                        yAxisId="left"
                        type="monotone"
                        dataKey="weight"
                        name="Weight (kgs)"
                        stroke="#3B82F6"
                        fill="#93C5FD"
                        activeDot={{ r: 8 }}
                      />
                      <Area
                        yAxisId="right"
                        type="monotone"
                        dataKey="strength"
                        name="Average Strength (kgs)"
                        stroke="#10B981"
                        fill="#6EE7B7"
                        activeDot={{ r: 8 }}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              )}
            </div>
            
            {/* Recent workouts */}
            <div className="bg-white shadow rounded-lg p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-lg font-medium text-gray-900">Recent Completed Workouts</h2>
                <Link to="/training-plan" className="text-sm text-blue-600 hover:text-blue-500 flex items-center">
                  View all <ChevronRight size={16} />
                </Link>
              </div>
              
              {loading ? (
                <div className="h-48 flex justify-center items-center">
                  <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
                </div>
              ) : error ? (
                <div className="h-48 flex justify-center items-center text-red-600">
                  {error}
                </div>
              ) : data?.recent_workouts && data.recent_workouts.length > 0 ? (
                <div className="space-y-4">
                  {data.recent_workouts.map((workout) => (
                    <div key={workout.id} className="py-3 flex justify-between items-center border-b border-gray-200 last:border-0">
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {new Date(workout.completed_date).toLocaleDateString('en-US', { 
                            weekday: 'long',
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric'
                          })}
                        </p>
                        <p className="text-sm text-gray-500">
                          {workout.workout_template.name} • {workout.duration_minutes} minutes
                        </p>
                      </div>
                      <div className="text-sm font-medium text-green-600">
                        Completed
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  No completed workouts yet
                </div>
              )}
            </div>
          </div>
          
          {/* Right column */}
          <div className="lg:col-span-4 space-y-8">
            {/* Training Stats */}
            {data?.training_stats && (
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">Training Stats</h2>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700">Weekly Workouts</span>
                      <span className="text-sm font-medium text-blue-600">
                        {data.training_stats.weekly_workouts_completed}/
                        {data.training_stats.weekly_workouts_total} completed
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2.5">
                      <div 
                        className="bg-blue-600 h-2.5 rounded-full" 
                        style={{ 
                          width: `${Math.round((data.training_stats.weekly_workouts_completed / 
                            data.training_stats.weekly_workouts_total) * 100)}%` 
                        }}
                      ></div>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700">Volume Progress</span>
                      <span className="text-sm font-medium text-green-600">
                        {data.training_stats.volume_progress_percentage}% completed
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2.5">
                      <div 
                        className="bg-green-600 h-2.5 rounded-full" 
                        style={{ width: `${data.training_stats.volume_progress_percentage}%` }}
                      ></div>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700">Program Adherence</span>
                      <span className="text-sm font-medium text-purple-600">
                        {data.training_stats.program_adherence_percentage}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2.5">
                      <div 
                        className="bg-purple-600 h-2.5 rounded-full" 
                        style={{ width: `${data.training_stats.program_adherence_percentage}%` }}
                      ></div>
                    </div>
                  </div>

                  <div className="pt-4 border-t border-gray-200">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-gray-500">Current streak</p>
                        <p className="font-medium text-gray-900">
                          {data.training_stats.current_streak} days
                        </p>
                      </div>
                      <div className="p-2 bg-blue-50 rounded-full">
                        <Activity className="h-5 w-5 text-blue-600" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Achievements */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-medium text-gray-900">Recent Achievements</h2>
                <Link to="/achievements" className="text-sm text-blue-600 hover:text-blue-500 flex items-center">
                  View all <ChevronRight size={16} />
                </Link>
              </div>
              
              <div className="space-y-4">
                {data?.recent_achievements.map((achievement) => (
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
                        {new Date(achievement.date).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                ))}
                
                {(!data?.recent_achievements || data.recent_achievements.length === 0) && (
                  <p className="text-sm text-gray-500 text-center py-4">
                    Complete workouts to earn achievements!
                  </p>
                )}
              </div>
            </div>

            {/* Weight Logs */}
            <div className="bg-white rounded-lg shadow p-6 mt-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-medium text-gray-900">Weight History</h2>
                <button
                  onClick={() => {
                    if (auth?.user?.profile?.weight) {
                      setWeightInput(auth.user.profile.weight.toString());
                    }
                    setShowWeightModal(true);
                  }}
                  className="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <Plus size={16} className="mr-1" /> Log Weight
                </button>
              </div>
              
              <div className="space-y-4">
                {loading ? (
                  <div className="flex justify-center items-center py-12">
                    <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
                  </div>
                ) : error ? (
                  <div className="text-center text-red-600 py-12">
                    {error}
                  </div>
                ) : data && data.body_metrics && data.body_metrics.length > 0 ? (
                  [...data.body_metrics]
                    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
                    .slice(0, 5) // Show last 5 entries
                    .map((metric, index, array) => (
                      <div key={index} className="flex items-start border-b border-gray-100 last:border-0 pb-3 last:pb-0">
                        <div className="flex-shrink-0">
                          <div className="p-2 rounded-full bg-blue-50">
                            <Activity className="h-5 w-5 text-blue-600" />
                          </div>
                        </div>
                        <div className="ml-3 flex-grow">
                          <div className="flex justify-between items-center">
                            <h3 className="text-sm font-medium text-gray-900">
                              {metric.weight} kg
                            </h3>
                            <p className="text-xs text-gray-500">
                              {new Date(metric.date).toLocaleDateString('en-US', {
                                year: 'numeric',
                                month: 'short',
                                day: 'numeric'
                              })}
                            </p>
                          </div>
                          {index < array.length - 1 && (
                            <p className="text-xs text-gray-500 mt-1">
                              {metric.weight - array[index + 1].weight > 0 ? (
                                <span className="text-red-500 flex items-center">
                                  <ArrowUp size={12} className="mr-1" />
                                  +{(metric.weight - array[index + 1].weight).toFixed(1)} kg
                                </span>
                              ) : (
                                <span className="text-green-500 flex items-center">
                                  <ArrowDown size={12} className="mr-1" />
                                  {(metric.weight - array[index + 1].weight).toFixed(1)} kg
                                </span>
                              )}
                            </p>
                          )}
                        </div>
                      </div>
                    ))
                ) : (
                  <p className="text-sm text-gray-500 text-center py-4">
                    No weight logs yet. Start tracking your progress!
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
      {WeightLoggingModal()}
    </div>
  );
};

export default DashboardPage;