import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  LineChart, Line, AreaChart, Area, BarChart, Bar, 
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { 
  Calendar, ChevronLeft, ChevronRight, 
  TrendingUp, Zap, Award, Target, BarChart2
} from 'lucide-react';

// Sample progress data
const bodyMetricsData = [
  { date: '2025-05-01', weight: 185, bodyFat: 22, muscleMass: 140 },
  { date: '2025-05-08', weight: 183, bodyFat: 21.5, muscleMass: 140.5 },
  { date: '2025-05-15', weight: 181, bodyFat: 21, muscleMass: 141 },
  { date: '2025-05-22', weight: 179, bodyFat: 20.5, muscleMass: 141.5 },
  { date: '2025-05-29', weight: 178, bodyFat: 20, muscleMass: 142 },
  { date: '2025-06-05', weight: 176, bodyFat: 19.5, muscleMass: 142.5 },
  { date: '2025-06-12', weight: 174, bodyFat: 19, muscleMass: 143 }
];

const strengthMetricsData = [
  { date: '2025-05-01', bench: 185, squat: 225, deadlift: 275 },
  { date: '2025-05-08', bench: 190, squat: 235, deadlift: 280 },
  { date: '2025-05-15', bench: 195, squat: 245, deadlift: 290 },
  { date: '2025-05-22', bench: 200, squat: 255, deadlift: 300 },
  { date: '2025-05-29', bench: 205, squat: 265, deadlift: 305 },
  { date: '2025-06-05', bench: 210, squat: 275, deadlift: 315 },
  { date: '2025-06-12', bench: 215, squat: 285, deadlift: 325 }
];

const workoutMetricsData = [
  { week: 'Week 1', workoutCount: 4, totalMinutes: 205, avgIntensity: 7.2 },
  { week: 'Week 2', workoutCount: 5, totalMinutes: 255, avgIntensity: 7.5 },
  { week: 'Week 3', workoutCount: 4, totalMinutes: 220, avgIntensity: 7.8 },
  { week: 'Week 4', workoutCount: 5, totalMinutes: 265, avgIntensity: 8.0 },
  { week: 'Week 5', workoutCount: 5, totalMinutes: 270, avgIntensity: 8.2 },
  { week: 'Week 6', workoutCount: 6, totalMinutes: 310, avgIntensity: 8.5 },
  { week: 'Week 7', workoutCount: 5, totalMinutes: 280, avgIntensity: 8.7 }
];

const nutritionData = [
  { week: 'Week 1', calorieAdherence: 85, proteinAdherence: 90, waterIntake: 75 },
  { week: 'Week 2', calorieAdherence: 88, proteinAdherence: 92, waterIntake: 80 },
  { week: 'Week 3', calorieAdherence: 86, proteinAdherence: 94, waterIntake: 82 },
  { week: 'Week 4', calorieAdherence: 90, proteinAdherence: 95, waterIntake: 85 },
  { week: 'Week 5', calorieAdherence: 92, proteinAdherence: 96, waterIntake: 88 },
  { week: 'Week 6', calorieAdherence: 94, proteinAdherence: 97, waterIntake: 90 },
  { week: 'Week 7', calorieAdherence: 93, proteinAdherence: 98, waterIntake: 92 }
];

const recentAchievements = [
  {
    id: 1,
    title: 'Strength Milestone',
    description: 'Reached 215 lbs on bench press',
    date: '2025-06-12',
    icon: 'dumbbell',
    color: 'blue'
  },
  {
    id: 2,
    title: 'Weight Goal Achievement',
    description: 'Dropped below 175 lbs',
    date: '2025-06-10',
    icon: 'scale',
    color: 'green'
  },
  {
    id: 3,
    title: 'Consistency Champion',
    description: '4 weeks of perfect workout adherence',
    date: '2025-06-05',
    icon: 'calendar',
    color: 'purple'
  },
  {
    id: 4,
    title: 'Nutrition Master',
    description: 'Met protein goals for 30 days straight',
    date: '2025-05-28',
    icon: 'apple',
    color: 'yellow'
  }
];

// Chart config
const chartConfig = {
  bodyMetrics: {
    title: 'Body Composition',
    description: 'Track changes in weight, body fat percentage, and muscle mass over time.',
    metrics: [
      { key: 'weight', name: 'Weight (lbs)', color: '#3B82F6' },
      { key: 'bodyFat', name: 'Body Fat %', color: '#F97316' },
      { key: 'muscleMass', name: 'Muscle Mass (lbs)', color: '#10B981' }
    ]
  },
  strengthMetrics: {
    title: 'Strength Progression',
    description: 'Monitor your progress on key compound lifts over time.',
    metrics: [
      { key: 'bench', name: 'Bench Press (lbs)', color: '#8B5CF6' },
      { key: 'squat', name: 'Squat (lbs)', color: '#EC4899' },
      { key: 'deadlift', name: 'Deadlift (lbs)', color: '#F59E0B' }
    ]
  }
};

const ProgressPage: React.FC = () => {
  const [timeRange, setTimeRange] = useState('7W');
  const [activeTab, setActiveTab] = useState('body');
  
  const handleTimeRangeChange = (range: string) => {
    setTimeRange(range);
  };
  
  return (
    <div className="bg-gray-50 pt-8 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Your Progress</h1>
          <p className="mt-2 text-gray-600">
            Track your fitness journey with detailed metrics and visualizations.
          </p>
        </div>

        {/* Time range selector */}
        <div className="bg-white rounded-lg shadow mb-8">
          <div className="p-4 flex items-center justify-between">
            <div className="flex items-center">
              <Calendar className="mr-2 h-5 w-5 text-gray-500" />
              <span className="text-gray-700 font-medium">Time Range:</span>
            </div>
            
            <div className="flex border border-gray-300 rounded-md">
              <button
                className={`px-3 py-1 text-sm ${timeRange === '1M' ? 'bg-blue-100 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}`}
                onClick={() => handleTimeRangeChange('1M')}
              >
                1M
              </button>
              <button
                className={`px-3 py-1 text-sm ${timeRange === '3M' ? 'bg-blue-100 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}`}
                onClick={() => handleTimeRangeChange('3M')}
              >
                3M
              </button>
              <button
                className={`px-3 py-1 text-sm ${timeRange === '7W' ? 'bg-blue-100 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}`}
                onClick={() => handleTimeRangeChange('7W')}
              >
                7W
              </button>
              <button
                className={`px-3 py-1 text-sm ${timeRange === '1Y' ? 'bg-blue-100 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}`}
                onClick={() => handleTimeRangeChange('1Y')}
              >
                1Y
              </button>
              <button
                className={`px-3 py-1 text-sm ${timeRange === 'ALL' ? 'bg-blue-100 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}`}
                onClick={() => handleTimeRangeChange('ALL')}
              >
                ALL
              </button>
            </div>
            
            <div className="flex items-center space-x-2">
              <button className="p-1 rounded-full hover:bg-gray-100">
                <ChevronLeft className="h-5 w-5 text-gray-500" />
              </button>
              <button className="p-1 rounded-full hover:bg-gray-100">
                <ChevronRight className="h-5 w-5 text-gray-500" />
              </button>
            </div>
          </div>
        </div>

        {/* Metrics summary cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <motion.div 
            whileHover={{ y: -5 }}
            className="bg-white rounded-lg shadow p-6"
          >
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-blue-100 text-blue-600">
                <TrendingUp size={24} />
              </div>
              <div className="ml-4">
                <h2 className="text-sm font-medium text-gray-500">Weight Change</h2>
                <div className="flex items-center">
                  <p className="text-2xl font-bold text-gray-900">-11 lbs</p>
                  <span className="ml-2 text-green-500 text-sm">-5.9%</span>
                </div>
                <p className="text-xs text-gray-500">Since program start</p>
              </div>
            </div>
          </motion.div>
          
          <motion.div 
            whileHover={{ y: -5 }}
            className="bg-white rounded-lg shadow p-6"
          >
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-green-100 text-green-600">
                <BarChart2 size={24} />
              </div>
              <div className="ml-4">
                <h2 className="text-sm font-medium text-gray-500">Strength Increase</h2>
                <div className="flex items-center">
                  <p className="text-2xl font-bold text-gray-900">+16%</p>
                  <span className="ml-2 text-green-500 text-sm">↑</span>
                </div>
                <p className="text-xs text-gray-500">Average across lifts</p>
              </div>
            </div>
          </motion.div>
          
          <motion.div 
            whileHover={{ y: -5 }}
            className="bg-white rounded-lg shadow p-6"
          >
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-yellow-100 text-yellow-600">
                <Zap size={24} />
              </div>
              <div className="ml-4">
                <h2 className="text-sm font-medium text-gray-500">Workout Consistency</h2>
                <div className="flex items-center">
                  <p className="text-2xl font-bold text-gray-900">92%</p>
                  <span className="ml-2 text-green-500 text-sm">+3%</span>
                </div>
                <p className="text-xs text-gray-500">34 of 37 completed</p>
              </div>
            </div>
          </motion.div>
          
          <motion.div 
            whileHover={{ y: -5 }}
            className="bg-white rounded-lg shadow p-6"
          >
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-purple-100 text-purple-600">
                <Target size={24} />
              </div>
              <div className="ml-4">
                <h2 className="text-sm font-medium text-gray-500">Goal Progress</h2>
                <div className="flex items-center">
                  <p className="text-2xl font-bold text-gray-900">67%</p>
                  <span className="ml-2 text-green-500 text-sm">On track</span>
                </div>
                <p className="text-xs text-gray-500">2/3 milestones hit</p>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Main content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Charts (left side) */}
          <div className="lg:col-span-2 space-y-8">
            {/* Chart tabs */}
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <div className="border-b border-gray-200">
                <nav className="flex -mb-px">
                  <button
                    className={`py-4 px-6 text-center border-b-2 text-sm font-medium ${
                      activeTab === 'body'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                    onClick={() => setActiveTab('body')}
                  >
                    Body Metrics
                  </button>
                  <button
                    className={`py-4 px-6 text-center border-b-2 text-sm font-medium ${
                      activeTab === 'strength'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                    onClick={() => setActiveTab('strength')}
                  >
                    Strength Metrics
                  </button>
                  <button
                    className={`py-4 px-6 text-center border-b-2 text-sm font-medium ${
                      activeTab === 'workouts'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                    onClick={() => setActiveTab('workouts')}
                  >
                    Workout Data
                  </button>
                  <button
                    className={`py-4 px-6 text-center border-b-2 text-sm font-medium ${
                      activeTab === 'nutrition'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                    onClick={() => setActiveTab('nutrition')}
                  >
                    Nutrition
                  </button>
                </nav>
              </div>
              
              <div className="p-6">
                {/* Body Metrics Chart */}
                {activeTab === 'body' && (
                  <div>
                    <div className="mb-4">
                      <h2 className="text-lg font-medium text-gray-900">
                        {chartConfig.bodyMetrics.title}
                      </h2>
                      <p className="mt-1 text-sm text-gray-500">
                        {chartConfig.bodyMetrics.description}
                      </p>
                    </div>
                    
                    <div className="h-80">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart
                          data={bodyMetricsData}
                          margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                        >
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis 
                            dataKey="date" 
                            tickFormatter={(date) => {
                              return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                            }}
                          />
                          <YAxis />
                          <Tooltip 
                            formatter={(value, name) => [
                              value, 
                              name === 'Weight (lbs)' || name === 'Muscle Mass (lbs)' 
                                ? `${name}` 
                                : name
                            ]}
                            labelFormatter={(date) => {
                              return new Date(date).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
                            }}
                          />
                          <Legend />
                          {chartConfig.bodyMetrics.metrics.map((metric) => (
                            <Line
                              key={metric.key}
                              type="monotone"
                              dataKey={metric.key}
                              name={metric.name}
                              stroke={metric.color}
                              activeDot={{ r: 8 }}
                            />
                          ))}
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                    
                    <div className="mt-6 pt-6 border-t border-gray-200 grid grid-cols-3 gap-4">
                      <div>
                        <p className="text-sm text-gray-500">Current Weight</p>
                        <p className="font-medium text-gray-900">174 lbs</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">Body Fat %</p>
                        <p className="font-medium text-gray-900">19%</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">Muscle Mass</p>
                        <p className="font-medium text-gray-900">143 lbs</p>
                      </div>
                    </div>
                  </div>
                )}
                
                {/* Strength Metrics Chart */}
                {activeTab === 'strength' && (
                  <div>
                    <div className="mb-4">
                      <h2 className="text-lg font-medium text-gray-900">
                        {chartConfig.strengthMetrics.title}
                      </h2>
                      <p className="mt-1 text-sm text-gray-500">
                        {chartConfig.strengthMetrics.description}
                      </p>
                    </div>
                    
                    <div className="h-80">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart
                          data={strengthMetricsData}
                          margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                        >
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis 
                            dataKey="date" 
                            tickFormatter={(date) => {
                              return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                            }}
                          />
                          <YAxis />
                          <Tooltip 
                            formatter={(value, name) => [`${value} lbs`, name]}
                            labelFormatter={(date) => {
                              return new Date(date).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
                            }}
                          />
                          <Legend />
                          {chartConfig.strengthMetrics.metrics.map((metric) => (
                            <Line
                              key={metric.key}
                              type="monotone"
                              dataKey={metric.key}
                              name={metric.name}
                              stroke={metric.color}
                              activeDot={{ r: 8 }}
                            />
                          ))}
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                    
                    <div className="mt-6 pt-6 border-t border-gray-200 grid grid-cols-3 gap-4">
                      <div>
                        <p className="text-sm text-gray-500">Bench Press</p>
                        <p className="font-medium text-gray-900">215 lbs</p>
                        <p className="text-xs text-green-500">+30 lbs</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">Squat</p>
                        <p className="font-medium text-gray-900">285 lbs</p>
                        <p className="text-xs text-green-500">+60 lbs</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">Deadlift</p>
                        <p className="font-medium text-gray-900">325 lbs</p>
                        <p className="text-xs text-green-500">+50 lbs</p>
                      </div>
                    </div>
                  </div>
                )}
                
                {/* Workout Data Chart */}
                {activeTab === 'workouts' && (
                  <div>
                    <div className="mb-4">
                      <h2 className="text-lg font-medium text-gray-900">
                        Workout Activity
                      </h2>
                      <p className="mt-1 text-sm text-gray-500">
                        Track your workout frequency, duration, and intensity over time.
                      </p>
                    </div>
                    
                    <div className="h-80">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={workoutMetricsData}
                          margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                        >
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="week" />
                          <YAxis yAxisId="left" orientation="left" stroke="#3B82F6" />
                          <YAxis yAxisId="right" orientation="right" stroke="#10B981" />
                          <Tooltip />
                          <Legend />
                          <Bar 
                            yAxisId="left" 
                            dataKey="workoutCount" 
                            name="Workout Count" 
                            fill="#3B82F6" 
                          />
                          <Bar 
                            yAxisId="left" 
                            dataKey="totalMinutes" 
                            name="Total Minutes" 
                            fill="#10B981" 
                          />
                          <Bar 
                            yAxisId="right" 
                            dataKey="avgIntensity" 
                            name="Avg. Intensity (1-10)" 
                            fill="#F97316" 
                          />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                    
                    <div className="mt-6 pt-6 border-t border-gray-200 grid grid-cols-3 gap-4">
                      <div>
                        <p className="text-sm text-gray-500">Weekly Average</p>
                        <p className="font-medium text-gray-900">4.9 workouts</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">Avg. Duration</p>
                        <p className="font-medium text-gray-900">57 minutes</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">Avg. Intensity</p>
                        <p className="font-medium text-gray-900">7.8 / 10</p>
                      </div>
                    </div>
                  </div>
                )}
                
                {/* Nutrition Data Chart */}
                {activeTab === 'nutrition' && (
                  <div>
                    <div className="mb-4">
                      <h2 className="text-lg font-medium text-gray-900">
                        Nutrition Adherence
                      </h2>
                      <p className="mt-1 text-sm text-gray-500">
                        Monitor your adherence to calorie, protein, and water intake goals.
                      </p>
                    </div>
                    
                    <div className="h-80">
                      <ResponsiveContainer width="100%" height="100%">
                        <AreaChart
                          data={nutritionData}
                          margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                        >
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="week" />
                          <YAxis />
                          <Tooltip />
                          <Legend />
                          <Area 
                            type="monotone" 
                            dataKey="calorieAdherence" 
                            name="Calorie Adherence %" 
                            stroke="#F97316" 
                            fill="#FED7AA" 
                          />
                          <Area 
                            type="monotone" 
                            dataKey="proteinAdherence" 
                            name="Protein Adherence %" 
                            stroke="#10B981" 
                            fill="#A7F3D0" 
                          />
                          <Area 
                            type="monotone" 
                            dataKey="waterIntake" 
                            name="Water Intake %" 
                            stroke="#3B82F6" 
                            fill="#BFDBFE" 
                          />
                        </AreaChart>
                      </ResponsiveContainer>
                    </div>
                    
                    <div className="mt-6 pt-6 border-t border-gray-200 grid grid-cols-3 gap-4">
                      <div>
                        <p className="text-sm text-gray-500">Calorie Adherence</p>
                        <p className="font-medium text-gray-900">93%</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">Protein Adherence</p>
                        <p className="font-medium text-gray-900">98%</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">Water Intake</p>
                        <p className="font-medium text-gray-900">92%</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
            
            {/* AI Analysis */}
            <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg shadow p-6 text-white">
              <h2 className="text-lg font-medium mb-4 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 2a4 4 0 0 0-4 4v12a4 4 0 0 0 8 0V6a4 4 0 0 0-4-4z" />
                  <path d="M16 6h2a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2" />
                  <path d="M8 6H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2" />
                  <path d="M17 22h1a2 2 0 0 0 2-2v-1" />
                  <path d="M7 22H6a2 2 0 0 1-2-2v-1" />
                </svg>
                AI Progress Analysis
              </h2>
              
              <div className="space-y-4">
                <p className="text-white text-opacity-90">
                  Your weight loss is consistent and healthy, averaging 1.5 lbs per week. This indicates an appropriate caloric deficit without sacrificing muscle.
                </p>
                
                <p className="text-white text-opacity-90">
                  Your bench press progress has been excellent, but squat and deadlift are increasing at a faster rate. Consider adding an extra upper body day to maintain balance.
                </p>
                
                <p className="text-white text-opacity-90">
                  Based on your body composition changes, you're currently at an optimal protein intake level. Consider maintaining current levels rather than increasing further.
                </p>
              </div>
              
              <div className="mt-6 pt-6 border-t border-white border-opacity-20 flex justify-between items-center">
                <div>
                  <p className="text-white text-opacity-70">Goal Trajectory</p>
                  <p className="font-medium">On target for next milestone</p>
                </div>
                <button className="px-4 py-2 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-md text-sm font-medium transition-colors duration-200">
                  Update goals
                </button>
              </div>
            </div>
          </div>
          
          {/* Sidebar (right side) */}
          <div className="space-y-8">
            {/* Current measurements */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Current Measurements</h2>
              
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Current Weight</span>
                    <span className="text-sm font-medium text-blue-600">174 lbs</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: '65%' }}></div>
                  </div>
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Starting: 185 lbs</span>
                    <span>Goal: 165 lbs</span>
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Body Fat %</span>
                    <span className="text-sm font-medium text-green-600">19%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-green-600 h-2.5 rounded-full" style={{ width: '70%' }}></div>
                  </div>
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Starting: 22%</span>
                    <span>Goal: 15%</span>
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Muscle Mass</span>
                    <span className="text-sm font-medium text-purple-600">143 lbs</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-purple-600 h-2.5 rounded-full" style={{ width: '60%' }}></div>
                  </div>
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Starting: 140 lbs</span>
                    <span>Goal: 145 lbs</span>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 pt-4 border-t border-gray-200">
                <button className="flex items-center text-blue-600 text-sm font-medium hover:text-blue-500">
                  <Calendar className="h-4 w-4 mr-1" />
                  Log new measurements
                </button>
              </div>
            </div>
            
            {/* Recent achievements */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Recent Achievements</h2>
              
              <div className="space-y-4">
                {recentAchievements.map((achievement) => (
                  <div key={achievement.id} className="flex items-start">
                    <div className="flex-shrink-0">
                      <div className={`p-2 bg-${achievement.color}-100 rounded-full`}>
                        <Award className={`h-5 w-5 text-${achievement.color}-600`} />
                      </div>
                    </div>
                    <div className="ml-3">
                      <h3 className="text-sm font-medium text-gray-900">{achievement.title}</h3>
                      <p className="text-xs text-gray-500">{achievement.description}</p>
                      <p className="text-xs text-gray-400 mt-1">
                        {new Date(achievement.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="mt-6 pt-4 border-t border-gray-200">
                <button className="text-blue-600 text-sm font-medium hover:text-blue-500">
                  View all achievements
                </button>
              </div>
            </div>
            
            {/* Goals overview */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Your Goals</h2>
              
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Weight Loss</span>
                    <span className="text-sm font-medium text-blue-600">55% complete</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: '55%' }}></div>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    Goal: Lose 20 lbs (11/20 lbs lost)
                  </p>
                </div>
                
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Bench Press</span>
                    <span className="text-sm font-medium text-green-600">72% complete</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-green-600 h-2.5 rounded-full" style={{ width: '72%' }}></div>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    Goal: 225 lbs (215/225 lbs)
                  </p>
                </div>
                
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Body Fat %</span>
                    <span className="text-sm font-medium text-purple-600">43% complete</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-purple-600 h-2.5 rounded-full" style={{ width: '43%' }}></div>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    Goal: 15% (19% current, started at 22%)
                  </p>
                </div>
              </div>
              
              <div className="mt-6">
                <button className="block w-full text-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                  Add/Edit Goals
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProgressPage;