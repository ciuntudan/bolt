import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, CheckCircle, Dumbbell, Apple, Brain, BarChart } from 'lucide-react';

const HomePage: React.FC = () => {
  return (
    <div className="bg-white">
      {/* Hero section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 opacity-10"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="relative pt-16 pb-20 md:pt-24 md:pb-28 lg:pt-32 lg:pb-36">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-center"
            >
              <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
                <span className="block text-blue-600">CNT</span>
                <span className="block">Champion Nutrition & Training</span>
                <span className="block text-blue-600">With AI-Powered Plans</span>
              </h1>
              <p className="mt-6 max-w-lg mx-auto text-xl text-gray-500 sm:max-w-3xl">
                Personalized workout routines and meal plans created by artificial intelligence to help you reach your fitness goals easier & faster.
              </p>
              <div className="mt-10 max-w-sm mx-auto sm:max-w-none sm:flex sm:justify-center">
                <div className="space-y-4 sm:space-y-0 sm:mx-auto sm:inline-grid sm:grid-cols-2 sm:gap-5">
                  <Link
                    to="/register"
                    className="flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10"
                  >
                    Get Started
                  </Link>
                  <Link
                    to="/login"
                    className="flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-blue-600 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10"
                  >
                    Sign In
                  </Link>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>

      {/* Features section */}
      <div className="bg-gray-50 py-16 sm:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
              AI-Powered Fitness Revolution
            </h2>
            <p className="mt-4 max-w-2xl mx-auto text-xl text-gray-500">
              Our platform uses cutting-edge AI technology to create personalized plans that adapt to your progress.
            </p>
          </div>

          <div className="mt-16">
            <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
              {/* Feature 1 */}
              <motion.div 
                whileHover={{ y: -8 }}
                className="bg-white overflow-hidden shadow rounded-lg"
              >
                <div className="px-6 py-8">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
                      <Dumbbell className="h-6 w-6 text-white" />
                    </div>
                    <h3 className="ml-4 text-xl font-medium text-gray-900">AI Training Plans</h3>
                  </div>
                  <p className="mt-5 text-base text-gray-500">
                    Custom workout plans tailored to your fitness level, goals and available equipment, with smart progression.
                  </p>
                  <div className="mt-6">
                    <Link to="/register" className="flex items-center text-blue-600 hover:text-blue-500">
                      Get started <ArrowRight size={16} className="ml-1" />
                    </Link>
                  </div>
                </div>
              </motion.div>

              {/* Feature 2 */}
              <motion.div 
                whileHover={{ y: -8 }}
                className="bg-white overflow-hidden shadow rounded-lg"
              >
                <div className="px-6 py-8">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
                      <Apple className="h-6 w-6 text-white" />
                    </div>
                    <h3 className="ml-4 text-xl font-medium text-gray-900">Meal Planning</h3>
                  </div>
                  <p className="mt-5 text-base text-gray-500">
                    Nutritionally balanced meal plans that match your dietary preferences and support your fitness goals.
                  </p>
                  <div className="mt-6">
                    <Link to="/register" className="flex items-center text-green-600 hover:text-green-500">
                      Explore plans <ArrowRight size={16} className="ml-1" />
                    </Link>
                  </div>
                </div>
              </motion.div>

              {/* Feature 3 */}
              <motion.div 
                whileHover={{ y: -8 }}
                className="bg-white overflow-hidden shadow rounded-lg"
              >
                <div className="px-6 py-8">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-purple-500 rounded-md p-3">
                      <BarChart className="h-6 w-6 text-white" />
                    </div>
                    <h3 className="ml-4 text-xl font-medium text-gray-900">Progress Tracking</h3>
                  </div>
                  <p className="mt-5 text-base text-gray-500">
                    Visual analytics to track your progress, set milestones, and celebrate achievements along your journey.
                  </p>
                  <div className="mt-6">
                    <Link to="/register" className="flex items-center text-purple-600 hover:text-purple-500">
                      Track progress <ArrowRight size={16} className="ml-1" />
                    </Link>
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </div>
      </div>

      {/* How it works section */}
      <div className="bg-white py-16 sm:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
              How CNT Works
            </h2>
            <p className="mt-4 max-w-2xl mx-auto text-xl text-gray-500">
              Our simple process helps you get started in minutes.
            </p>
          </div>

          <div className="mt-16">
            <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
              {/* Step 1 */}
              <div className="text-center">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white mx-auto">
                  <span className="text-lg font-bold">1</span>
                </div>
                <h3 className="mt-6 text-lg font-medium text-gray-900">Create an account</h3>
                <p className="mt-2 text-base text-gray-500">
                  Sign up in seconds and set up your profile with basic information.
                </p>
              </div>

              {/* Step 2 */}
              <div className="text-center">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white mx-auto">
                  <span className="text-lg font-bold">2</span>
                </div>
                <h3 className="mt-6 text-lg font-medium text-gray-900">Define your goals</h3>
                <p className="mt-2 text-base text-gray-500">
                  Tell us what you want to achieve and your current fitness level.
                </p>
              </div>

              {/* Step 3 */}
              <div className="text-center">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white mx-auto">
                  <span className="text-lg font-bold">3</span>
                </div>
                <h3 className="mt-6 text-lg font-medium text-gray-900">Get your AI plans</h3>
                <p className="mt-2 text-base text-gray-500">
                  Our AI generates custom workout and meal plans just for you.
                </p>
              </div>

              {/* Step 4 */}
              <div className="text-center">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white mx-auto">
                  <span className="text-lg font-bold">4</span>
                </div>
                <h3 className="mt-6 text-lg font-medium text-gray-900">Track your progress</h3>
                <p className="mt-2 text-base text-gray-500">
                  Follow your plans and watch your results improve over time.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Testimonials */}
      <div className="bg-gray-50 py-16 sm:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
              What Our Users Say
            </h2>
          </div>

          <div className="mt-16 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            {/* Testimonial 1 */}
            <motion.div 
              whileHover={{ scale: 1.03 }}
              className="bg-white rounded-lg shadow-lg overflow-hidden"
            >
              <div className="px-6 py-8">
                <div className="flex items-center mb-4">
                  <div className="h-10 w-10 rounded-full overflow-hidden bg-gray-200">
                    <img 
                      src="https://source.unsplash.com/random/100x100/?portrait&1" 
                      alt="User avatar" 
                      className="h-full w-full object-cover"
                    />
                  </div>
                  <div className="ml-3">
                    <h3 className="text-lg font-medium text-gray-900">Sarah K.</h3>
                    <p className="text-sm text-gray-500">Lost 15 kgs in 3 months</p>
                  </div>
                </div>
                <p className="text-gray-600 italic">
                  "The AI-generated meal plans were a game changer for me. I've tried many apps before, but this one actually adapts to my progress and preferences."
                </p>
              </div>
            </motion.div>

            {/* Testimonial 2 */}
            <motion.div 
              whileHover={{ scale: 1.03 }}
              className="bg-white rounded-lg shadow-lg overflow-hidden"
            >
              <div className="px-6 py-8">
                <div className="flex items-center mb-4">
                  <div className="h-10 w-10 rounded-full overflow-hidden bg-gray-200">
                    <img 
                      src="https://source.unsplash.com/random/100x100/?portrait&2" 
                      alt="User avatar" 
                      className="h-full w-full object-cover"
                    />
                  </div>
                  <div className="ml-3">
                    <h3 className="text-lg font-medium text-gray-900">Michael T.</h3>
                    <p className="text-sm text-gray-500">Gained 10 kgs of muscle</p>
                  </div>
                </div>
                <p className="text-gray-600 italic">
                  "The workout plans are excellent. As I progress, the AI adjusts the intensity and introduces new exercises to keep challenging me."
                </p>
              </div>
            </motion.div>

            {/* Testimonial 3 */}
            <motion.div 
              whileHover={{ scale: 1.03 }}
              className="bg-white rounded-lg shadow-lg overflow-hidden"
            >
              <div className="px-6 py-8">
                <div className="flex items-center mb-4">
                  <div className="h-10 w-10 rounded-full overflow-hidden bg-gray-200">
                    <img 
                      src="https://source.unsplash.com/random/100x100/?portrait&3" 
                      alt="User avatar" 
                      className="h-full w-full object-cover"
                    />
                  </div>
                  <div className="ml-3">
                    <h3 className="text-lg font-medium text-gray-900">Lisa J.</h3>
                    <p className="text-sm text-gray-500">Improved marathon time</p>
                  </div>
                </div>
                <p className="text-gray-600 italic">
                  "I love the progress tracking feature. Seeing the charts and achievements keeps me motivated to stick with my training plan."
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="bg-blue-600">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between">
          <h2 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            <span className="block">Ready to transform your fitness?</span>
            <span className="block text-blue-200">Start your journey today.</span>
          </h2>
          <div className="mt-8 flex lg:mt-0 lg:flex-shrink-0">
            <div className="inline-flex rounded-md shadow">
              <Link
                to="/register"
                className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-blue-600 bg-white hover:bg-blue-50"
              >
                Get started
              </Link>
            </div>
            <div className="ml-3 inline-flex rounded-md shadow">
              <Link
                to="#features"
                className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-800 hover:bg-blue-700"
              >
                Learn more
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;