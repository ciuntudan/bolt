import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { motion } from 'framer-motion';
import { authAPI } from '../../services/api';
import {
  User as UserIcon, Mail, Lock, FileText, ChevronDown, ChevronUp,
  BarChart2, Activity, Target, Bell, Settings, Save, Loader2
} from 'lucide-react';
import type { Profile } from '../../services/api';
import type { AuthContextType } from '../../hooks/useAuth';

// Define types
interface UserData {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  profile: Profile;
}

const ProfilePage: React.FC = () => {
  const auth = useAuth();
  const [activeSection, setActiveSection] = useState('personalInfo');
  const [expandedSection, setExpandedSection] = useState('');
  const [loading, setLoading] = useState(false);
  const [profileData, setProfileData] = useState<Profile | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  
  // Show loading while auth is being initialized
  if (!auth || auth.loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!auth.isAuthenticated || !auth.user) {
    window.location.href = '/login';
    return null;
  }

  const toggleSection = (section: string) => {
    setExpandedSection(expandedSection === section ? '' : section);
  };

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        setLoading(true);
        const data = await authAPI.getProfile();
        setProfileData(data);
        setError(null);
      } catch (err) {
        setError('Failed to load profile data');
        console.error('Error fetching profile:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProfileData();
  }, []);

  const handleProfileUpdate = async (formData: Partial<Profile>) => {
    try {
      setLoading(true);
      setError(null);
      setSuccessMessage(null);
      
      const data = await authAPI.updateProfile(formData);
      setProfileData(data);
      setSuccessMessage('Profile updated successfully');
      
      // Update the auth context
      auth.updateProfile(data);
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Failed to update profile';
      setError(errorMessage);
      console.error('Error updating profile:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-red-500">{error}</div>
      </div>
    );
  }

  // Sample user data (would come from context in real app)
  const userData = {
    name: auth.user?.first_name + ' ' + auth.user?.last_name || 'Ciuntu Daniel',
    email: auth.user?.email || 'dan.ciuntug7@gmail.com',
    age: auth.user?.profile?.age || 22,
    height: auth.user?.profile?.height || 185,
    weight: auth.user?.profile?.weight || 92,
    gender: auth.user?.profile?.gender || 'Male',
    goals: ['Weight loss', 'Muscle gain', 'Improved strength'],
    fitnessLevel: auth.user?.profile?.fitness_level || 'Intermediate',
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
                    src={profileData?.avatar || "./bbr_black.png"}
                    alt={`${auth.user?.first_name} ${auth.user?.last_name}`}
                    className="h-full w-full object-cover"
                  />
                  <div className="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 flex items-center justify-center transition-all duration-300 cursor-pointer">
                    <div className="text-white opacity-0 hover:opacity-100 text-xs font-medium">
                      Change Photo
                    </div>
                  </div>
                </div>
                <h2 className="text-xl font-bold text-gray-900">{`${auth.user?.first_name} ${auth.user?.last_name}`}</h2>
                <p className="text-sm text-gray-500">{auth.user?.email}</p>
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
                      <UserIcon className="mr-3 h-5 w-5" />
                      Personal Information
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
                  <form onSubmit={(e) => {
                    e.preventDefault();
                    const formData = new FormData(e.currentTarget);
                    handleProfileUpdate({
                      age: parseInt(formData.get('age') as string),
                      height: parseFloat(formData.get('height') as string),
                      weight: parseFloat(formData.get('weight') as string),
                      gender: formData.get('gender') as Profile['gender'],
                      fitness_level: formData.get('fitness_level') as Profile['fitness_level'],
                    });
                  }} className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label htmlFor="first_name" className="block text-sm font-medium text-gray-700">
                          First Name
                        </label>
                        <input
                          type="text"
                          name="first_name"
                          id="first_name"
                          defaultValue={auth.user?.first_name}
                          disabled
                          className="mt-1 bg-gray-50 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="last_name" className="block text-sm font-medium text-gray-700">
                          Last Name
                        </label>
                        <input
                          type="text"
                          name="last_name"
                          id="last_name"
                          defaultValue={auth.user?.last_name}
                          disabled
                          className="mt-1 bg-gray-50 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
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
                          defaultValue={auth.user?.email}
                          disabled
                          className="mt-1 bg-gray-50 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
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
                          defaultValue={profileData?.age}
                          min={13}
                          max={120}
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
                          defaultValue={profileData?.gender}
                          className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        >
                          <option value="male">Male</option>
                          <option value="female">Female</option>
                          <option value="other">Other</option>
                        </select>
                      </div>
                      
                      <div>
                        <label htmlFor="height" className="block text-sm font-medium text-gray-700">
                          Height (cm)
                        </label>
                        <input
                          type="number"
                          name="height"
                          id="height"
                          defaultValue={profileData?.height}
                          min={100}
                          max={250}
                          step="0.1"
                          className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="weight" className="block text-sm font-medium text-gray-700">
                          Weight (kg)
                        </label>
                        <input
                          type="number"
                          name="weight"
                          id="weight"
                          defaultValue={profileData?.weight}
                          min={30}
                          max={300}
                          step="0.1"
                          className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="fitness_level" className="block text-sm font-medium text-gray-700">
                          Fitness Level
                        </label>
                        <select
                          id="fitness_level"
                          name="fitness_level"
                          defaultValue={profileData?.fitness_level}
                          className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        >
                          <option value="beginner">Beginner</option>
                          <option value="intermediate">Intermediate</option>
                          <option value="advanced">Advanced</option>
                        </select>
                      </div>
                    </div>
                    
                    <div>
                      <button
                        type="submit"
                        disabled={loading}
                        className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                      >
                        <Save className="mr-2 -ml-1 h-5 w-5" />
                        {loading ? 'Saving...' : 'Save Changes'}
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
                  <form className="space-y-6" onSubmit={e => {
                    e.preventDefault();
                    const formData = new FormData(e.currentTarget);
                    handleProfileUpdate({
                      // Only update weight and strength goals
                      target_weight: formData.get('targetWeight') ? parseFloat(formData.get('targetWeight') as string) : undefined,
                      weight_goal_date: formData.get('weightGoalDate') as string,
                      bench_press_goal: formData.get('benchPress') ? parseFloat(formData.get('benchPress') as string) : undefined,
                      squat_goal: formData.get('squat') ? parseFloat(formData.get('squat') as string) : undefined,
                      deadlift_goal: formData.get('deadlift') ? parseFloat(formData.get('deadlift') as string) : undefined,
                      strength_goal_date: formData.get('strengthGoalDate') as string,
                    });
                  }}>
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
                                Current Weight (kgs)
                              </label>
                              <input
                                type="number"
                                name="currentWeight"
                                id="currentWeight"
                                defaultValue={userData.weight}
                                className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                disabled
                              />
                            </div>
                            <div>
                              <label htmlFor="targetWeight" className="block text-xs font-medium text-gray-700">
                                Target Weight (kgs)
                              </label>
                              <input
                                type="number"
                                name="targetWeight"
                                id="targetWeight"
                                defaultValue="88"
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
                          </motion.div>
                        )}
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

      {/* Show success message */}
      {successMessage && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-4">
          <div className="bg-green-50 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
            <span className="block sm:inline">{successMessage}</span>
          </div>
        </div>
      )}
      
      {/* Show error message */}
      {error && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-4">
          <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <span className="block sm:inline">{error}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProfilePage;