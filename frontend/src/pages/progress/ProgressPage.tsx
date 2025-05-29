import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  LineChart, Line, AreaChart, Area, BarChart, Bar, 
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { 
  Calendar, ChevronLeft, ChevronRight, 
  TrendingUp, Zap, Award, Target, BarChart2,
  Loader2
} from 'lucide-react';
import { useProgress } from '../../hooks/useProgress';

// Chart config
const chartConfig = {
  bodyMetrics: {
    title: 'Body Composition',
    description: 'Track changes in weight, body fat percentage, and muscle mass over time.',
    metrics: [
      { key: 'weight', name: 'Weight (kgs)', color: '#3B82F6' },
      { key: 'body_fat', name: 'Body Fat %', color: '#F97316' },
      { key: 'muscle_mass', name: 'Muscle Mass (kgs)', color: '#10B981' }
    ]
  },
  strengthMetrics: {
    title: 'Strength Progression',
    description: 'Monitor your progress on key compound lifts over time.',
    metrics: [
      { key: 'bench_press', name: 'Bench Press (kgs)', color: '#8B5CF6' },
      { key: 'squat', name: 'Squat (kgs)', color: '#EC4899' },
      { key: 'deadlift', name: 'Deadlift (kgs)', color: '#F59E0B' }
    ]
  }
};

const ProgressPage: React.FC = () => {
  const [timeRange, setTimeRange] = useState('7W');
  const [activeTab, setActiveTab] = useState('body');
  const { data, loading, error } = useProgress(timeRange);
  
  const handleTimeRangeChange = (range: string) => {
    setTimeRange(range);
  };

  // Calculate weight change
  const calculateWeightChange = () => {
    if (!data?.body_metrics || data.body_metrics.length < 2) return { change: 0, percentage: 0 };
    
    const first = data.body_metrics[0];
    const last = data.body_metrics[data.body_metrics.length - 1];
    const change = last.weight - first.weight;
    const percentage = (change / first.weight) * 100;
    
    return { change, percentage };
  };

  // Format date for display
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    });
  };

  // Check if data exists and has metrics
  const hasData = data && (
    (data.body_metrics && data.body_metrics.length > 0) ||
    (data.strength_metrics && data.strength_metrics.length > 0) ||
    (data.achievements && data.achievements.length > 0)
  );
  
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
          </div>
        </div>

        {loading ? (
          <div className="flex justify-center items-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
          </div>
        ) : error ? (
          <div className="text-center text-red-600 py-12">
            {error}
          </div>
        ) : !hasData ? (
          <div className="text-center text-gray-500 py-12">
            <p className="text-lg font-medium">No progress data available</p>
            <p className="mt-2">Start logging your workouts and measurements to see your progress here.</p>
          </div>
        ) : (
          <>
            {/* Metrics summary cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              {data.body_metrics && data.body_metrics.length > 0 && (
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
                        <p className="text-2xl font-bold text-gray-900">
                          {calculateWeightChange().change.toFixed(1)} kg
                        </p>
                        <span className={`ml-2 ${calculateWeightChange().change < 0 ? 'text-green-500' : 'text-red-500'} text-sm`}>
                          {calculateWeightChange().percentage.toFixed(1)}%
                        </span>
                      </div>
                      <p className="text-xs text-gray-500">Since {formatDate(data.body_metrics[0].date)}</p>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Body Composition Chart */}
              {data.body_metrics && data.body_metrics.length > 0 && (
                <div className="col-span-full bg-white rounded-lg shadow p-6">
                  <div className="mb-6">
                    <h2 className="text-lg font-medium text-gray-900">{chartConfig.bodyMetrics.title}</h2>
                    <p className="text-sm text-gray-500">{chartConfig.bodyMetrics.description}</p>
                  </div>
                  <div className="h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={data.body_metrics}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis 
                          dataKey="date" 
                          tickFormatter={formatDate}
                        />
                        <YAxis />
                        <Tooltip 
                          labelFormatter={formatDate}
                          formatter={(value: number) => [value.toFixed(1), '']}
                        />
                        <Legend />
                        {chartConfig.bodyMetrics.metrics.map(metric => (
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
                </div>
              )}

              {/* Strength Progress Chart */}
              {data.strength_metrics && data.strength_metrics.length > 0 && (
                <div className="col-span-full bg-white rounded-lg shadow p-6">
                  <div className="mb-6">
                    <h2 className="text-lg font-medium text-gray-900">{chartConfig.strengthMetrics.title}</h2>
                    <p className="text-sm text-gray-500">{chartConfig.strengthMetrics.description}</p>
                  </div>
                  <div className="h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={data.strength_metrics}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis 
                          dataKey="date" 
                          tickFormatter={formatDate}
                        />
                        <YAxis />
                        <Tooltip 
                          labelFormatter={formatDate}
                          formatter={(value: number) => [`${value} kg`, '']}
                        />
                        <Legend />
                        {chartConfig.strengthMetrics.metrics.map(metric => (
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
                </div>
              )}

              {/* Recent Achievements */}
              {data.achievements && data.achievements.length > 0 && (
                <div className="col-span-full lg:col-span-4 bg-white rounded-lg shadow p-6">
                  <h2 className="text-lg font-medium text-gray-900 mb-6">Recent Achievements</h2>
                  <div className="space-y-4">
                    {data.achievements.map((achievement, index) => (
                      <div key={index} className="flex items-start space-x-3">
                        <div className={`p-2 rounded-lg bg-${achievement.color}-100`}>
                          <Award className={`w-5 h-5 text-${achievement.color}-600`} />
                        </div>
                        <div>
                          <h3 className="text-sm font-medium text-gray-900">{achievement.title}</h3>
                          <p className="text-sm text-gray-500">{achievement.description}</p>
                          <p className="text-xs text-gray-400 mt-1">{formatDate(achievement.date)}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ProgressPage;