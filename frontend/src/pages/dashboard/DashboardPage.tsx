import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { 
  ChevronRight, Dumbbell, Apple, Activity, 
  ArrowUp, ArrowDown, Calendar, Clock, Award, Target
} from 'lucide-react';
import { motion } from 'framer-motion';
import { 
  AreaChart, Area, BarChart, Bar, XAxis, YAxis, 
  CartesianGrid, Tooltip, ResponsiveContainer, Legend 
} from 'recharts';

// Sample progress data
const progressData = [
  { name: 'Week 1', weight: 185, strength: 65 },
  { name: 'Week 2', weight: 183, strength: 68 },
  { name: 'Week 3', weight: 181, strength: 72 },
  { name: 'Week 4', weight: 179, strength: 75 },
  { name: 'Week 5', weight: 178, strength: 78 },
  { name: 'Week 6', weight: 176, strength: 82 },
  { name: 'Week 7', weight: 174, strength: 85 },
  { name: 'Week 8', weight: 173, strength: 88 },
];

// Sample nutrition data
const nutritionData = [
  { name: 'Mon', calories: 2100, protein: 120, carbs: 240, fat: 70 },
  { name: 'Tue', calories: 2200, protein: 130, carbs: 220, fat: 75 },
  { name: 'Wed', calories: 2050, protein: 125, carbs: 210, fat: 72 },
  { name: 'Thu', calories: 2150, protein: 135, carbs: 230, fat: 68 },
  { name: 'Fri', calories: 2250, protein: 140, carbs: 245, fat: 73 },
  { name: 'Sat', calories: 2300, protein: 145, carbs: 250, fat: 78 },
  { name: 'Sun', calories: 2000, protein: 115, carbs: 200, fat: 65 },
];

// Sample workout for today
const todayWorkout = {
  title: 'Upper Body Strength',
  exercises: [
    { name: 'Bench Press', sets: 4, reps: '8-10', weight: '135 lbs' },
    { name: 'Incline Dumbbell Press', sets: 3, reps: '10-12', weight: '40 lbs' },
    { name: 'Lat Pulldowns', sets: 4, reps: '10-12', weight: '120 lbs' },
    { name: 'Seated Cable Rows', sets: 3, reps: '10-12', weight: '140 lbs' },
    { name: 'Shoulder Press', sets: 3, reps: '10-12', weight: '35 lbs' }
  ],
  duration: '45-60 min'
};

// Sample meal for today
const todayMeals = [
  { 
    title: 'Breakfast', 
    foods: ['Oatmeal with berries', 'Greek yogurt', 'Protein shake'],
    calories: 450,
    protein: 35,
    time: '7:30 AM'
  },
  { 
    title: 'Lunch', 
    foods: ['Grilled chicken breast', 'Quinoa', 'Mixed vegetables', 'Olive oil'],
    calories: 650,
    protein: 45,
    time: '12:30 PM'
  },
  { 
    title: 'Snack', 
    foods: ['Protein bar', 'Apple'],
    calories: 250,
    protein: 20,
    time: '3:30 PM'
  },
  { 
    title: 'Dinner', 
    foods: ['Salmon fillet', 'Brown rice', 'Steamed broccoli', 'Avocado'],
    calories: 750,
    protein: 40,
    time: '7:00 PM'
  }
];

const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  
  const formatDate = () => {
    const date = new Date();
    return new Intl.DateTimeFormat('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    }).format(date);
  };

  return (
    <div className="bg-gray-50 pt-8 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Welcome back, {user?.name}
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
                  <p className="text-2xl font-bold text-gray-900">173 lbs</p>
                  <span className="flex items-center ml-2 text-green-500 text-sm">
                    <ArrowDown size={16} />
                    2.3%
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
                <h2 className="text-sm font-medium text-gray-500">Strength Score</h2>
                <div className="flex items-center">
                  <p className="text-2xl font-bold text-gray-900">88</p>
                  <span className="flex items-center ml-2 text-green-500 text-sm">
                    <ArrowUp size={16} />
                    3.5%
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
                <h2 className="text-sm font-medium text-gray-500">Streak</h2>
                <div className="flex items-center">
                  <p className="text-2xl font-bold text-gray-900">24 days</p>
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
                <h2 className="text-sm font-medium text-gray-500">Achievements</h2>
                <div className="flex items-center">
                  <p className="text-2xl font-bold text-gray-900">12</p>
                  <span className="flex items-center ml-2 text-yellow-500 text-sm">
                    <Target size={16} className="mr-1" />
                    3 new
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
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-lg font-medium text-gray-900">Your Progress</h2>
                <Link to="/progress" className="text-sm text-blue-600 hover:text-blue-500 flex items-center">
                  View details <ChevronRight size={16} />
                </Link>
              </div>
              
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart
                    data={progressData}
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
                      name="Weight (lbs)"
                      stroke="#3B82F6"
                      fill="#93C5FD"
                      activeDot={{ r: 8 }}
                    />
                    <Area
                      yAxisId="right"
                      type="monotone"
                      dataKey="strength"
                      name="Strength Score"
                      stroke="#10B981"
                      fill="#6EE7B7"
                      activeDot={{ r: 8 }}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
            
            {/* Today's workout */}
            <div className="bg-white shadow rounded-lg p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-lg font-medium text-gray-900">Today's Workout</h2>
                <Link to="/training-plan" className="text-sm text-blue-600 hover:text-blue-500 flex items-center">
                  Full plan <ChevronRight size={16} />
                </Link>
              </div>
              
              <div>
                <div className="flex items-center mb-4">
                  <Dumbbell size={20} className="text-gray-500 mr-2" />
                  <h3 className="text-xl font-medium text-gray-900">{todayWorkout.title}</h3>
                  <span className="ml-auto flex items-center text-gray-500">
                    <Clock size={16} className="mr-1" />
                    {todayWorkout.duration}
                  </span>
                </div>
                
                <div className="border-t border-gray-200 pt-4">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead>
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Exercise</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sets</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reps</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Weight</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {todayWorkout.exercises.map((exercise, index) => (
                        <tr key={index} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{exercise.name}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{exercise.sets}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{exercise.reps}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{exercise.weight}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                
                <div className="mt-6">
                  <Link
                    to="/training-plan"
                    className="block w-full text-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                  >
                    Start Workout
                  </Link>
                </div>
              </div>
            </div>
          </div>
          
          {/* Right column */}
          <div className="lg:col-span-4 space-y-8">
            {/* Nutrition summary */}
            <div className="bg-white shadow rounded-lg p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-lg font-medium text-gray-900">Today's Nutrition</h2>
                <Link to="/meal-plan" className="text-sm text-blue-600 hover:text-blue-500 flex items-center">
                  Full menu <ChevronRight size={16} />
                </Link>
              </div>
              
              <div className="space-y-4">
                {todayMeals.map((meal, index) => (
                  <div key={index} className="border-t border-gray-200 pt-4 first:border-0 first:pt-0">
                    <div className="flex justify-between items-center mb-2">
                      <h3 className="font-medium text-gray-900">{meal.title}</h3>
                      <span className="text-sm text-gray-500">{meal.time}</span>
                    </div>
                    <div className="text-sm text-gray-600 mb-2">
                      {meal.foods.join(', ')}
                    </div>
                    <div className="flex text-xs text-gray-500">
                      <span className="mr-4">{meal.calories} kcal</span>
                      <span>{meal.protein}g protein</span>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="mt-6 pt-6 border-t border-gray-200">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-gray-700">Daily Totals</span>
                  <span className="text-sm font-medium text-blue-600">2100 / 2300 kcal</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: '91%' }}></div>
                </div>
              </div>
              
              <div className="mt-6">
                <h3 className="text-sm font-medium text-gray-700 mb-2">Weekly Nutrition</h3>
                <div className="h-60">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={nutritionData}
                      margin={{ top: 5, right: 5, left: 0, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="protein" fill="#3B82F6" name="Protein" />
                      <Bar dataKey="fat" fill="#F59E0B" name="Fat" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
            
            {/* Goals */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-6">Your Goals</h2>
              
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Weight Goal: 165 lbs</span>
                    <span className="text-sm font-medium text-blue-600">53% complete</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: '53%' }}></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Strength Goal: 100</span>
                    <span className="text-sm font-medium text-green-600">88% complete</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-green-600 h-2.5 rounded-full" style={{ width: '88%' }}></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Workout Consistency</span>
                    <span className="text-sm font-medium text-purple-600">86% complete</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-purple-600 h-2.5 rounded-full" style={{ width: '86%' }}></div>
                  </div>
                </div>
              </div>
              
              <div className="mt-6">
                <Link
                  to="/profile"
                  className="block w-full text-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                >
                  Update Goals
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;