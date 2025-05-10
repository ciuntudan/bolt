import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Apple, ChevronRight, ChevronDown, ChevronUp, 
  Calendar, Plus, Minus, RefreshCw, Filter, PenSquare, Utensils
} from 'lucide-react';

// Sample meal plan data
const DAILY_MEALS = [
  {
    day: 'Monday',
    meals: [
      {
        type: 'Breakfast',
        time: '7:30 AM',
        title: 'High Protein Oatmeal',
        description: 'Rolled oats with protein powder, berries, and nuts',
        ingredients: [
          { name: 'Rolled oats', amount: '50 g', calories: 150, protein: 5 },
          { name: 'Whey protein', amount: '1 scoop', calories: 120, protein: 24 },
          { name: 'Mixed berries', amount: '50 g', calories: 40, protein: 0.5 },
          { name: 'Almonds', amount: '30 g', calories: 60, protein: 2 },
          { name: 'Cinnamon', amount: '5 g', calories: 0, protein: 0 },
          { name: 'Almond milk', amount: '100 ml', calories: 15, protein: 0.5 }
        ],
        nutrition: {
          calories: 385,
          protein: 32,
          carbs: 40,
          fat: 12
        },
        image: 'https://source.unsplash.com/K1ATc-tjf8U/800x600'
      },
      {
        type: 'Snack',
        time: '10:30 AM',
        title: 'Greek Yogurt Parfait',
        description: 'Greek yogurt with honey and granola',
        ingredients: [
          { name: 'Greek yogurt', amount: '100 g', calories: 130, protein: 22 },
          { name: 'Honey', amount: '20 g', calories: 64, protein: 0 },
          { name: 'Granola', amount: '30 g', calories: 120, protein: 3 }
        ],
        nutrition: {
          calories: 314,
          protein: 25,
          carbs: 40,
          fat: 8
        },
        image: 'https://source.unsplash.com/qvIrI4ueqzY/800x600'
      },
      {
        type: 'Lunch',
        time: '1:00 PM',
        title: 'Grilled Chicken Salad',
        description: 'Grilled chicken breast with mixed greens and vinaigrette',
        ingredients: [
          { name: 'Chicken breast', amount: '80g', calories: 180, protein: 36 },
          { name: 'Mixed greens', amount: '30 g', calories: 15, protein: 1 },
          { name: 'Cherry tomatoes', amount: '50 g', calories: 20, protein: 1 },
          { name: 'Cucumber', amount: '50 g', calories: 8, protein: 0.5 },
          { name: 'Olive oil', amount: '20 ml', calories: 120, protein: 0 },
          { name: 'Balsamic vinegar', amount: '10 ml', calories: 14, protein: 0 }
        ],
        nutrition: {
          calories: 357,
          protein: 38.5,
          carbs: 10,
          fat: 16
        },
        image: 'https://source.unsplash.com/IGfIGP5ONV0/800x600'
      },
      {
        type: 'Snack',
        time: '4:00 PM',
        title: 'Protein Shake with Banana',
        description: 'Whey protein shake with a banana',
        ingredients: [
          { name: 'Whey protein', amount: '1 scoop', calories: 120, protein: 24 },
          { name: 'Banana', amount: '1 medium', calories: 105, protein: 1.3 },
          { name: 'Water', amount: '200 ml', calories: 0, protein: 0 }
        ],
        nutrition: {
          calories: 225,
          protein: 25.3,
          carbs: 27,
          fat: 1
        },
        image: 'https://source.unsplash.com/F1-UvxPkJDU/800x600'
      },
      {
        type: 'Dinner',
        time: '7:00 PM',
        title: 'Salmon with Quinoa and Veggies',
        description: 'Baked salmon with quinoa and roasted vegetables',
        ingredients: [
          { name: 'Salmon fillet', amount: '100 g', calories: 250, protein: 36 },
          { name: 'Quinoa', amount: '50 g', calories: 110, protein: 4 },
          { name: 'Brussels sprouts', amount: '30 g', calories: 60, protein: 4 },
          { name: 'Bell pepper', amount: '30 g', calories: 25, protein: 1 },
          { name: 'Olive oil', amount: '30 ml', calories: 120, protein: 0 },
          { name: 'Lemon juice', amount: '10 ml', calories: 4, protein: 0 }
        ],
        nutrition: {
          calories: 569,
          protein: 45,
          carbs: 35,
          fat: 24
        },
        image: 'https://source.unsplash.com/YnPNEFC4Rn0/800x600'
      }
    ],
    totals: {
      calories: 1850,
      protein: 165.8,
      carbs: 152,
      fat: 61
    }
  },
  {
    day: 'Tuesday',
    meals: [
      {
        type: 'Breakfast',
        time: '7:30 AM',
        title: 'Spinach and Egg White Omelet',
        description: 'Egg white omelet with spinach, feta cheese, and whole grain toast',
        ingredients: [
          { name: 'Egg whites', amount: '30 g', calories: 125, protein: 26 },
          { name: 'Spinach', amount: '30 g', calories: 7, protein: 0.9 },
          { name: 'Feta cheese', amount: '70 g', calories: 74, protein: 4 },
          { name: 'Whole grain toast', amount: '25 g', calories: 80, protein: 4 },
          { name: 'Olive oil spray', amount: '1 spray', calories: 5, protein: 0 }
        ],
        nutrition: {
          calories: 291,
          protein: 34.9,
          carbs: 15,
          fat: 10
        },
        image: 'https://source.unsplash.com/Wl5rExgPrGw/800x600'
      }
      // Additional meals would be added here
    ],
    totals: {
      calories: 1800,
      protein: 160,
      carbs: 150,
      fat: 60
    }
  }
  // Additional days would be added here
];

// Dietary preferences options
const DIETARY_PREFERENCES = [
  'Vegetarian',
  'Vegan',
  'Gluten-Free',
  'Dairy-Free',
  'Keto',
  'Paleo',
  'Low Carb',
  'High Protein'
];

// Calorie adjustment options
const CALORIE_ADJUSTMENTS = [
  { value: -500, label: 'Weight Loss (Aggressive)' },
  { value: -300, label: 'Weight Loss (Moderate)' },
  { value: -100, label: 'Weight Loss (Slow)' },
  { value: 0, label: 'Maintenance' },
  { value: 200, label: 'Muscle Gain (Lean)' },
  { value: 400, label: 'Muscle Gain (Moderate)' },
  { value: 600, label: 'Muscle Gain (Aggressive)' }
];

const MealPlanPage: React.FC = () => {
  const [expandedDay, setExpandedDay] = useState('Monday');
  const [selectedMeal, setSelectedMeal] = useState<any>(null);
  const [showFilters, setShowFilters] = useState(false);
  const [selectedPreferences, setSelectedPreferences] = useState<string[]>(['High Protein']);
  const [calorieAdjustment, setCalorieAdjustment] = useState(0);
  
  const toggleDay = (day: string) => {
    setExpandedDay(expandedDay === day ? '' : day);
  };
  
  const openMealDetail = (meal: any) => {
    setSelectedMeal(meal);
  };
  
  const closeMealDetail = () => {
    setSelectedMeal(null);
  };
  
  const togglePreference = (preference: string) => {
    if (selectedPreferences.includes(preference)) {
      setSelectedPreferences(selectedPreferences.filter(p => p !== preference));
    } else {
      setSelectedPreferences([...selectedPreferences, preference]);
    }
  };
  
  const regenerateMealPlan = () => {
    // This would typically call an API to get a new meal plan
    alert('Regenerating meal plan based on your preferences...');
  };

  return (
    <div className="bg-gray-50 pt-8 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Your Meal Plan</h1>
          <p className="mt-2 text-gray-600">
            AI-powered nutrition tailored to your goals, preferences, and training schedule.
          </p>
        </div>

        {/* Main content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Meal plan (left side) */}
          <div className="lg:col-span-2">
            {/* Controls */}
            <div className="bg-white rounded-lg shadow mb-6 p-4">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div className="flex items-center">
                  <Calendar className="mr-2 h-5 w-5 text-gray-500" />
                  <h2 className="text-lg font-medium text-gray-900">Week of June 10, 2025</h2>
                </div>
                
                <div className="flex space-x-3">
                  <button
                    onClick={() => setShowFilters(!showFilters)}
                    className="flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                  >
                    <Filter className="mr-2 h-4 w-4" />
                    Filters
                  </button>
                  
                  <button
                    onClick={regenerateMealPlan}
                    className="flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                  >
                    <RefreshCw className="mr-2 h-4 w-4" />
                    Regenerate Plan
                  </button>
                </div>
              </div>
              
              {/* Filters */}
              <motion.div
                initial={false}
                animate={{ height: showFilters ? 'auto' : 0, opacity: showFilters ? 1 : 0 }}
                transition={{ duration: 0.3 }}
                className="overflow-hidden"
              >
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h3 className="text-sm font-medium text-gray-900 mb-3">Dietary Preferences</h3>
                      <div className="flex flex-wrap gap-2">
                        {DIETARY_PREFERENCES.map(preference => (
                          <button
                            key={preference}
                            onClick={() => togglePreference(preference)}
                            className={`px-3 py-1 rounded-full text-xs font-medium ${
                              selectedPreferences.includes(preference)
                                ? 'bg-blue-100 text-blue-800'
                                : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                            }`}
                          >
                            {preference}
                          </button>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <h3 className="text-sm font-medium text-gray-900 mb-3">Calorie Adjustment</h3>
                      <select
                        value={calorieAdjustment}
                        onChange={(e) => setCalorieAdjustment(Number(e.target.value))}
                        className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                      >
                        {CALORIE_ADJUSTMENTS.map(option => (
                          <option key={option.value} value={option.value}>
                            {option.label} ({option.value > 0 ? '+' : ''}{option.value} calories)
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>
                  
                  <div className="mt-4 text-right">
                    <button
                      onClick={regenerateMealPlan}
                      className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                    >
                      Apply Changes
                    </button>
                  </div>
                </div>
              </motion.div>
            </div>
            
            {/* Daily meal plans */}
            <div className="bg-white rounded-lg shadow overflow-hidden">
              {DAILY_MEALS.map((dayPlan) => (
                <div key={dayPlan.day} className="border-b border-gray-200 last:border-b-0">
                  <button
                    className="w-full px-6 py-4 flex items-center justify-between text-left"
                    onClick={() => toggleDay(dayPlan.day)}
                  >
                    <div className="flex items-center">
                      <Apple className="h-5 w-5 text-green-500 mr-2" />
                      <span className="font-medium text-gray-900">{dayPlan.day}</span>
                    </div>
                    <div className="flex items-center">
                      <div className="mr-4 text-sm text-gray-500">
                        {dayPlan.totals.calories} kcal | {dayPlan.totals.protein}g protein
                      </div>
                      {expandedDay === dayPlan.day ? (
                        <ChevronUp className="h-5 w-5 text-gray-500" />
                      ) : (
                        <ChevronDown className="h-5 w-5 text-gray-500" />
                      )}
                    </div>
                  </button>
                  
                  {expandedDay === dayPlan.day && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.3 }}
                      className="px-6 pb-4"
                    >
                      <div className="space-y-4">
                        {dayPlan.meals.map((meal, index) => (
                          <div 
                            key={index}
                            className="bg-gray-50 rounded-lg overflow-hidden border border-gray-200 hover:border-blue-200 cursor-pointer transition-all duration-200"
                            onClick={() => openMealDetail(meal)}
                          >
                            <div className="p-4">
                              <div className="flex justify-between items-start">
                                <div>
                                  <div className="flex items-center text-sm text-gray-500 mb-1">
                                    <Utensils className="h-4 w-4 mr-1" /> 
                                    {meal.type} • {meal.time}
                                  </div>
                                  <h3 className="text-lg font-medium text-gray-900">{meal.title}</h3>
                                  <p className="mt-1 text-sm text-gray-600">{meal.description}</p>
                                </div>
                                
                                <div className="ml-4 flex-shrink-0">
                                  <img
                                    src={meal.image}
                                    alt={meal.title}
                                    className="h-16 w-16 rounded-md object-cover"
                                  />
                                </div>
                              </div>
                              
                              <div className="mt-3 flex items-center text-xs">
                                <span className="px-2 py-1 rounded-full bg-blue-100 text-blue-800">
                                  {meal.nutrition.calories} kcal
                                </span>
                                <span className="ml-2 px-2 py-1 rounded-full bg-green-100 text-green-800">
                                  {meal.nutrition.protein}g protein
                                </span>
                                <span className="ml-2 px-2 py-1 rounded-full bg-yellow-100 text-yellow-800">
                                  {meal.nutrition.carbs}g carbs
                                </span>
                                <span className="ml-2 px-2 py-1 rounded-full bg-red-100 text-red-800">
                                  {meal.nutrition.fat}g fat
                                </span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                      
                      <div className="mt-6 pt-4 border-t border-gray-200 flex justify-between items-center">
                        <div>
                          <div className="flex items-center gap-3 text-sm">
                            <span className="px-2 py-1 rounded-full bg-blue-100 text-blue-800">
                              {dayPlan.totals.calories} kcal
                            </span>
                            <span className="px-2 py-1 rounded-full bg-green-100 text-green-800">
                              {dayPlan.totals.protein}g protein
                            </span>
                            <span className="px-2 py-1 rounded-full bg-yellow-100 text-yellow-800">
                              {dayPlan.totals.carbs}g carbs
                            </span>
                            <span className="px-2 py-1 rounded-full bg-red-100 text-red-800">
                              {dayPlan.totals.fat}g fat
                            </span>
                          </div>
                        </div>
                        
                        <button className="text-blue-600 text-sm font-medium hover:text-blue-500 flex items-center">
                          <PenSquare className="h-4 w-4 mr-1" />
                          Edit day
                        </button>
                      </div>
                    </motion.div>
                  )}
                </div>
              ))}
            </div>
          </div>
          
          {/* Sidebar (right side) */}
          <div className="space-y-8">
            {/* Nutrition summary */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Weekly Nutrition Summary</h2>
              
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Daily Average Calories</span>
                    <span className="text-sm font-medium text-blue-600">1825 kcal</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: '85%' }}></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Protein Goal</span>
                    <span className="text-sm font-medium text-green-600">163g / 160g</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-green-600 h-2.5 rounded-full" style={{ width: '102%' }}></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Carbohydrates</span>
                    <span className="text-sm font-medium text-yellow-600">151g / 175g</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-yellow-600 h-2.5 rounded-full" style={{ width: '86%' }}></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Fats</span>
                    <span className="text-sm font-medium text-red-600">60.5g / 65g</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div className="bg-red-600 h-2.5 rounded-full" style={{ width: '93%' }}></div>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 pt-4 border-t border-gray-200">
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Protein ratio</p>
                    <p className="font-medium text-gray-900">36%</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Carb/fat ratio</p>
                    <p className="font-medium text-gray-900">2.5:1</p>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Shopping list */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Shopping List</h2>
              
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <input
                      id="check-chicken"
                      name="check-chicken"
                      type="checkbox"
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label htmlFor="check-chicken" className="ml-2 block text-sm text-gray-900">
                      Chicken breast (2 lbs)
                    </label>
                  </div>
                  <span className="text-gray-500 text-xs">$12.99</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <input
                      id="check-eggs"
                      name="check-eggs"
                      type="checkbox"
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label htmlFor="check-eggs" className="ml-2 block text-sm text-gray-900">
                      Eggs (18 count)
                    </label>
                  </div>
                  <span className="text-gray-500 text-xs">$4.99</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <input
                      id="check-greek"
                      name="check-greek"
                      type="checkbox"
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label htmlFor="check-greek" className="ml-2 block text-sm text-gray-900">
                      Greek yogurt (32 oz)
                    </label>
                  </div>
                  <span className="text-gray-500 text-xs">$5.49</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <input
                      id="check-oats"
                      name="check-oats"
                      type="checkbox"
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label htmlFor="check-oats" className="ml-2 block text-sm text-gray-900">
                      Rolled oats (24 oz)
                    </label>
                  </div>
                  <span className="text-gray-500 text-xs">$3.99</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <input
                      id="check-salmon"
                      name="check-salmon"
                      type="checkbox"
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label htmlFor="check-salmon" className="ml-2 block text-sm text-gray-900">
                      Salmon fillets (1 lb)
                    </label>
                  </div>
                  <span className="text-gray-500 text-xs">$12.99</span>
                </div>
              </div>
              
              <div className="mt-6 pt-4 border-t border-gray-200">
                <button className="text-blue-600 text-sm font-medium hover:text-blue-500">
                  View complete shopping list
                </button>
              </div>
            </div>
            
            {/* AI recommendations */}
            <div className="bg-gradient-to-br from-green-500 to-teal-600 rounded-lg shadow p-6 text-white">
              <h2 className="text-lg font-medium mb-4 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 2a4 4 0 0 0-4 4v12a4 4 0 0 0 8 0V6a4 4 0 0 0-4-4z" />
                  <path d="M16 6h2a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2" />
                  <path d="M8 6H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2" />
                  <path d="M17 22h1a2 2 0 0 0 2-2v-1" />
                  <path d="M7 22H6a2 2 0 0 1-2-2v-1" />
                </svg>
                AI Nutrition Insights
              </h2>
              
              <div className="space-y-4">
                <p className="text-white text-opacity-90">
                  Your post-workout meals could benefit from an additional 15g of carbs to maximize recovery.
                </p>
                
                <p className="text-white text-opacity-90">
                  Consider adding more leafy greens to increase your micronutrient intake, especially calcium and iron.
                </p>
                
                <p className="text-white text-opacity-90">
                  Drinking an additional 16oz of water with each meal will help with nutrient absorption and hydration.
                </p>
              </div>
              
              <button className="mt-6 w-full bg-white bg-opacity-20 hover:bg-opacity-30 text-white py-2 px-4 rounded-md text-sm font-medium transition-colors duration-200">
                Get personalized advice
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Meal detail modal */}
      {selectedMeal && (
        <div className="fixed inset-0 overflow-y-auto z-50">
          <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity" aria-hidden="true">
              <div className="absolute inset-0 bg-gray-500 opacity-75" onClick={closeMealDetail}></div>
            </div>
            
            <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
              className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
            >
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <div className="sm:flex sm:items-start">
                  <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="text-lg leading-6 font-medium text-gray-900">{selectedMeal.title}</h3>
                        <p className="mt-1 text-sm text-gray-500">
                          {selectedMeal.type} • {selectedMeal.time}
                        </p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="px-2 py-1 rounded-full bg-blue-100 text-blue-800 text-xs">
                          {selectedMeal.nutrition.calories} kcal
                        </span>
                      </div>
                    </div>
                    
                    <div className="mt-4">
                      <img
                        src={selectedMeal.image}
                        alt={selectedMeal.title}
                        className="w-full h-48 object-cover rounded-lg"
                      />
                    </div>
                    
                    <div className="mt-4">
                      <h4 className="text-sm font-medium text-gray-900">Description</h4>
                      <p className="mt-1 text-sm text-gray-500">{selectedMeal.description}</p>
                    </div>
                    
                    <div className="mt-4">
                      <h4 className="text-sm font-medium text-gray-900">Ingredients</h4>
                      <ul className="mt-2 divide-y divide-gray-200">
                        {selectedMeal.ingredients.map((ingredient: any, index: number) => (
                          <li key={index} className="py-2 flex justify-between">
                            <div className="text-sm text-gray-900">
                              {ingredient.name} ({ingredient.amount})
                            </div>
                            <div className="text-sm text-gray-500">
                              {ingredient.calories} kcal • {ingredient.protein}g protein
                            </div>
                          </li>
                        ))}
                      </ul>
                    </div>
                    
                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <h4 className="text-sm font-medium text-gray-900">Nutrition Information</h4>
                      <div className="mt-2 grid grid-cols-4 gap-2">
                        <div className="text-center p-2 bg-blue-50 rounded-lg">
                          <div className="text-xs text-gray-500">Calories</div>
                          <div className="font-medium text-gray-900">{selectedMeal.nutrition.calories}</div>
                        </div>
                        <div className="text-center p-2 bg-green-50 rounded-lg">
                          <div className="text-xs text-gray-500">Protein</div>
                          <div className="font-medium text-gray-900">{selectedMeal.nutrition.protein}g</div>
                        </div>
                        <div className="text-center p-2 bg-yellow-50 rounded-lg">
                          <div className="text-xs text-gray-500">Carbs</div>
                          <div className="font-medium text-gray-900">{selectedMeal.nutrition.carbs}g</div>
                        </div>
                        <div className="text-center p-2 bg-red-50 rounded-lg">
                          <div className="text-xs text-gray-500">Fats</div>
                          <div className="font-medium text-gray-900">{selectedMeal.nutrition.fat}g</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                <button
                  type="button"
                  onClick={closeMealDetail}
                  className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm"
                >
                  Close
                </button>
                <button
                  type="button"
                  className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                >
                  Mark as eaten
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MealPlanPage;