import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { motion } from 'framer-motion';
import {
  User, Mail, Lock, FileText, ChevronDown, ChevronUp,
  BarChart2, Activity, Target, Bell, Settings, Save
} from 'lucide-react';

const ProfilePage: React.FC = () => {
  const { user } = useAuth();
  const [activeSection, setActiveSection] = useState('personalInfo');
  const [expandedSection, setExpandedSection] = useState('');
  
  const toggleSection = (section: string) => {
    setExpandedSection(expandedSection === section ? '' : section);
  };
  
  // Sample user data (would come from context in real app)
  const userData = {
    name: user?.name || 'Ciuntu Daniel',
    email: user?.email || 'dan.ciuntug7@gmail.com',
    age: 22,
    height: '185cm',
    weight: 92,
    gender: 'Male',
    goals: ['Weight loss', 'Muscle gain', 'Improved strength'],
    fitnessLevel: 'Intermediate',
    dietaryPreferences: ['High protein', 'Low carb'],
    allergies: ['None'],
    medicalConditions: ['None'],
    activityLevel: 'Moderately active',
    workoutFrequency: '4-5 times per week',
    workoutDuration: '45-60 minutes',
    sleepAverage: '7 hours',
    stressLevel: 'Moderate',
    profession: 'Student',
    dateJoined: 'May 15, 2025'
  };
  
  return (
    <div className="bg-gray-50 pt-8 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Your Profile</h1>
          <p className="mt-2 text-gray-600">
            Manage your account information and preferences.
          </p>
        </div>

        {/* Main content */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar navigation */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <div className="p-6 text-center border-b border-gray-200">
                <div className="relative mx-auto h-24 w-24 rounded-full overflow-hidden bg-gray-100 mb-4 border-2 border-blue-500">
                  <img
                    src={user?.avatar || "frontend/bbr_black.png"}
                    alt={userData.name}
                    className="h-full w-full object-cover"
                  />
                  <div className="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 flex items-center justify-center transition-all duration-300 cursor-pointer">
                    <div className="text-white opacity-0 hover:opacity-100 text-xs font-medium">
                      Change Photo
                    </div>
                  </div>
                </div>
                <h2 className="text-xl font-bold text-gray-900">{userData.name}</h2>
                <p className="text-sm text-gray-500">{userData.email}</p>
                <p className="mt-1 text-xs text-gray-400">Member since {userData.dateJoined}</p>
              </div>
              
              <nav className="p-4">
                <ul className="space-y-2">
                  <li>
                    <button
                      className={`w-full flex items-center px-4 py-2 text-sm font-medium rounded-md ${
                        activeSection === 'personalInfo'
                          ? 'bg-blue-50 text-blue-700'
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                      onClick={() => setActiveSection('personalInfo')}
                    >
                      <User className="mr-3 h-5 w-5" />
                      Personal Information
                    </button>
                  </li>
                  <li>
                    <button
                      className={`w-full flex items-center px-4 py-2 text-sm font-medium rounded-md ${
                        activeSection === 'fitnessProfile'
                          ? 'bg-blue-50 text-blue-700'
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                      onClick={() => setActiveSection('fitnessProfile')}
                    >
                      <Activity className="mr-3 h-5 w-5" />
                      Fitness Profile
                    </button>
                  </li>
                  <li>
                    <button
                      className={`w-full flex items-center px-4 py-2 text-sm font-medium rounded-md ${
                        activeSection === 'goals'
                          ? 'bg-blue-50 text-blue-700'
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                      onClick={() => setActiveSection('goals')}
                    >
                      <Target className="mr-3 h-5 w-5" />
                      Goals
                    </button>
                  </li>
                  <li>
                    <button
                      className={`w-full flex items-center px-4 py-2 text-sm font-medium rounded-md ${
                        activeSection === 'healthData'
                          ? 'bg-blue-50 text-blue-700'
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                      onClick={() => setActiveSection('healthData')}
                    >
                      <FileText className="mr-3 h-5 w-5" />
                      Health Data
                    </button>
                  </li>
                  <li>
                    <button
                      className={`w-full flex items-center px-4 py-2 text-sm font-medium rounded-md ${
                        activeSection === 'accountSettings'
                          ? 'bg-blue-50 text-blue-700'
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                      onClick={() => setActiveSection('accountSettings')}
                    >
                      <Settings className="mr-3 h-5 w-5" />
                      Account Settings
                    </button>
                  </li>
                  <li>
                    <button
                      className={`w-full flex items-center px-4 py-2 text-sm font-medium rounded-md ${
                        activeSection === 'notifications'
                          ? 'bg-blue-50 text-blue-700'
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                      onClick={() => setActiveSection('notifications')}
                    >
                      <Bell className="mr-3 h-5 w-5" />
                      Notifications
                    </button>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
          
          {/* Content area */}
          <div className="lg:col-span-3">
            {/* Personal Information */}
            {activeSection === 'personalInfo' && (
              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-lg font-medium text-gray-900">Personal Information</h2>
                  <p className="mt-1 text-sm text-gray-500">
                    Update your basic profile information.
                  </p>
                </div>
                
                <div className="p-6">
                  <form className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                          Full Name
                        </label>
                        <input
                          type="text"
                          name="name"
                          id="name"
                          defaultValue={userData.name}
                          className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                          Email Address
                        </label>
                        <input
                          type="email"
                          name="email"
                          id="email"
                          defaultValue={userData.email}
                          className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="age" className="block text-sm font-medium text-gray-700">
                          Age
                        </label>
                        <input
                          type="number"
                          name="age"
                          id="age"
                          defaultValue={userData.age}
                          className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="gender" className="block text-sm font-medium text-gray-700">
                          Gender
                        </label>
                        <select
                          id="gender"
                          name="gender"
                          defaultValue={userData.gender}
                          className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        >
                          <option>Male</option>
                          <option>Female</option>
                          <option>Non-binary</option>
                          <option>Prefer not to say</option>
                        </select>
                      </div>
                      
                      <div>
                        <label htmlFor="height" className="block text-sm font-medium text-gray-700">
                          Height
                        </label>
                        <input
                          type="text"
                          name="height"
                          id="height"
                          defaultValue={userData.height}
                          className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="weight" className="block text-sm font-medium text-gray-700">
                          Weight (kgs)
                        </label>
                        <input
                          type="number"
                          name="weight"
                          id="weight"
                          defaultValue={userData.weight}
                          className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="profession" className="block text-sm font-medium text-gray-700">
                          Profession
                        </label>
                        <input
                          type="text"
                          name="profession"
                          id="profession"
                          defaultValue={userData.profession}
                          className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                        />
                      </div>
                    </div>
                    
                    <div>
                      <button
                        type="submit"
                        className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                      >
                        <Save className="mr-2 -ml-1 h-5 w-5" />
                        Save Changes
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}
            
            {/* Fitness Profile */}
            {activeSection === 'fitnessProfile' && (
              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-lg font-medium text-gray-900">Fitness Profile</h2>
                  <p className="mt-1 text-sm text-gray-500">
                    Update your fitness preferences and activity levels.
                  </p>
                </div>
                
                <div className="p-6">
                  <form className="space-y-6">
                    <div>
                      <label htmlFor="fitnessLevel" className="block text-sm font-medium text-gray-700">
                        Fitness Level
                      </label>
                      <select
                        id="fitnessLevel"
                        name="fitnessLevel"
                        defaultValue={userData.fitnessLevel}
                        className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      >
                        <option>Beginner</option>
                        <option>Intermediate</option>
                        <option>Advanced</option>
                        <option>Athletic</option>
                      </select>
                    </div>
                    
                    <div>
                      <label htmlFor="activityLevel" className="block text-sm font-medium text-gray-700">
                        Activity Level
                      </label>
                      <select
                        id="activityLevel"
                        name="activityLevel"
                        defaultValue={userData.activityLevel}
                        className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      >
                        <option>Sedentary (office job, little exercise)</option>
                        <option>Lightly active (light exercise 1-3 days/week)</option>
                        <option>Moderately active (moderate exercise 3-5 days/week)</option>
                        <option>Very active (hard exercise 6-7 days/week)</option>
                        <option>Extremely active (physical job, hard exercise daily)</option>
                      </select>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label htmlFor="workoutFrequency" className="block text-sm font-medium text-gray-700">
                          Workout Frequency
                        </label>
                        <select
                          id="workoutFrequency"
                          name="workoutFrequency"
                          defaultValue={userData.workoutFrequency}
                          className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        >
                          <option>1-2 times per week</option>
                          <option>3-4 times per week</option>
                          <option>4-5 times per week</option>
                          <option>6-7 times per week</option>
                        </select>
                      </div>
                      
                      <div>
                        <label htmlFor="workoutDuration" className="block text-sm font-medium text-gray-700">
                          Workout Duration
                        </label>
                        <select
                          id="workoutDuration"
                          name="workoutDuration"
                          defaultValue={userData.workoutDuration}
                          className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        >
                          <option>15-30 minutes</option>
                          <option>30-45 minutes</option>
                          <option>45-60 minutes</option>
                          <option>60-90 minutes</option>
                          <option>90+ minutes</option>
                        </select>
                      </div>
                    </div>
                    
                    <div>
                      <span className="block text-sm font-medium text-gray-700 mb-2">
                        Preferred Exercise Types
                      </span>
                      <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-4">
                        {['Weight training', 'Cardio', 'HIIT', 'Yoga', 'Pilates', 'Calisthenics', 'CrossFit', 'Running'].map((type) => (
                          <div key={type} className="flex items-center">
                            <input
                              id={`exercise-${type}`}
                              name="exerciseType"
                              type="checkbox"
                              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                              defaultChecked={type === 'Weight training' || type === 'Cardio'}
                            />
                            <label htmlFor={`exercise-${type}`} className="ml-2 block text-sm text-gray-700">
                              {type}
                            </label>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <label htmlFor="dietaryPreferences" className="block text-sm font-medium text-gray-700 mb-2">
                        Dietary Preferences
                      </label>
                      <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-4">
                        {['High protein', 'Low carb', 'Vegetarian', 'Vegan', 'Paleo', 'Keto', 'Mediterranean', 'Intermittent fasting'].map((diet) => (
                          <div key={diet} className="flex items-center">
                            <input
                              id={`diet-${diet}`}
                              name="dietaryPreferences"
                              type="checkbox"
                              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                              defaultChecked={userData.dietaryPreferences.includes(diet)}
                            />
                            <label htmlFor={`diet-${diet}`} className="ml-2 block text-sm text-gray-700">
                              {diet}
                            </label>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <button
                        type="submit"
                        className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                      >
                        <Save className="mr-2 -ml-1 h-5 w-5" />
                        Save Changes
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}
            
            {/* Goals */}
            {activeSection === 'goals' && (
              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-lg font-medium text-gray-900">Fitness Goals</h2>
                  <p className="mt-1 text-sm text-gray-500">
                    Set and track your fitness and health goals.
                  </p>
                </div>
                
                <div className="p-6">
                  <form className="space-y-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Primary Goals
                      </label>
                      <div className="space-y-2">
                        {['Weight loss', 'Muscle gain', 'Improved strength', 'Better endurance', 'Overall health', 'Sport-specific training'].map((goal) => (
                          <div key={goal} className="flex items-center">
                            <input
                              id={`goal-${goal}`}
                              name="primaryGoals"
                              type="checkbox"
                              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                              defaultChecked={userData.goals.includes(goal)}
                            />
                            <label htmlFor={`goal-${goal}`} className="ml-2 block text-sm text-gray-700">
                              {goal}
                            </label>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <span className="block text-sm font-medium text-gray-700 mb-3">
                        Specific Goals
                      </span>
                      
                      <div className="space-y-4">
                        {/* Weight Goal */}
                        <div className="border border-gray-200 rounded-md p-4">
                          <div 
                            className="flex justify-between items-center cursor-pointer"
                            onClick={() => toggleSection('weightGoal')}
                          >
                            <h3 className="text-sm font-medium text-gray-900">Weight Goal</h3>
                            {expandedSection === 'weightGoal' ? (
                              <ChevronUp className="h-5 w-5 text-gray-500" />
                            ) : (
                              <ChevronDown className="h-5 w-5 text-gray-500" />
                            )}
                          </div>
                          
                          {expandedSection === 'weightGoal' && (
                            <motion.div
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: 'auto', opacity: 1 }}
                              transition={{ duration: 0.3 }}
                              className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2"
                            >
                              <div>
                                <label htmlFor="currentWeight" className="block text-xs font-medium text-gray-700">
                                  Current Weight (lbs)
                                </label>
                                <input
                                  type="number"
                                  name="currentWeight"
                                  id="currentWeight"
                                  defaultValue={userData.weight}
                                  className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                              </div>
                              
                              <div>
                                <label htmlFor="targetWeight" className="block text-xs font-medium text-gray-700">
                                  Target Weight (lbs)
                                </label>
                                <input
                                  type="number"
                                  name="targetWeight"
                                  id="targetWeight"
                                  defaultValue="165"
                                  className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                              </div>
                              
                              <div className="sm:col-span-2">
                                <label htmlFor="weightGoalDate" className="block text-xs font-medium text-gray-700">
                                  Target Date
                                </label>
                                <input
                                  type="date"
                                  name="weightGoalDate"
                                  id="weightGoalDate"
                                  defaultValue="2025-09-30"
                                  className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                              </div>
                              
                              <div className="sm:col-span-2 pt-2">
                                <div className="w-full bg-gray-200 rounded-full h-2.5">
                                  <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: '55%' }}></div>
                                </div>
                                <div className="flex justify-between text-xs text-gray-500 mt-1">
                                  <span>88 kgs</span>
                                  <span>Current: 92 kgs</span>
                                  <span>Goal: 88kgs</span>
                                </div>
                              </div>
                            </motion.div>
                          )}
                        </div>
                        
                        {/* Strength Goal */}
                        <div className="border border-gray-200 rounded-md p-4">
                          <div 
                            className="flex justify-between items-center cursor-pointer"
                            onClick={() => toggleSection('strengthGoal')}
                          >
                            <h3 className="text-sm font-medium text-gray-900">Strength Goal</h3>
                            {expandedSection === 'strengthGoal' ? (
                              <ChevronUp className="h-5 w-5 text-gray-500" />
                            ) : (
                              <ChevronDown className="h-5 w-5 text-gray-500" />
                            )}
                          </div>
                          
                          {expandedSection === 'strengthGoal' && (
                            <motion.div
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: 'auto', opacity: 1 }}
                              transition={{ duration: 0.3 }}
                              className="mt-4 space-y-4"
                            >
                              <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                                <div>
                                  <label htmlFor="benchPress" className="block text-xs font-medium text-gray-700">
                                    Bench Press (kgs)
                                  </label>
                                  <input
                                    type="number"
                                    name="benchPress"
                                    id="benchPress"
                                    defaultValue="100"
                                    className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                  />
                                </div>
                                
                                <div>
                                  <label htmlFor="squat" className="block text-xs font-medium text-gray-700">
                                    Squat (kgs)
                                  </label>
                                  <input
                                    type="number"
                                    name="squat"
                                    id="squat"
                                    defaultValue="150"
                                    className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                  />
                                </div>
                                
                                <div>
                                  <label htmlFor="deadlift" className="block text-xs font-medium text-gray-700">
                                    Deadlift (kgs)
                                  </label>
                                  <input
                                    type="number"
                                    name="deadlift"
                                    id="deadlift"
                                    defaultValue="150"
                                    className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                  />
                                </div>
                              </div>
                              
                              <div>
                                <label htmlFor="strengthGoalDate" className="block text-xs font-medium text-gray-700">
                                  Target Date
                                </label>
                                <input
                                  type="date"
                                  name="strengthGoalDate"
                                  id="strengthGoalDate"
                                  defaultValue="2025-11-30"
                                  className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                              </div>
                              
                              <div>
                                <div className="flex justify-between mb-1">
                                  <span className="text-xs font-medium text-gray-700">Bench Press Progress</span>
                                  <span className="text-xs font-medium text-blue-600">96/100 kgs (96%)</span>
                                </div>
                                <div className="w-full bg-gray-200 rounded-full h-2">
                                  <div className="bg-blue-600 h-2 rounded-full" style={{ width: '96%' }}></div>
                                </div>
                              </div>
                              
                              <div>
                                <div className="flex justify-between mb-1">
                                  <span className="text-xs font-medium text-gray-700">Squat Progress</span>
                                  <span className="text-xs font-medium text-blue-600">120/150 kgs (90%)</span>
                                </div>
                                <div className="w-full bg-gray-200 rounded-full h-2">
                                  <div className="bg-blue-600 h-2 rounded-full" style={{ width: '90%' }}></div>
                                </div>
                              </div>
                              
                              <div>
                                <div className="flex justify-between mb-1">
                                  <span className="text-xs font-medium text-gray-700">Deadlift Progress</span>
                                  <span className="text-xs font-medium text-blue-600">150/170 kgs (89%)</span>
                                </div>
                                <div className="w-full bg-gray-200 rounded-full h-2">
                                  <div className="bg-blue-600 h-2 rounded-full" style={{ width: '89%' }}></div>
                                </div>
                              </div>
                            </motion.div>
                          )}
                        </div>
                        
                        {/* Body Composition Goal */}
                        <div className="border border-gray-200 rounded-md p-4">
                          <div 
                            className="flex justify-between items-center cursor-pointer"
                            onClick={() => toggleSection('bodyCompGoal')}
                          >
                            <h3 className="text-sm font-medium text-gray-900">Body Composition Goal</h3>
                            {expandedSection === 'bodyCompGoal' ? (
                              <ChevronUp className="h-5 w-5 text-gray-500" />
                            ) : (
                              <ChevronDown className="h-5 w-5 text-gray-500" />
                            )}
                          </div>
                          
                          {expandedSection === 'bodyCompGoal' && (
                            <motion.div
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: 'auto', opacity: 1 }}
                              transition={{ duration: 0.3 }}
                              className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2"
                            >
                              <div>
                                <label htmlFor="currentBodyFat" className="block text-xs font-medium text-gray-700">
                                  Current Body Fat %
                                </label>
                                <input
                                  type="number"
                                  step="0.1"
                                  name="currentBodyFat"
                                  id="currentBodyFat"
                                  defaultValue="19"
                                  className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                              </div>
                              
                              <div>
                                <label htmlFor="targetBodyFat" className="block text-xs font-medium text-gray-700">
                                  Target Body Fat %
                                </label>
                                <input
                                  type="number"
                                  step="0.1"
                                  name="targetBodyFat"
                                  id="targetBodyFat"
                                  defaultValue="15"
                                  className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                              </div>
                              
                              <div>
                                <label htmlFor="currentMuscleMass" className="block text-xs font-medium text-gray-700">
                                  Current Muscle Mass (lbs)
                                </label>
                                <input
                                  type="number"
                                  step="0.1"
                                  name="currentMuscleMass"
                                  id="currentMuscleMass"
                                  defaultValue="143"
                                  className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                              </div>
                              
                              <div>
                                <label htmlFor="targetMuscleMass" className="block text-xs font-medium text-gray-700">
                                  Target Muscle Mass (kgs)
                                </label>
                                <input
                                  type="number"
                                  step="0.1"
                                  name="targetMuscleMass"
                                  id="targetMuscleMass"
                                  defaultValue="145"
                                  className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                              </div>
                              
                              <div className="sm:col-span-2">
                                <label htmlFor="bodyCompGoalDate" className="block text-xs font-medium text-gray-700">
                                  Target Date
                                </label>
                                <input
                                  type="date"
                                  name="bodyCompGoalDate"
                                  id="bodyCompGoalDate"
                                  defaultValue="2025-10-31"
                                  className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                              </div>
                            </motion.div>
                          )}
                        </div>
                      </div>
                    </div>
                    
                    <div>
                      <button
                        type="submit"
                        className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                      >
                        <Save className="mr-2 -ml-1 h-5 w-5" />
                        Save Goals
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}
            
            {/* Health Data */}
            {activeSection === 'healthData' && (
              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-lg font-medium text-gray-900">Health Information</h2>
                  <p className="mt-1 text-sm text-gray-500">
                    Provide health details to help personalize your experience.
                  </p>
                </div>
                
                <div className="p-6">
                  <form className="space-y-6">
                    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                      <div>
                        <label htmlFor="allergies" className="block text-sm font-medium text-gray-700">
                          Food Allergies/Intolerances
                        </label>
                        <textarea
                          id="allergies"
                          name="allergies"
                          rows={3}
                          defaultValue={userData.allergies.join(', ')}
                          className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                          placeholder="List any food allergies or intolerances"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="medicalConditions" className="block text-sm font-medium text-gray-700">
                          Medical Conditions
                        </label>
                        <textarea
                          id="medicalConditions"
                          name="medicalConditions"
                          rows={3}
                          defaultValue={userData.medicalConditions.join(', ')}
                          className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                          placeholder="List any medical conditions that might affect your fitness plan"
                        />
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                      <div>
                        <label htmlFor="sleepAverage" className="block text-sm font-medium text-gray-700">
                          Average Sleep Duration
                        </label>
                        <select
                          id="sleepAverage"
                          name="sleepAverage"
                          defaultValue={userData.sleepAverage}
                          className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        >
                          <option>Less than 5 hours</option>
                          <option>5-6 hours</option>
                          <option>6-7 hours</option>
                          <option>7 hours</option>
                          <option>7-8 hours</option>
                          <option>8-9 hours</option>
                          <option>More than 9 hours</option>
                        </select>
                      </div>
                      
                      <div>
                        <label htmlFor="stressLevel" className="block text-sm font-medium text-gray-700">
                          Stress Level
                        </label>
                        <select
                          id="stressLevel"
                          name="stressLevel"
                          defaultValue={userData.stressLevel}
                          className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        >
                          <option>Low</option>
                          <option>Moderate</option>
                          <option>High</option>
                          <option>Very high</option>
                        </select>
                      </div>
                    </div>
                    
                    <div>
                      <span className="block text-sm font-medium text-gray-700 mb-2">
                        Physical Limitations or Injuries
                      </span>
                      <div className="space-y-2">
                        {['Shoulder', 'Back', 'Knee', 'Hip', 'Ankle', 'Wrist', 'Neck', 'None'].map((area) => (
                          <div key={area} className="flex items-center">
                            <input
                              id={`injury-${area}`}
                              name="injuries"
                              type="checkbox"
                              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                              defaultChecked={area === 'None'}
                            />
                            <label htmlFor={`injury-${area}`} className="ml-2 block text-sm text-gray-700">
                              {area}
                            </label>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <label htmlFor="injuryDetails" className="block text-sm font-medium text-gray-700">
                        Injury Details
                      </label>
                      <textarea
                        id="injuryDetails"
                        name="injuryDetails"
                        rows={3}
                        className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                        placeholder="Provide details about any injuries or limitations"
                      />
                    </div>
                    
                    <div>
                      <button
                        type="submit"
                        className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                      >
                        <Save className="mr-2 -ml-1 h-5 w-5" />
                        Save Health Information
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}
            
            {/* Account Settings */}
            {activeSection === 'accountSettings' && (
              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-lg font-medium text-gray-900">Account Settings</h2>
                  <p className="mt-1 text-sm text-gray-500">
                    Manage your account settings and security.
                  </p>
                </div>
                
                <div className="p-6 space-y-8">
                  <div>
                    <h3 className="text-base font-medium text-gray-900 mb-4">Email and Password</h3>
                    <form className="space-y-4">
                      <div>
                        <label htmlFor="accountEmail" className="block text-sm font-medium text-gray-700">
                          Email Address
                        </label>
                        <div className="mt-1 flex rounded-md shadow-sm">
                          <input
                            type="email"
                            name="accountEmail"
                            id="accountEmail"
                            defaultValue={userData.email}
                            className="focus:ring-blue-500 focus:border-blue-500 flex-1 block w-full rounded-md sm:text-sm border-gray-300"
                            placeholder="you@example.com"
                          />
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                        <div className="sm:col-span-1">
                          <label htmlFor="currentPassword" className="block text-sm font-medium text-gray-700">
                            Current Password
                          </label>
                          <input
                            type="password"
                            name="currentPassword"
                            id="currentPassword"
                            className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                          />
                        </div>
                        
                        <div className="sm:col-span-1">
                          <label htmlFor="newPassword" className="block text-sm font-medium text-gray-700">
                            New Password
                          </label>
                          <input
                            type="password"
                            name="newPassword"
                            id="newPassword"
                            className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                          />
                        </div>
                        
                        <div className="sm:col-span-1">
                          <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                            Confirm New Password
                          </label>
                          <input
                            type="password"
                            name="confirmPassword"
                            id="confirmPassword"
                            className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                          />
                        </div>
                      </div>
                      
                      <div>
                        <button
                          type="submit"
                          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                        >
                          Update Email & Password
                        </button>
                      </div>
                    </form>
                  </div>
                  
                  <div className="pt-6 border-t border-gray-200">
                    <h3 className="text-base font-medium text-gray-900 mb-4">Data Privacy</h3>
                    <div className="space-y-4">
                      <div className="flex items-start">
                        <div className="flex items-center h-5">
                          <input
                            id="dataSharing"
                            name="dataSharing"
                            type="checkbox"
                            className="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                            defaultChecked
                          />
                        </div>
                        <div className="ml-3 text-sm">
                          <label htmlFor="dataSharing" className="font-medium text-gray-700">Share fitness data with AI</label>
                          <p className="text-gray-500">Allow our AI to analyze your fitness data to provide personalized recommendations</p>
                        </div>
                      </div>
                      
                      <div className="flex items-start">
                        <div className="flex items-center h-5">
                          <input
                            id="analytics"
                            name="analytics"
                            type="checkbox"
                            className="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                            defaultChecked
                          />
                        </div>
                        <div className="ml-3 text-sm">
                          <label htmlFor="analytics" className="font-medium text-gray-700">Anonymous analytics</label>
                          <p className="text-gray-500">Allow anonymous usage data to help improve our services</p>
                        </div>
                      </div>
                      
                      <div className="flex items-start">
                        <div className="flex items-center h-5">
                          <input
                            id="marketing"
                            name="marketing"
                            type="checkbox"
                            className="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                          />
                        </div>
                        <div className="ml-3 text-sm">
                          <label htmlFor="marketing" className="font-medium text-gray-700">Marketing communications</label>
                          <p className="text-gray-500">Receive marketing emails about new features and offers</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-4">
                      <button
                        type="button"
                        className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                      >
                        Save Privacy Settings
                      </button>
                    </div>
                  </div>
                  
                  <div className="pt-6 border-t border-gray-200">
                    <h3 className="text-base font-medium text-gray-900 mb-4">Account Actions</h3>
                    <div className="space-y-4">
                      <div>
                        <button
                          type="button"
                          className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                        >
                          Download Your Data
                        </button>
                      </div>
                      
                      <div>
                        <button
                          type="button"
                          className="inline-flex items-center px-4 py-2 border border-red-300 rounded-md shadow-sm text-sm font-medium text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                        >
                          Delete Account
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {/* Notifications */}
            {activeSection === 'notifications' && (
              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-lg font-medium text-gray-900">Notification Settings</h2>
                  <p className="mt-1 text-sm text-gray-500">
                    Manage how and when you receive notifications.
                  </p>
                </div>
                
                <div className="p-6">
                  <form className="space-y-6">
                    <div>
                      <h3 className="text-base font-medium text-gray-900 mb-4">Email Notifications</h3>
                      <div className="space-y-4">
                        <div className="flex items-start">
                          <div className="flex items-center h-5">
                            <input
                              id="emailWorkoutReminders"
                              name="emailWorkoutReminders"
                              type="checkbox"
                              className="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                              defaultChecked
                            />
                          </div>
                          <div className="ml-3 text-sm">
                            <label htmlFor="emailWorkoutReminders" className="font-medium text-gray-700">Workout reminders</label>
                            <p className="text-gray-500">Receive email reminders for scheduled workouts</p>
                          </div>
                        </div>
                        
                        <div className="flex items-start">
                          <div className="flex items-center h-5">
                            <input
                              id="emailProgressUpdates"
                              name="emailProgressUpdates"
                              type="checkbox"
                              className="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                              defaultChecked
                            />
                          </div>
                          <div className="ml-3 text-sm">
                            <label htmlFor="emailProgressUpdates" className="font-medium text-gray-700">Progress updates</label>
                            <p className="text-gray-500">Weekly summaries of your fitness progress</p>
                          </div>
                        </div>
                        
                        <div className="flex items-start">
                          <div className="flex items-center h-5">
                            <input
                              id="emailAchievements"
                              name="emailAchievements"
                              type="checkbox"
                              className="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                              defaultChecked
                            />
                          </div>
                          <div className="ml-3 text-sm">
                            <label htmlFor="emailAchievements" className="font-medium text-gray-700">Achievements</label>
                            <p className="text-gray-500">Notifications when you reach fitness milestones</p>
                          </div>
                        </div>
                        
                        <div className="flex items-start">
                          <div className="flex items-center h-5">
                            <input
                              id="emailTips"
                              name="emailTips"
                              type="checkbox"
                              className="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                            />
                          </div>
                          <div className="ml-3 text-sm">
                            <label htmlFor="emailTips" className="font-medium text-gray-700">Tips and advice</label>
                            <p className="text-gray-500">Personalized fitness and nutrition tips from our AI</p>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="pt-6 border-t border-gray-200">
                      <h3 className="text-base font-medium text-gray-900 mb-4">Push Notifications</h3>
                      <div className="space-y-4">
                        <div className="flex items-start">
                          <div className="flex items-center h-5">
                            <input
                              id="pushWorkoutReminders"
                              name="pushWorkoutReminders"
                              type="checkbox"
                              className="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                              defaultChecked
                            />
                          </div>
                          <div className="ml-3 text-sm">
                            <label htmlFor="pushWorkoutReminders" className="font-medium text-gray-700">Workout reminders</label>
                            <p className="text-gray-500">Receive push notifications for scheduled workouts</p>
                          </div>
                        </div>
                        
                        <div className="flex items-start">
                          <div className="flex items-center h-5">
                            <input
                              id="pushMealReminders"
                              name="pushMealReminders"
                              type="checkbox"
                              className="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                              defaultChecked
                            />
                          </div>
                          <div className="ml-3 text-sm">
                            <label htmlFor="pushMealReminders" className="font-medium text-gray-700">Meal reminders</label>
                            <p className="text-gray-500">Receive push notifications for scheduled meals</p>
                          </div>
                        </div>
                        
                        <div className="flex items-start">
                          <div className="flex items-center h-5">
                            <input
                              id="pushAchievements"
                              name="pushAchievements"
                              type="checkbox"
                              className="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                              defaultChecked
                            />
                          </div>
                          <div className="ml-3 text-sm">
                            <label htmlFor="pushAchievements" className="font-medium text-gray-700">Achievements</label>
                            <p className="text-gray-500">Notifications when you reach fitness milestones</p>
                          </div>
                        </div>
                        
                        <div className="flex items-start">
                          <div className="flex items-center h-5">
                            <input
                              id="pushUpdates"
                              name="pushUpdates"
                              type="checkbox"
                              className="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                            />
                          </div>
                          <div className="ml-3 text-sm">
                            <label htmlFor="pushUpdates" className="font-medium text-gray-700">App updates</label>
                            <p className="text-gray-500">Notifications about new features and improvements</p>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="pt-6 border-t border-gray-200">
                      <h3 className="text-base font-medium text-gray-900 mb-4">Notification Frequency</h3>
                      <div className="max-w-lg">
                        <div>
                          <label htmlFor="reminderTiming" className="block text-sm font-medium text-gray-700">
                            Workout reminder timing
                          </label>
                          <select
                            id="reminderTiming"
                            name="reminderTiming"
                            className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                            defaultValue="30"
                          >
                            <option value="15">15 minutes before</option>
                            <option value="30">30 minutes before</option>
                            <option value="60">1 hour before</option>
                            <option value="120">2 hours before</option>
                            <option value="day">Day before (8pm)</option>
                          </select>
                        </div>
                        
                        <div className="mt-4">
                          <label htmlFor="progressFrequency" className="block text-sm font-medium text-gray-700">
                            Progress update frequency
                          </label>
                          <select
                            id="progressFrequency"
                            name="progressFrequency"
                            className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                            defaultValue="weekly"
                          >
                            <option value="daily">Daily</option>
                            <option value="weekly">Weekly</option>
                            <option value="biweekly">Bi-weekly</option>
                            <option value="monthly">Monthly</option>
                          </select>
                        </div>
                      </div>
                    </div>
                    
                    <div>
                      <button
                        type="submit"
                        className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                      >
                        <Save className="mr-2 -ml-1 h-5 w-5" />
                        Save Notification Settings
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;