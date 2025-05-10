import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { 
  Menu, X, User, ChevronDown, Dumbbell, Apple, BarChart, Home, LogOut 
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsProfileOpen(false);
    setIsMenuOpen(false);
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
    if (isProfileOpen) setIsProfileOpen(false);
  };

  const toggleProfile = () => {
    setIsProfileOpen(!isProfileOpen);
  };

  return (
    <nav className="bg-white shadow-md z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
          <div className="flex-shrink-0 flex items-center">
          <Link to="/" className="flex items-center">
          <img
              src="./bbr_black.png"
              alt="Logo"
              className="h-15 w-20"
            />
    <span className="ml-2 text-xl font-bold text-gray-900">CNT</span>
  </Link>
</div>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              <Link to="/" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 border-b-2 border-transparent hover:border-blue-500">
                Home
              </Link>
              
              {isAuthenticated && (
                <>
                  <Link to="/dashboard" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 border-b-2 border-transparent hover:border-blue-500">
                    Dashboard
                  </Link>
                  <Link to="/training-plan" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 border-b-2 border-transparent hover:border-blue-500">
                    Training
                  </Link>
                  <Link to="/meal-plan" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 border-b-2 border-transparent hover:border-blue-500">
                    Meal Plans
                  </Link>
                  <Link to="/progress" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 border-b-2 border-transparent hover:border-blue-500">
                    Progress
                  </Link>
                </>
              )}
            </div>
          </div>
          
          {/* Auth buttons / User profile */}
          <div className="hidden sm:ml-6 sm:flex sm:items-center">
            {isAuthenticated ? (
              <div className="relative">
                <button
                  type="button"
                  className="flex items-center max-w-xs rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  id="user-menu-button"
                  onClick={toggleProfile}
                >
                  <span className="sr-only">Open user menu</span>
                  <div className="flex items-center">
                    <img
                      className="h-8 w-8 rounded-full object-cover"
                      src={user?.avatar || "https://source.unsplash.com/random/100x100/?portrait"}
                      alt={user?.name || "User"}
                    />
                    <span className="ml-2 text-gray-700">{user?.name}</span>
                    <ChevronDown size={16} className="ml-1 text-gray-400" />
                  </div>
                </button>
                
                {/* Profile dropdown */}
                <AnimatePresence>
                  {isProfileOpen && (
                    <motion.div
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.95 }}
                      transition={{ duration: 0.1 }}
                      className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
                      role="menu"
                      aria-orientation="vertical"
                      aria-labelledby="user-menu-button"
                    >
                      <Link to="/profile" className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                        <User size={16} className="mr-2" />Profile
                      </Link>
                      <button
                        onClick={handleLogout}
                        className="flex w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        <LogOut size={16} className="mr-2" />Sign out
                      </button>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ) : (
              <div className="flex items-center space-x-4">
                <Link
                  to="/login"
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-600 bg-white hover:bg-gray-50"
                >
                  Sign in
                </Link>
                <Link
                  to="/register"
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                >
                  Sign up
                </Link>
              </div>
            )}
          </div>
          
          {/* Mobile menu button */}
          <div className="flex items-center sm:hidden">
            <button
              type="button"
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
              aria-controls="mobile-menu"
              aria-expanded="false"
              onClick={toggleMenu}
            >
              <span className="sr-only">Open main menu</span>
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>
      
      {/* Mobile menu */}
      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="sm:hidden"
            id="mobile-menu"
          >
            <div className="pt-2 pb-3 space-y-1">
              <Link to="/" className="flex items-center text-base font-medium text-gray-900 hover:text-blue-600 hover:bg-gray-50 block px-3 py-2 rounded-md">
                <Home size={20} className="mr-2" />Home
              </Link>
              
              {isAuthenticated ? (
                <>
                  <Link to="/dashboard" className="flex items-center text-base font-medium text-gray-900 hover:text-blue-600 hover:bg-gray-50 block px-3 py-2 rounded-md">
                    <Home size={20} className="mr-2" />Dashboard
                  </Link>
                  <Link to="/training-plan" className="flex items-center text-base font-medium text-gray-900 hover:text-blue-600 hover:bg-gray-50 block px-3 py-2 rounded-md">
                    <Dumbbell size={20} className="mr-2" />Training
                  </Link>
                  <Link to="/meal-plan" className="flex items-center text-base font-medium text-gray-900 hover:text-blue-600 hover:bg-gray-50 block px-3 py-2 rounded-md">
                    <Apple size={20} className="mr-2" />Meal Plans
                  </Link>
                  <Link to="/progress" className="flex items-center text-base font-medium text-gray-900 hover:text-blue-600 hover:bg-gray-50 block px-3 py-2 rounded-md">
                    <BarChart size={20} className="mr-2" />Progress
                  </Link>
                  <Link to="/profile" className="flex items-center text-base font-medium text-gray-900 hover:text-blue-600 hover:bg-gray-50 block px-3 py-2 rounded-md">
                    <User size={20} className="mr-2" />Profile
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="flex w-full items-center text-base font-medium text-gray-900 hover:text-blue-600 hover:bg-gray-50 px-3 py-2 rounded-md"
                  >
                    <LogOut size={20} className="mr-2" />Sign out
                  </button>
                </>
              ) : (
                <div className="space-y-1 px-3 pt-2">
                  <Link
                    to="/login"
                    className="block w-full py-2 px-4 text-center font-medium text-blue-600 bg-gray-50 hover:bg-gray-100 rounded-md"
                  >
                    Sign in
                  </Link>
                  <Link
                    to="/register"
                    className="block w-full py-2 px-4 text-center font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md mt-2"
                  >
                    Sign up
                  </Link>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

export default Navbar;