import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useDashboard } from '../../hooks/useDashboard';
import type { DashboardData } from '../../hooks/useDashboard';
import type { User } from '../../hooks/useAuth';
import { 
  ChevronRight, Dumbbell, Apple, Activity, 
  ArrowUp, ArrowDown, Calendar, Clock, Award, Target,
  Loader2
} from 'lucide-react';
import { motion } from 'framer-motion';
import { 
  AreaChart, Area, BarChart, Bar, XAxis, YAxis, 
  CartesianGrid, Tooltip, ResponsiveContainer, Legend 
} from 'recharts';

const formatProgressData = (bodyMetrics: DashboardData['body_metrics'], strengthMetrics: DashboardData['strength_metrics']) => {
  const data = [];
  const lastSevenDays = Array.from({ length: 7 }, (_, i) => {
    const date = new Date();
    date.setDate(date.getDate() - (6 - i));
    return date.toISOString().split('T')[0];
  });

  for (const date of lastSevenDays) {
    const dayData = {
      name: new Date(date).toLocaleDateString('en-US', { weekday: 'short' }),
      weight: 0,
      strength: 0,
    };

    const weightRecord = bodyMetrics.find(m => m.date.startsWith(date));
    if (weightRecord) {
      dayData.weight = weightRecord.weight;
    }

    const strengthRecords = strengthMetrics.filter(m => m.date.startsWith(date));
    if (strengthRecords.length > 0) {
      dayData.strength = strengthRecords.reduce((acc, curr) => acc + curr.weight, 0) / strengthRecords.length;
    }

    data.push(dayData);
  }

  return data;
};

const formatNutritionData = (nutritionMetrics: DashboardData['nutrition_metrics']) => {
  const lastSevenDays = Array.from({ length: 7 }, (_, i) => {
    const date = new Date();
    date.setDate(date.getDate() - (6 - i));
    return date.toISOString().split('T')[0];
  });

  return lastSevenDays.map(date => {
    const record = nutritionMetrics.find(m => m.date.startsWith(date)) || {
      calories: 0,
      protein: 0,
      carbs: 0,
      fats: 0
    };

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
  const { data, loading, error } = useDashboard();
  
  const formatDate = () => {
    const date = new Date();
    return new Intl.DateTimeFormat('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    }).format(date);
  };

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
          {loading ? (
            <div className="col-span-4 flex justify-center items-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            </div>
          ) : error ? (
            <div className="col-span-4 text-center text-red-600 py-12">
              {error}
            </div>
          ) : data && (
            <>
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
                        {data.body_metrics[data.body_metrics.length - 1]?.weight || 0} kg
                      </p>
                      <span className={`flex items-center ml-2 ${data.weight_change < 0 ? 'text-green-500' : 'text-red-500'} text-sm`}>
                        {data.weight_change < 0 ? <ArrowDown size={16} /> : <ArrowUp size={16} />}
                        {Math.abs(data.weight_change).toFixed(1)}%
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
                  <div className="p-3 rounded-full bg-green-100 text-green-600">
                    <Dumbbell size={24} />
                  </div>
                  <div className="ml-4">
                    <h2 className="text-sm font-medium text-gray-500">Strength Increase</h2>
                    <div className="flex items-center">
                      <p className="text-2xl font-bold text-gray-900">
                        {data.strength_increase.toFixed(1)}%
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
                      <p className="text-2xl font-bold text-gray-900">{data.workout_consistency.toFixed(0)}%</p>
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
                      <p className="text-2xl font-bold text-gray-900">{data.recent_achievements.length}</p>
                      <span className="flex items-center ml-2 text-yellow-500 text-sm">
                        <Target size={16} className="mr-1" />
                        New
                      </span>
                    </div>
                  </div>
                </div>
              </motion.div>
            </>
          )}
        </div>
        
        {/* Main content grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left column */}
          <div className="lg:col-span-8 space-y-8">
            {/* Progress charts */}
            <div className="bg-white shadow rounded-lg p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-lg font-medium text-gray-900">Your Progress</h2>
                <Link to="/progress" className="text-sm text-blue-600 hover:text-blue-500 flex items-center">
                  View details <ChevronRight size={16} />
                </Link>
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
                      data={formatProgressData(data.body_metrics, data.strength_metrics)}
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
                <h2 className="text-lg font-medium text-gray-900">Recent Workouts</h2>
                <Link to="/workouts" className="text-sm text-blue-600 hover:text-blue-500 flex items-center">
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
              ) : data && data.workout_metrics.length > 0 ? (
                <div className="space-y-4">
                  {data.workout_metrics.slice(-3).map((workout, index) => (
                    <div key={index} className="py-3 flex justify-between items-center border-b border-gray-200 last:border-0">
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {new Date(workout.date).toLocaleDateString('en-US', { weekday: 'long' })}
                        </p>
                        <p className="text-sm text-gray-500">
                          {workout.duration} minutes • {workout.intensity} intensity
                        </p>
                      </div>
                      <div className="text-sm font-medium text-gray-900">
                        {workout.calories_burned} cal
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  No recent workouts
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
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;