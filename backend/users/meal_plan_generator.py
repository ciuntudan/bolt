from typing import List, Dict, Any
import random
from datetime import datetime, timedelta
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

class MealPlanGenerator:
    def __init__(self):
        # Initialize ML models and scaler
        self.calorie_model = None
        self.macro_model = None
        self.meal_timing_model = None
        self.meal_composition_model = None
        self.scaler = None
        
        # Deep learning models
        self.deep_calorie_model = None
        self.deep_macro_model = None
        self.deep_meal_composition_model = None
        self.deep_scaler = None
        
        # Load ML models and scaler
        try:
            model_dir = os.path.join(os.path.dirname(__file__), 'models')
            
            # Try to load deep learning models first (preferred)
            try:
                import tensorflow as tf
                self.deep_calorie_model = tf.keras.models.load_model(os.path.join(model_dir, 'deep_calorie_model.h5'))
                self.deep_macro_model = tf.keras.models.load_model(os.path.join(model_dir, 'deep_macro_model.h5'))
                self.deep_meal_composition_model = tf.keras.models.load_model(os.path.join(model_dir, 'deep_meal_composition_model.h5'))
                self.deep_scaler = joblib.load(os.path.join(model_dir, 'deep_scaler.joblib'))
                print("Successfully loaded deep learning models!")
            except Exception as deep_e:
                print(f"Deep learning models not available: {str(deep_e)}")
                
                # Fallback to traditional ML models
                try:
                    self.scaler = joblib.load(os.path.join(model_dir, 'feature_scaler.joblib'))
                except:
                    self.scaler = joblib.load(os.path.join(model_dir, 'scaler.joblib'))
                
                self.calorie_model = joblib.load(os.path.join(model_dir, 'calorie_model.joblib'))
                self.macro_model = joblib.load(os.path.join(model_dir, 'macro_model.joblib'))
                self.meal_timing_model = joblib.load(os.path.join(model_dir, 'meal_timing_model.joblib'))
                self.meal_composition_model = joblib.load(os.path.join(model_dir, 'meal_composition_model.joblib'))
                print("Successfully loaded traditional ML models")
        except Exception as e:
            print(f"Warning: Could not load any ML models - {str(e)}")
            print("Falling back to rule-based calculations")
        
        # Comprehensive food database with nutritional information
        self.food_database = {
            'proteins': {
                # Poultry
                'chicken_breast': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6},
                'chicken_thigh': {'calories': 209, 'protein': 26, 'carbs': 0, 'fat': 12.5},
                'chicken_wings': {'calories': 290, 'protein': 27, 'carbs': 0, 'fat': 19.5},
                'turkey_breast': {'calories': 135, 'protein': 30, 'carbs': 0, 'fat': 1},
                'turkey_thigh': {'calories': 187, 'protein': 28, 'carbs': 0, 'fat': 8},
                'duck_breast': {'calories': 337, 'protein': 19, 'carbs': 0, 'fat': 28},
                'quail': {'calories': 227, 'protein': 25, 'carbs': 0, 'fat': 14},
                
                # Red Meat
                'lean_beef': {'calories': 250, 'protein': 26, 'carbs': 0, 'fat': 17},
                'beef_sirloin': {'calories': 271, 'protein': 33, 'carbs': 0, 'fat': 16},
                'beef_tenderloin': {'calories': 267, 'protein': 29, 'carbs': 0, 'fat': 17},
                'ground_beef_90_10': {'calories': 184, 'protein': 23, 'carbs': 0, 'fat': 10},
                'lamb_chop': {'calories': 294, 'protein': 25, 'carbs': 0, 'fat': 21},
                'pork_loin': {'calories': 242, 'protein': 27, 'carbs': 0, 'fat': 14},
                'pork_tenderloin': {'calories': 143, 'protein': 26, 'carbs': 0, 'fat': 4},
                'venison': {'calories': 157, 'protein': 30, 'carbs': 0, 'fat': 3.4},
                'bison': {'calories': 143, 'protein': 28, 'carbs': 0, 'fat': 2.4},
                
                # Seafood
                'salmon': {'calories': 208, 'protein': 22, 'carbs': 0, 'fat': 13},
                'tuna': {'calories': 130, 'protein': 28, 'carbs': 0, 'fat': 1.3},
                'shrimp': {'calories': 85, 'protein': 20, 'carbs': 0, 'fat': 1.1},
                'cod': {'calories': 105, 'protein': 23, 'carbs': 0, 'fat': 1},
                'tilapia': {'calories': 128, 'protein': 26, 'carbs': 0, 'fat': 2.7},
                'halibut': {'calories': 140, 'protein': 27, 'carbs': 0, 'fat': 3},
                'mahi_mahi': {'calories': 117, 'protein': 25, 'carbs': 0, 'fat': 1},
                'sea_bass': {'calories': 124, 'protein': 24, 'carbs': 0, 'fat': 2.8},
                'sardines': {'calories': 208, 'protein': 24, 'carbs': 0, 'fat': 11},
                'mackerel': {'calories': 305, 'protein': 27, 'carbs': 0, 'fat': 21},
                'scallops': {'calories': 137, 'protein': 27, 'carbs': 5, 'fat': 1.2},
                'crab': {'calories': 120, 'protein': 26, 'carbs': 0, 'fat': 1.3},
                'lobster': {'calories': 129, 'protein': 27, 'carbs': 1, 'fat': 1.3},
                'mussels': {'calories': 172, 'protein': 24, 'carbs': 7, 'fat': 4.5},
                'oysters': {'calories': 169, 'protein': 19, 'carbs': 12, 'fat': 5},
                
                # Eggs & Dairy Proteins
                'eggs': {'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11},
                'egg_whites': {'calories': 52, 'protein': 11, 'carbs': 0.7, 'fat': 0.2},
                'greek_yogurt': {'calories': 130, 'protein': 22, 'carbs': 9, 'fat': 0.7},
                'cottage_cheese': {'calories': 120, 'protein': 14, 'carbs': 3, 'fat': 5},
                'whey_protein': {'calories': 120, 'protein': 24, 'carbs': 3, 'fat': 2},
                'casein_protein': {'calories': 120, 'protein': 24, 'carbs': 3, 'fat': 1},
                
                # Plant-Based Proteins
                'tofu': {'calories': 144, 'protein': 17, 'carbs': 3.3, 'fat': 8.7},
                'tempeh': {'calories': 195, 'protein': 20, 'carbs': 7.6, 'fat': 11},
                'seitan': {'calories': 370, 'protein': 75, 'carbs': 14, 'fat': 1.9},
                'edamame': {'calories': 189, 'protein': 17, 'carbs': 15, 'fat': 8},
                'lentils': {'calories': 230, 'protein': 18, 'carbs': 40, 'fat': 0.8},
                'black_beans': {'calories': 132, 'protein': 15, 'carbs': 41, 'fat': 0.9},
                'chickpeas': {'calories': 269, 'protein': 14.5, 'carbs': 45, 'fat': 4.3},
                'kidney_beans': {'calories': 127, 'protein': 15, 'carbs': 40, 'fat': 0.5},
                'pinto_beans': {'calories': 143, 'protein': 15, 'carbs': 45, 'fat': 1},
                'navy_beans': {'calories': 140, 'protein': 16, 'carbs': 47, 'fat': 0.6},
                'black_eyed_peas': {'calories': 160, 'protein': 13, 'carbs': 35, 'fat': 0.9},
                'mung_beans': {'calories': 212, 'protein': 14, 'carbs': 39, 'fat': 0.8},
                'pea_protein': {'calories': 120, 'protein': 24, 'carbs': 2, 'fat': 2},
                'tvp': {'calories': 160, 'protein': 24, 'carbs': 10, 'fat': 0.5},
                
                # Additional Proteins
                'hemp_protein': {'calories': 120, 'protein': 15, 'carbs': 8, 'fat': 3},
                'rice_protein': {'calories': 110, 'protein': 24, 'carbs': 2, 'fat': 1},
                'soy_protein_isolate': {'calories': 95, 'protein': 23, 'carbs': 0, 'fat': 0.5},
                'bone_broth_protein': {'calories': 90, 'protein': 20, 'carbs': 0, 'fat': 0},
                'collagen_protein': {'calories': 70, 'protein': 18, 'carbs': 0, 'fat': 0},
                'spirulina': {'calories': 290, 'protein': 57, 'carbs': 24, 'fat': 8},
                'nutritional_yeast': {'calories': 60, 'protein': 8, 'carbs': 5, 'fat': 1},
                'hemp_hearts': {'calories': 170, 'protein': 10, 'carbs': 2.5, 'fat': 14},
                'organ_meats': {'calories': 175, 'protein': 26, 'carbs': 4, 'fat': 6},
                'bone_marrow': {'calories': 786, 'protein': 7, 'carbs': 0, 'fat': 84}
            },
            'carbs': {
                # Grains
                'brown_rice': {'calories': 216, 'protein': 5, 'carbs': 45, 'fat': 1.8},
                'white_rice': {'calories': 205, 'protein': 4.3, 'carbs': 45, 'fat': 0.4},
                'basmati_rice': {'calories': 190, 'protein': 3.5, 'carbs': 45, 'fat': 0.2},
                'jasmine_rice': {'calories': 180, 'protein': 3.3, 'carbs': 43, 'fat': 0.2},
                'wild_rice': {'calories': 166, 'protein': 6.5, 'carbs': 35, 'fat': 0.6},
                'quinoa': {'calories': 120, 'protein': 4.4, 'carbs': 21, 'fat': 1.9},
                'bulgur': {'calories': 151, 'protein': 5.6, 'carbs': 34, 'fat': 0.4},
                'farro': {'calories': 170, 'protein': 6, 'carbs': 34, 'fat': 1.5},
                'barley': {'calories': 193, 'protein': 3.5, 'carbs': 44, 'fat': 1},
                'millet': {'calories': 207, 'protein': 6, 'carbs': 41, 'fat': 1.7},
                'amaranth': {'calories': 251, 'protein': 9.3, 'carbs': 46, 'fat': 5.6},
                'teff': {'calories': 255, 'protein': 9.7, 'carbs': 50, 'fat': 2},
                'buckwheat': {'calories': 155, 'protein': 5.7, 'carbs': 33, 'fat': 0.6},
                'sorghum': {'calories': 329, 'protein': 10, 'carbs': 72, 'fat': 3.3},
                
                # Starchy Vegetables
                'sweet_potato': {'calories': 103, 'protein': 2, 'carbs': 24, 'fat': 0.2},
                'white_potato': {'calories': 161, 'protein': 4.3, 'carbs': 37, 'fat': 0.2},
                'purple_potato': {'calories': 140, 'protein': 2, 'carbs': 33, 'fat': 0},
                'japanese_sweet_potato': {'calories': 113, 'protein': 1.5, 'carbs': 27, 'fat': 0.1},
                'butternut_squash': {'calories': 82, 'protein': 1.8, 'carbs': 21, 'fat': 0.2},
                'acorn_squash': {'calories': 56, 'protein': 1.1, 'carbs': 15, 'fat': 0.1},
                'pumpkin': {'calories': 49, 'protein': 1.8, 'carbs': 12, 'fat': 0.2},
                'corn': {'calories': 132, 'protein': 5, 'carbs': 29, 'fat': 1.8},
                'green_peas': {'calories': 81, 'protein': 5, 'carbs': 14, 'fat': 0.4},
                'parsnips': {'calories': 128, 'protein': 1.6, 'carbs': 30, 'fat': 0.3},
                'cassava': {'calories': 160, 'protein': 1.4, 'carbs': 38, 'fat': 0.3},
                'taro': {'calories': 142, 'protein': 2.5, 'carbs': 34, 'fat': 0.2},
                
                # Breads & Pasta
                'whole_wheat_bread': {'calories': 247, 'protein': 13, 'carbs': 41, 'fat': 3.4},
                'sourdough_bread': {'calories': 255, 'protein': 10, 'carbs': 48, 'fat': 3},
                'ezekiel_bread': {'calories': 160, 'protein': 8, 'carbs': 34, 'fat': 1},
                'rye_bread': {'calories': 259, 'protein': 8.5, 'carbs': 48, 'fat': 3.3},
                'pasta': {'calories': 200, 'protein': 7, 'carbs': 42, 'fat': 1.2},
                'whole_wheat_pasta': {'calories': 174, 'protein': 7.5, 'carbs': 37, 'fat': 0.8},
                'chickpea_pasta': {'calories': 190, 'protein': 13, 'carbs': 32, 'fat': 3.5},
                'rice_noodles': {'calories': 190, 'protein': 3.2, 'carbs': 42, 'fat': 0.4},
                'soba_noodles': {'calories': 113, 'protein': 5.8, 'carbs': 24, 'fat': 0.1},
                'udon_noodles': {'calories': 210, 'protein': 6, 'carbs': 43, 'fat': 1},
                'couscous': {'calories': 176, 'protein': 6, 'carbs': 36, 'fat': 0.3},
                
                # Breakfast Cereals
                'oats': {'calories': 307, 'protein': 13, 'carbs': 55, 'fat': 5.3},
                'steel_cut_oats': {'calories': 170, 'protein': 7, 'carbs': 29, 'fat': 3},
                'muesli': {'calories': 289, 'protein': 8, 'carbs': 61, 'fat': 4},
                'granola': {'calories': 471, 'protein': 10, 'carbs': 64, 'fat': 20},
                'cream_of_wheat': {'calories': 160, 'protein': 5, 'carbs': 34, 'fat': 0.5},
                'cream_of_rice': {'calories': 130, 'protein': 2.5, 'carbs': 28, 'fat': 0},
                
                # Additional Grains & Carbs
                'black_rice': {'calories': 160, 'protein': 4.9, 'carbs': 34, 'fat': 1.8},
                'red_rice': {'calories': 405, 'protein': 7.9, 'carbs': 86, 'fat': 2.2},
                'cauliflower_rice': {'calories': 25, 'protein': 2, 'carbs': 5, 'fat': 0.3},
                'shirataki_noodles': {'calories': 20, 'protein': 1, 'carbs': 4, 'fat': 0},
                'konjac_noodles': {'calories': 10, 'protein': 0, 'carbs': 3, 'fat': 0},
                'kelp_noodles': {'calories': 6, 'protein': 0.2, 'carbs': 1.4, 'fat': 0},
                'palmini_noodles': {'calories': 20, 'protein': 2, 'carbs': 4, 'fat': 0},
                'zucchini_noodles': {'calories': 20, 'protein': 2.7, 'carbs': 4, 'fat': 0.4},
                'spaghetti_squash': {'calories': 28, 'protein': 0.6, 'carbs': 6.9, 'fat': 0.3},
                'plantain': {'calories': 122, 'protein': 1.3, 'carbs': 31.9, 'fat': 0.4},
                'yuca': {'calories': 160, 'protein': 1.4, 'carbs': 38, 'fat': 0.3},
                'water_chestnuts': {'calories': 97, 'protein': 1.4, 'carbs': 24, 'fat': 0.1}
            },
            'fats': {
                # Nuts
                'almonds': {'calories': 164, 'protein': 6, 'carbs': 6.1, 'fat': 14},
                'walnuts': {'calories': 185, 'protein': 4.3, 'carbs': 3.9, 'fat': 18.5},
                'cashews': {'calories': 157, 'protein': 5.2, 'carbs': 8.6, 'fat': 12.4},
                'macadamia_nuts': {'calories': 204, 'protein': 2.2, 'carbs': 3.9, 'fat': 21.5},
                'pecans': {'calories': 196, 'protein': 2.6, 'carbs': 3.9, 'fat': 20.4},
                'pistachios': {'calories': 159, 'protein': 5.7, 'carbs': 7.7, 'fat': 12.9},
                'brazil_nuts': {'calories': 186, 'protein': 4.1, 'carbs': 3.3, 'fat': 19},
                'pine_nuts': {'calories': 191, 'protein': 3.9, 'carbs': 3.7, 'fat': 19.1},
                'hazelnuts': {'calories': 178, 'protein': 4.2, 'carbs': 4.7, 'fat': 17.2},
                
                # Seeds
                'chia_seeds': {'calories': 138, 'protein': 4.7, 'carbs': 12, 'fat': 8.7},
                'flax_seeds': {'calories': 150, 'protein': 5.2, 'carbs': 8.2, 'fat': 12},
                'sunflower_seeds': {'calories': 164, 'protein': 5.8, 'carbs': 5.6, 'fat': 14.4},
                'pumpkin_seeds': {'calories': 158, 'protein': 8.6, 'carbs': 3.8, 'fat': 13.9},
                'hemp_seeds': {'calories': 166, 'protein': 9.5, 'carbs': 2.6, 'fat': 14.6},
                'sesame_seeds': {'calories': 173, 'protein': 5, 'carbs': 6.6, 'fat': 15},
                'poppy_seeds': {'calories': 151, 'protein': 5.8, 'carbs': 4.5, 'fat': 13.5},
                
                # Nut & Seed Butters
                'peanut_butter': {'calories': 188, 'protein': 8, 'carbs': 6, 'fat': 16},
                'almond_butter': {'calories': 180, 'protein': 6.7, 'carbs': 6.6, 'fat': 16.2},
                'cashew_butter': {'calories': 187, 'protein': 5.6, 'carbs': 7.6, 'fat': 15.8},
                'sunflower_butter': {'calories': 197, 'protein': 5.5, 'carbs': 7.2, 'fat': 17.7},
                'tahini': {'calories': 178, 'protein': 5.2, 'carbs': 6.5, 'fat': 16},
                'walnut_butter': {'calories': 183, 'protein': 4.8, 'carbs': 3.4, 'fat': 18.3},
                
                # Oils
                'olive_oil': {'calories': 120, 'protein': 0, 'carbs': 0, 'fat': 14},
                'coconut_oil': {'calories': 120, 'protein': 0, 'carbs': 0, 'fat': 14},
                'avocado_oil': {'calories': 124, 'protein': 0, 'carbs': 0, 'fat': 14},
                'mct_oil': {'calories': 115, 'protein': 0, 'carbs': 0, 'fat': 14},
                'walnut_oil': {'calories': 120, 'protein': 0, 'carbs': 0, 'fat': 14},
                'flaxseed_oil': {'calories': 120, 'protein': 0, 'carbs': 0, 'fat': 14},
                'sesame_oil': {'calories': 120, 'protein': 0, 'carbs': 0, 'fat': 14},
                'ghee': {'calories': 123, 'protein': 0, 'carbs': 0, 'fat': 14},
                
                # Other Healthy Fats
                'avocado': {'calories': 160, 'protein': 2, 'carbs': 8.5, 'fat': 14.7},
                'coconut': {'calories': 354, 'protein': 3.3, 'carbs': 15, 'fat': 33},
                'olives': {'calories': 115, 'protein': 0.8, 'carbs': 6.3, 'fat': 10.7},
                'dark_chocolate': {'calories': 170, 'protein': 2.2, 'carbs': 13, 'fat': 12}
            },
            'vegetables': {
                # Leafy Greens
                'spinach': {'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4},
                'kale': {'calories': 33, 'protein': 2.2, 'carbs': 6.7, 'fat': 0.5},
                'romaine_lettuce': {'calories': 17, 'protein': 1.2, 'carbs': 3.3, 'fat': 0.3},
                'arugula': {'calories': 25, 'protein': 2.6, 'carbs': 3.7, 'fat': 0.4},
                'swiss_chard': {'calories': 19, 'protein': 1.8, 'carbs': 3.7, 'fat': 0.2},
                'collard_greens': {'calories': 32, 'protein': 3, 'carbs': 5.7, 'fat': 0.5},
                'watercress': {'calories': 11, 'protein': 2.3, 'carbs': 1.3, 'fat': 0.1},
                'mustard_greens': {'calories': 27, 'protein': 2.9, 'carbs': 4.7, 'fat': 0.2},
                
                # Cruciferous Vegetables
                'broccoli': {'calories': 55, 'protein': 3.7, 'carbs': 11.2, 'fat': 0.6},
                'cauliflower': {'calories': 25, 'protein': 2, 'carbs': 5, 'fat': 0.3},
                'brussels_sprouts': {'calories': 43, 'protein': 3.4, 'carbs': 9, 'fat': 0.3},
                'cabbage': {'calories': 25, 'protein': 1.3, 'carbs': 5.8, 'fat': 0.1},
                'bok_choy': {'calories': 13, 'protein': 1.5, 'carbs': 2.2, 'fat': 0.2},
                'kohlrabi': {'calories': 27, 'protein': 1.7, 'carbs': 6.2, 'fat': 0.1},
                'radishes': {'calories': 16, 'protein': 0.7, 'carbs': 3.4, 'fat': 0.1},
                
                # Nightshade Vegetables
                'tomatoes': {'calories': 22, 'protein': 1.1, 'carbs': 4.8, 'fat': 0.2},
                'bell_peppers': {'calories': 30, 'protein': 1, 'carbs': 7, 'fat': 0.2},
                'eggplant': {'calories': 25, 'protein': 1, 'carbs': 6, 'fat': 0.2},
                'chili_peppers': {'calories': 40, 'protein': 1.9, 'carbs': 8.8, 'fat': 0.4},
                
                # Root Vegetables
                'carrots': {'calories': 41, 'protein': 0.9, 'carbs': 9.6, 'fat': 0.2},
                'beets': {'calories': 43, 'protein': 1.6, 'carbs': 9.6, 'fat': 0.2},
                'turnips': {'calories': 28, 'protein': 0.9, 'carbs': 6.4, 'fat': 0.1},
                'rutabaga': {'calories': 38, 'protein': 1.1, 'carbs': 8.8, 'fat': 0.2},
                'radishes': {'calories': 16, 'protein': 0.7, 'carbs': 3.4, 'fat': 0.1},
                
                # Other Vegetables
                'mushrooms': {'calories': 22, 'protein': 3.1, 'carbs': 3.3, 'fat': 0.3},
                'asparagus': {'calories': 20, 'protein': 2.2, 'carbs': 3.9, 'fat': 0.2},
                'green_beans': {'calories': 31, 'protein': 1.8, 'carbs': 7, 'fat': 0.2},
                'zucchini': {'calories': 17, 'protein': 1.2, 'carbs': 3.1, 'fat': 0.3},
                'cucumber': {'calories': 8, 'protein': 0.5, 'carbs': 1.9, 'fat': 0.1},
                'celery': {'calories': 16, 'protein': 0.7, 'carbs': 3, 'fat': 0.2},
                'artichokes': {'calories': 47, 'protein': 3.3, 'carbs': 10.5, 'fat': 0.2},
                'bamboo_shoots': {'calories': 27, 'protein': 2.6, 'carbs': 5, 'fat': 0.3},
                'seaweed': {'calories': 30, 'protein': 1.3, 'carbs': 9.6, 'fat': 0.5},
                'okra': {'calories': 33, 'protein': 1.9, 'carbs': 7, 'fat': 0.2},
                'jicama': {'calories': 38, 'protein': 0.7, 'carbs': 9, 'fat': 0.1}
            },
            'fruits': {
                # Berries
                'blueberries': {'calories': 57, 'protein': 0.7, 'carbs': 14.5, 'fat': 0.3},
                'strawberries': {'calories': 32, 'protein': 0.7, 'carbs': 7.7, 'fat': 0.3},
                'raspberries': {'calories': 52, 'protein': 1.2, 'carbs': 11.9, 'fat': 0.7},
                'blackberries': {'calories': 43, 'protein': 1.4, 'carbs': 9.6, 'fat': 0.5},
                'goji_berries': {'calories': 98, 'protein': 3.3, 'carbs': 21.6, 'fat': 0.4},
                'acai_berries': {'calories': 70, 'protein': 1, 'carbs': 4, 'fat': 5},
                
                # Citrus Fruits
                'orange': {'calories': 62, 'protein': 1.2, 'carbs': 15.4, 'fat': 0.2},
                'grapefruit': {'calories': 42, 'protein': 0.8, 'carbs': 10.7, 'fat': 0.1},
                'lemon': {'calories': 29, 'protein': 1.1, 'carbs': 9.3, 'fat': 0.3},
                'lime': {'calories': 20, 'protein': 0.5, 'carbs': 7.1, 'fat': 0.1},
                'tangerine': {'calories': 53, 'protein': 0.8, 'carbs': 13.3, 'fat': 0.3},
                'pomelo': {'calories': 38, 'protein': 0.8, 'carbs': 9.4, 'fat': 0.1},
                
                # Tropical Fruits
                'mango': {'calories': 99, 'protein': 1.4, 'carbs': 24.7, 'fat': 0.6},
                'pineapple': {'calories': 82, 'protein': 0.9, 'carbs': 21.6, 'fat': 0.2},
                'papaya': {'calories': 43, 'protein': 0.5, 'carbs': 10.8, 'fat': 0.3},
                'coconut': {'calories': 354, 'protein': 3.3, 'carbs': 15, 'fat': 33},
                'guava': {'calories': 68, 'protein': 2.6, 'carbs': 14.3, 'fat': 1},
                'passion_fruit': {'calories': 97, 'protein': 2.2, 'carbs': 23.4, 'fat': 0.7},
                'dragon_fruit': {'calories': 60, 'protein': 1.2, 'carbs': 13, 'fat': 0},
                'lychee': {'calories': 66, 'protein': 0.8, 'carbs': 16.5, 'fat': 0.4},
                
                # Stone Fruits
                'peach': {'calories': 59, 'protein': 1.4, 'carbs': 14.3, 'fat': 0.4},
                'plum': {'calories': 46, 'protein': 0.7, 'carbs': 11.4, 'fat': 0.3},
                'nectarine': {'calories': 44, 'protein': 1.1, 'carbs': 10.6, 'fat': 0.3},
                'apricot': {'calories': 48, 'protein': 1.4, 'carbs': 11.1, 'fat': 0.4},
                'cherries': {'calories': 50, 'protein': 1, 'carbs': 12.2, 'fat': 0.3},
                
                # Other Fruits
                'apple': {'calories': 95, 'protein': 0.5, 'carbs': 25, 'fat': 0.3},
                'pear': {'calories': 101, 'protein': 0.6, 'carbs': 27, 'fat': 0.2},
                'banana': {'calories': 105, 'protein': 1.3, 'carbs': 27, 'fat': 0.3},
                'grapes': {'calories': 69, 'protein': 0.7, 'carbs': 18.1, 'fat': 0.2},
                'kiwi': {'calories': 61, 'protein': 1.1, 'carbs': 14.7, 'fat': 0.5},
                'pomegranate': {'calories': 83, 'protein': 1.7, 'carbs': 18.7, 'fat': 1.2},
                'figs': {'calories': 74, 'protein': 0.8, 'carbs': 19.2, 'fat': 0.3},
                'dates': {'calories': 282, 'protein': 2.5, 'carbs': 75, 'fat': 0.4},
                'persimmon': {'calories': 118, 'protein': 0.6, 'carbs': 31.2, 'fat': 0.3}
            },
            'dairy': {
                # Milk
                'whole_milk': {'calories': 149, 'protein': 8, 'carbs': 12, 'fat': 8},
                'reduced_fat_milk': {'calories': 122, 'protein': 8.1, 'carbs': 12, 'fat': 4.8},
                'skim_milk': {'calories': 83, 'protein': 8.3, 'carbs': 12, 'fat': 0.2},
                'almond_milk': {'calories': 30, 'protein': 1, 'carbs': 1, 'fat': 2.5},
                'soy_milk': {'calories': 80, 'protein': 7, 'carbs': 4, 'fat': 4},
                'oat_milk': {'calories': 120, 'protein': 3, 'carbs': 16, 'fat': 5},
                'cashew_milk': {'calories': 25, 'protein': 1, 'carbs': 1, 'fat': 2},
                'coconut_milk': {'calories': 230, 'protein': 2.3, 'carbs': 5.5, 'fat': 23},
                
                # Yogurt
                'greek_yogurt': {'calories': 130, 'protein': 22, 'carbs': 9, 'fat': 0.7},
                'regular_yogurt': {'calories': 150, 'protein': 12, 'carbs': 17, 'fat': 8},
                'skyr': {'calories': 110, 'protein': 22, 'carbs': 6, 'fat': 0.4},
                'kefir': {'calories': 150, 'protein': 10, 'carbs': 12, 'fat': 8},
                'coconut_yogurt': {'calories': 130, 'protein': 1, 'carbs': 13, 'fat': 8},
                'almond_yogurt': {'calories': 120, 'protein': 5, 'carbs': 9, 'fat': 7},
                
                # Cheese
                'cheddar': {'calories': 402, 'protein': 25, 'carbs': 1.3, 'fat': 33},
                'mozzarella': {'calories': 280, 'protein': 28, 'carbs': 2.2, 'fat': 17},
                'feta': {'calories': 264, 'protein': 14, 'carbs': 4.1, 'fat': 21},
                'cottage_cheese': {'calories': 120, 'protein': 14, 'carbs': 3, 'fat': 5},
                'ricotta': {'calories': 174, 'protein': 11, 'carbs': 4, 'fat': 13},
                'parmesan': {'calories': 431, 'protein': 38, 'carbs': 4.1, 'fat': 29},
                'gouda': {'calories': 356, 'protein': 25, 'carbs': 2.2, 'fat': 27},
                'brie': {'calories': 334, 'protein': 21, 'carbs': 0.5, 'fat': 28},
                
                # Other Dairy
                'whey_protein': {'calories': 120, 'protein': 24, 'carbs': 3, 'fat': 2},
                'casein_protein': {'calories': 120, 'protein': 24, 'carbs': 3, 'fat': 1},
                'cream_cheese': {'calories': 342, 'protein': 6, 'carbs': 4.1, 'fat': 34},
                'sour_cream': {'calories': 193, 'protein': 2.1, 'carbs': 4.6, 'fat': 20},
                'heavy_cream': {'calories': 340, 'protein': 2.8, 'carbs': 2.8, 'fat': 36},
                'half_and_half': {'calories': 130, 'protein': 3, 'carbs': 4, 'fat': 12}
            }
        }

    def preprocess_user_data(self, user_data: Dict[str, Any], meal_type: str = None) -> np.ndarray:
        """Preprocess user data to match the training data format"""
        # Extract and validate required fields
        required_fields = ['weight', 'height', 'age', 'gender', 'activity_level', 'goal']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Convert dietary preferences to boolean flags
        is_vegetarian = user_data.get('vegetarian', False)
        is_vegan = user_data.get('vegan', False)
        is_gluten_free = 'Gluten-Free' in user_data.get('dietary_preferences', [])
        is_dairy_free = 'Dairy-Free' in user_data.get('dietary_preferences', [])
        
        # Numerical features
        numerical_features = np.array([
            float(user_data.get('weight', 70)), 
            float(user_data.get('height', 170)),
            float(user_data.get('age', 25)),
            float(user_data.get('body_fat_pct', 20)),
            float(user_data.get('blood_pressure_systolic', 120)),
            float(user_data.get('blood_pressure_diastolic', 80)),
            float(user_data.get('resting_heart_rate', 70)),
            float(user_data.get('hours_sleep', 7))
        ]).reshape(1, -1)
        
        # Gender encoding (binary)
        gender_encoded = np.array([1 if user_data.get('gender', 'male').lower() == 'male' else 0]).reshape(1, -1)
        
        # Activity level one-hot encoding
        activity_categories = ['sedentary', 'light', 'moderate', 'active', 'very_active']
        activity_level = user_data.get('activity_level', 'moderate').lower()
        activity_encoded = np.zeros((1, len(activity_categories)))
        try:
            activity_idx = activity_categories.index(activity_level)
            activity_encoded[0, activity_idx] = 1
        except ValueError:
            activity_encoded[0, activity_categories.index('moderate')] = 1 
        
        # Goal one-hot encoding
        goal_categories = ['weight_loss', 'maintenance', 'muscle_gain']
        goal = user_data.get('goal', 'maintenance').lower()
        goal_encoded = np.zeros((1, len(goal_categories)))
        try:
            goal_idx = goal_categories.index(goal)
            goal_encoded[0, goal_idx] = 1
        except ValueError:
            goal_encoded[0, goal_categories.index('maintenance')] = 1  
        
        # Fitness level one-hot encoding
        fitness_categories = ['beginner', 'intermediate', 'advanced']
        fitness_level = user_data.get('fitness_level', 'intermediate').lower()
        fitness_encoded = np.zeros((1, len(fitness_categories)))
        try:
            fitness_idx = fitness_categories.index(fitness_level)
            fitness_encoded[0, fitness_idx] = 1
        except ValueError:
            fitness_encoded[0, fitness_categories.index('intermediate')] = 1  
        # Boolean features
        boolean_features = np.array([
            1 if is_vegetarian else 0,
            1 if is_vegan else 0,
            1 if is_gluten_free else 0,
            1 if is_dairy_free else 0
        ]).reshape(1, -1)
        
        # Meal type encoding (if provided)
        if meal_type:
            meal_type_categories = ['breakfast', 'lunch', 'dinner', 'snack']
            meal_type_encoded = np.zeros((1, len(meal_type_categories)))
            try:
                meal_idx = meal_type_categories.index(meal_type.lower())
                meal_type_encoded[0, meal_idx] = 1
            except ValueError:
                meal_type_encoded[0, meal_type_categories.index('snack')] = 1  
        else:
            meal_type_encoded = np.zeros((1, 4))  
        
        # Combine all features
        X = np.hstack([
            numerical_features,     
            gender_encoded,       
            activity_encoded,      
            goal_encoded,         
            fitness_encoded,       
            boolean_features,      
            meal_type_encoded     
        ])  
        
        # Scale features
        if self.scaler is not None:
            X = self.scaler.transform(X)
        
        return X

    def prepare_deep_features(self, user_data: Dict[str, Any]) -> np.ndarray:
        """Prepare features for deep learning models"""
        # Activity level mapping
        activity_mapping = {
            'sedentary': 0, 'light': 1, 'moderate': 2, 'active': 3, 'very_active': 4
        }
        
        # Goal mapping
        goal_mapping = {
            'weight_loss': 0, 'maintenance': 1, 'muscle_gain': 2
        }
        
        # Fitness level mapping
        fitness_mapping = {
            'beginner': 0, 'intermediate': 1, 'advanced': 2
        }
        
        # Gender mapping
        gender_value = 1 if user_data.get('gender', 'male').lower() == 'male' else 0
        
        # Prepare feature vector
        features = np.array([
            float(user_data.get('weight', 70)),
            float(user_data.get('height', 170)),
            float(user_data.get('age', 25)),
            gender_value,
            activity_mapping.get(user_data.get('activity_level', 'moderate'), 2),
            goal_mapping.get(user_data.get('goal', 'maintenance'), 1),
            fitness_mapping.get(user_data.get('fitness_level', 'intermediate'), 1),
            float(user_data.get('body_fat_pct', 20)),
            float(user_data.get('blood_pressure_systolic', 120)),
            float(user_data.get('blood_pressure_diastolic', 80)),
            float(user_data.get('resting_heart_rate', 70)),
            float(user_data.get('hours_sleep', 7)),
            1 if user_data.get('vegetarian', False) else 0,
            1 if user_data.get('vegan', False) else 0,
            1 if 'Gluten-Free' in user_data.get('dietary_preferences', []) else 0,
            1 if 'Dairy-Free' in user_data.get('dietary_preferences', []) else 0,
            float(user_data.get('meals_per_day', 4))
        ])
        
        return features

    def predict_calories(self, user_data: Dict[str, Any]) -> float:
        """Predict daily calorie needs using deep learning, ML model or traditional method"""
        # Validate required user data
        required_fields = ['weight', 'height', 'age', 'gender', 'activity_level']
        for field in required_fields:
            if field not in user_data or user_data[field] is None:
                raise ValueError(f"Missing required field for calorie calculation: {field}")
        
        # Check for default values that indicate incomplete profile
        if (user_data['weight'] == 70.0 and user_data['height'] == 170.0 and user_data['age'] == 18):
            print("WARNING: User appears to be using default profile values. Meal plan calories may not be accurate.")
        
        # Try deep learning model first
        if self.deep_calorie_model is not None and self.deep_scaler is not None:
            # Prepare features for deep learning model
            features = self.prepare_deep_features(user_data)
            features_scaled = self.deep_scaler.transform(features.reshape(1, -1))
            
            # Predict using deep learning model
            predicted_calories = float(self.deep_calorie_model.predict(features_scaled, verbose=0)[0][0])
            print(f"Deep Learning Model predicted calories: {predicted_calories:.0f} for user: weight={user_data['weight']}kg, height={user_data['height']}cm, age={user_data['age']}, goal={user_data.get('goal', 'maintenance')}")
            return max(1200, predicted_calories)  # Ensure minimum safe calorie intake
        
        elif self.calorie_model is not None:
            # Use traditional ML model for prediction
            features = self.preprocess_user_data(user_data)
            predicted_calories = self.calorie_model.predict(features)[0]
            # Add goal-based adjustment
            goal_adjustments = {
                'weight_loss': -500,
                'maintenance': 0,
                'muscle_gain': 500
            }
            predicted_calories += goal_adjustments.get(user_data.get('goal', 'maintenance').lower(), 0)
            print(f"ML Model predicted calories: {predicted_calories:.0f} for user: weight={user_data['weight']}kg, height={user_data['height']}cm, age={user_data['age']}, goal={user_data.get('goal', 'maintenance')}")
            return max(1200, predicted_calories)  # Ensure minimum safe calorie intake
        else:
            # Fallback to traditional TDEE calculation
            tdee_calories = self.calculate_tdee(
                user_data['weight'],
                user_data['height'], 
                user_data['age'],
                user_data['gender'],
                user_data['activity_level']
            )
            
            # Apply goal-based adjustments
            goal_adjustments = {
                'weight_loss': -500,
                'maintenance': 0,
                'muscle_gain': 500
            }
            final_calories = tdee_calories + goal_adjustments.get(user_data.get('goal', 'maintenance').lower(), 0)
            print(f"TDEE calculated calories: {final_calories:.0f} for user: weight={user_data['weight']}kg, height={user_data['height']}cm, age={user_data['age']}, activity={user_data['activity_level']}, goal={user_data.get('goal', 'maintenance')}")
            return max(1200, final_calories)  # Ensure minimum safe calorie intake

    def predict_macros(self, calories: float, user_data: Dict[str, Any]) -> Dict[str, float]:
        """Predict macro distribution using ML model or traditional method"""
        features = self.preprocess_user_data(user_data)
        
        if self.macro_model is not None:
            # Add calories as a feature (scaled to match training data)
            calories_scaled = (calories - 2000) / 500  # Simple scaling based on typical calorie range
            features = np.hstack([features, np.array(calories_scaled).reshape(1, -1)])
            
            # Predict macro ratios
            protein_ratio, carb_ratio, fat_ratio = self.macro_model.predict(features)[0]
            
            return {
                'protein': (calories * protein_ratio) / 4,  
                'carbs': (calories * carb_ratio) / 4,      
                'fat': (calories * fat_ratio) / 9         
            }
        else:
            # Fallback to traditional macro calculation
            return self.calculate_macros(calories, user_data.get('goal', 'maintenance'))

    def predict_meal_composition(self, meal_type: str, user_data: Dict[str, Any]) -> Dict[str, float]:
        """Predict optimal meal composition using ML model"""
        # Preprocess user data with meal type included
        features = self.preprocess_user_data(user_data, meal_type)
        
        if self.meal_timing_model is not None:
            # Predict food group ratios
            ratios = self.meal_timing_model.predict(features)[0]
            return {
                'proteins': ratios[0],
                'carbs': ratios[1],
                'fats': ratios[2],
                'vegetables': ratios[3],
                'fruits': ratios[4],
                'dairy': ratios[5]
            }
        else:
            # Fallback to traditional meal templates
            return self.get_default_meal_composition(meal_type)

    def get_default_meal_composition(self, meal_type: str) -> Dict[str, float]:
        """Get default meal composition ratios"""
        templates = {
            'breakfast': {
                'proteins': 0.3,
                'carbs': 0.3,
                'fats': 0.2,
                'fruits': 0.1,
                'dairy': 0.1,
                'vegetables': 0
            },
            'lunch': {
                'proteins': 0.3,
                'carbs': 0.3,
                'fats': 0.15,
                'vegetables': 0.25,
                'fruits': 0,
                'dairy': 0
            },
            'dinner': {
                'proteins': 0.35,
                'carbs': 0.25,
                'fats': 0.15,
                'vegetables': 0.25,
                'fruits': 0,
                'dairy': 0
            },
            'snack': {
                'proteins': 0.3,
                'carbs': 0.3,
                'fats': 0.2,
                'fruits': 0.2,
                'dairy': 0,
                'vegetables': 0
            }
        }
        return templates.get(meal_type.lower(), templates['snack'])

    def calculate_tdee(self, weight: float, height: float, age: int, 
                      gender: str, activity_level: str) -> float:
        """Calculate Total Daily Energy Expenditure"""
        # Calculate BMR using the Mifflin-St Jeor Equation
        # For men: 10×weight (kg)+6.25×height (cm)−5×age (years)+5
        # For women: 10×weight (kg)+6.25×height (cm)−5×age (years)−161
        if gender.lower() == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        # Activity multipliers
        activity_multipliers = {
            'sedentary': 1.2,      
            'light': 1.375,       
            'moderate': 1.55,     
            'active': 1.725,       
            'very_active': 1.9     
        }

        return bmr * activity_multipliers.get(activity_level.lower(), 1.2)

    def calculate_macros(self, calories: float, goal: str) -> Dict[str, float]:
        """Calculate macronutrient ratios based on goal"""
        macros = {
            'weight_loss': {'protein': 0.35, 'carbs': 0.40, 'fat': 0.25},  
            'maintenance': {'protein': 0.30, 'carbs': 0.45, 'fat': 0.25},  
            'muscle_gain': {'protein': 0.40, 'carbs': 0.40, 'fat': 0.20}   
        }

        goal_macros = macros.get(goal.lower(), macros['maintenance'])
        return {
            'protein': (calories * goal_macros['protein']) / 4,  
            'carbs': (calories * goal_macros['carbs']) / 4,     
            'fat': (calories * goal_macros['fat']) / 9,        
        }

    def filter_foods_by_preferences(self, preferences: Dict[str, Any]) -> None:
        """Filter food database based on dietary preferences and restrictions"""
        filtered_database = self.food_database.copy()
        
        # Handle vegetarian preference
        if preferences.get('vegetarian'):
            if 'proteins' in filtered_database:
                filtered_database['proteins'] = {
                    k: v for k, v in filtered_database['proteins'].items()
                    if k in ['tofu', 'tempeh', 'seitan', 'eggs', 'egg_whites', 'greek_yogurt',
                            'cottage_cheese', 'whey_protein', 'casein_protein', 'lentils',
                            'black_beans', 'chickpeas', 'kidney_beans', 'pinto_beans',
                            'navy_beans', 'black_eyed_peas', 'mung_beans', 'pea_protein', 'tvp']
                }
        
        # Handle vegan preference
        if preferences.get('vegan'):
            if 'proteins' in filtered_database:
                filtered_database['proteins'] = {
                    k: v for k, v in filtered_database['proteins'].items()
                    if k in ['tofu', 'tempeh', 'seitan', 'lentils', 'black_beans',
                            'chickpeas', 'kidney_beans', 'pinto_beans', 'navy_beans',
                            'black_eyed_peas', 'mung_beans', 'pea_protein', 'tvp']
                }
            if 'dairy' in filtered_database:
                filtered_database['dairy'] = {
                    k: v for k, v in filtered_database['dairy'].items()
                    if 'milk' in k and k != 'whole_milk' and k != 'reduced_fat_milk' and k != 'skim_milk'
                }

        # Handle special diets from dietary_preferences
        dietary_preferences = preferences.get('dietary_preferences', [])
        
        # Handle Keto diet
        if 'Keto' in dietary_preferences:
            # Remove high-carb foods
            if 'carbs' in filtered_database:
                filtered_database['carbs'] = {
                    k: v for k, v in filtered_database['carbs'].items()
                    if v['carbs'] <= 10  # Only keep very low carb options
                }
            # Keep high-fat foods
            if 'fats' in filtered_database:
                filtered_database['fats'] = {
                    k: v for k, v in filtered_database['fats'].items()
                    if v['fat'] >= 5  # Focus on fatty foods
                }
            # Keep high-fat proteins
            if 'proteins' in filtered_database:
                filtered_database['proteins'] = {
                    k: v for k, v in filtered_database['proteins'].items()
                    if v['carbs'] <= 5  # Low carb proteins only
                }
            # Remove high-carb fruits
            if 'fruits' in filtered_database:
                filtered_database['fruits'] = {
                    k: v for k, v in filtered_database['fruits'].items()
                    if v['carbs'] <= 10  # Only berries and low-carb fruits
                }

        # Handle Low Carb diet
        if 'Low Carb' in dietary_preferences:
            if 'carbs' in filtered_database:
                filtered_database['carbs'] = {
                    k: v for k, v in filtered_database['carbs'].items()
                    if v['carbs'] <= 20  # Only moderate-low carb options
                }
            # Keep moderate carb proteins
            if 'proteins' in filtered_database:
                filtered_database['proteins'] = {
                    k: v for k, v in filtered_database['proteins'].items()
                    if v['carbs'] <= 10  # Moderate-low carb proteins
                }
            # Limit high-carb fruits
            if 'fruits' in filtered_database:
                filtered_database['fruits'] = {
                    k: v for k, v in filtered_database['fruits'].items()
                    if v['carbs'] <= 15  # Lower carb fruits
                }
        
        # Handle gluten-free preference
        if 'Gluten-Free' in dietary_preferences:
            if 'carbs' in filtered_database:
                filtered_database['carbs'] = {
                    k: v for k, v in filtered_database['carbs'].items()
                    if k not in ['whole_wheat_bread', 'sourdough_bread', 'rye_bread', 'pasta',
                               'whole_wheat_pasta', 'udon_noodles', 'couscous']
                }
        
        # Handle dairy-free preference
        if 'Dairy-Free' in dietary_preferences:
            if 'dairy' in filtered_database:
                filtered_database['dairy'] = {
                    k: v for k, v in filtered_database['dairy'].items()
                    if k in ['almond_milk', 'soy_milk', 'oat_milk', 'cashew_milk', 'coconut_milk',
                            'coconut_yogurt', 'almond_yogurt']
                }
            if 'proteins' in filtered_database:
                filtered_database['proteins'] = {
                    k: v for k, v in filtered_database['proteins'].items()
                    if not any(x in k for x in ['milk', 'cheese', 'yogurt', 'whey', 'casein'])
                }
        
        # Handle allergies
        for allergy in preferences.get('allergies', []):
            allergy = allergy.lower()
            if allergy == 'nuts':
                if 'fats' in filtered_database:
                    filtered_database['fats'] = {
                        k: v for k, v in filtered_database['fats'].items()
                        if 'nuts' not in k and 'nut' not in k
                    }
            elif allergy == 'dairy':
                if 'dairy' in filtered_database:
                    filtered_database['dairy'] = {}
                if 'proteins' in filtered_database:
                    filtered_database['proteins'] = {
                        k: v for k, v in filtered_database['proteins'].items()
                        if not any(x in k for x in ['milk', 'cheese', 'yogurt', 'whey', 'casein'])
                    }
            elif allergy == 'shellfish':
                if 'proteins' in filtered_database:
                    filtered_database['proteins'] = {
                        k: v for k, v in filtered_database['proteins'].items()
                        if not any(x in k for x in ['shrimp', 'crab', 'lobster', 'scallops', 'mussels', 'oysters'])
                    }
            elif allergy == 'soy':
                if 'proteins' in filtered_database:
                    filtered_database['proteins'] = {
                        k: v for k, v in filtered_database['proteins'].items()
                        if k not in ['tofu', 'tempeh', 'edamame']
                    }
        
        # Adjust macro ratios for special diets
        if 'Keto' in dietary_preferences:
            self.macro_ratios = {
                'weight_loss': {'protein': 0.35, 'carbs': 0.05, 'fat': 0.60},
                'maintenance': {'protein': 0.30, 'carbs': 0.05, 'fat': 0.65},
                'muscle_gain': {'protein': 0.35, 'carbs': 0.05, 'fat': 0.60}
            }
        elif 'Low Carb' in dietary_preferences:
            self.macro_ratios = {
                'weight_loss': {'protein': 0.40, 'carbs': 0.20, 'fat': 0.40},
                'maintenance': {'protein': 0.35, 'carbs': 0.25, 'fat': 0.40},
                'muscle_gain': {'protein': 0.40, 'carbs': 0.20, 'fat': 0.40}
            }
        
        self.food_database = filtered_database

    def adjust_portions(self, food: Dict[str, float], target: Dict[str, float]) -> Dict[str, float]:
        """Adjust food portions to match target macros"""
        portions = {}
        
        # Define minimum portions for different food types (in grams)
        min_portions = {
            'eggs': 50,  # 1 egg
            'whey_protein': 30,  # 1 scoop
            'bread': 30,  # 1 slice
            'oils': 5,  # 1 teaspoon
            'fruits': 100,  # standard serving
            'vegetables': 100,  # standard serving
            'nuts': 30,  # standard serving
            'dairy': 100,  # standard serving
            'meat': 100,  # standard serving
            'fish': 100,  # standard serving
            'legumes': 100,  # standard serving
            'grains': 50  # standard serving
        }

        for food_type, foods in food.items():
            # Calculate total target macros for this food type
            total_target = 0
            if food_type == 'proteins':
                total_target = target['protein']
            elif food_type == 'carbs':
                total_target = target['carbs']
            elif food_type == 'fats':
                total_target = target['fat']
            
            # Distribute target among foods of this type
            num_foods = len(foods)
            if num_foods > 0:
                target_per_food = total_target / num_foods
                
                for name, nutrients in foods.items():
                    # Determine base portion based on food type
                    base_portion = 100  # default
                    
                    # Set minimum portion based on food type
                    for food_category, min_portion in min_portions.items():
                        if food_category in name.lower() or food_category.rstrip('s') in name.lower():
                            base_portion = min_portion
                            break
                    
                    # Calculate portion based on target macros
                    if food_type == 'proteins' and nutrients['protein'] > 0:
                        portion = max(base_portion, (target_per_food / (nutrients['protein'] / 100)))
                    elif food_type == 'carbs' and nutrients['carbs'] > 0:
                        portion = max(base_portion, (target_per_food / (nutrients['carbs'] / 100)))
                    elif food_type == 'fats' and nutrients['fat'] > 0:
                        portion = max(base_portion, (target_per_food / (nutrients['fat'] / 100)))
                    else:
                        portion = base_portion
                    
                    # Ensure minimum portion size
                    portion = max(portion, base_portion)
                    
                    # Round portion appropriately
                    if 'egg' in name.lower():
                        portion = max(1, round(portion / 50)) * 50  # Round to whole eggs
                    elif 'protein' in name.lower() and 'whey' in name.lower():
                        portion = max(1, round(portion / 30)) * 30  # Round to whole scoops
                    else:
                        portion = round(portion / 5) * 5  # Round to nearest 5g
                    
                    portions[name] = portion

        return portions

    def generate_meal(self, target_calories: float, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a single meal based on target calories and preferences"""
        # Calculate target macros for this meal
        meal_macros = self.calculate_macros(target_calories, preferences.get('goal', 'maintenance'))
        
        # Initialize meal structure
        meal = {
            'foods': [],
            'nutrition': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        }
        
        # Get meal composition
        meal_type = preferences.get('meal_type', 'breakfast')
        meal_composition = self.predict_meal_composition(meal_type, preferences)
        
        # Select foods for meal with limited quantities per category
        selected_foods = self._select_foods_for_meal(meal_type, meal_composition)
        
        # Calculate portions more accurately based on target macros, not just calories
        total_target_calories = target_calories
        target_protein = meal_macros['protein']
        target_carbs = meal_macros['carbs'] 
        target_fat = meal_macros['fat']
        
        current_nutrition = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        
        # Add foods to meal with macro-targeted portion control
        for category, foods in selected_foods.items():
            if not foods:
                continue
                
            # Calculate macro targets for this category
            if category == 'proteins':
                category_target_protein = target_protein * meal_composition.get(category, 0)
                category_target_calories = category_target_protein * 4  # 4 cal per g protein
            elif category == 'carbs':
                category_target_carbs = target_carbs * meal_composition.get(category, 0)
                category_target_calories = category_target_carbs * 4  # 4 cal per g carbs
            elif category == 'fats':
                category_target_fat = target_fat * meal_composition.get(category, 0)
                category_target_calories = category_target_fat * 9  # 9 cal per g fat
            else:
                # For other categories (vegetables, fruits, dairy), use calorie-based targeting
                category_target_calories = total_target_calories * meal_composition.get(category, 0)
            
            if category_target_calories > 0:
                # Distribute target among foods in this category
                target_per_food = category_target_calories / len(foods)
                
                for name, nutrients in foods.items():
                    # Don't add if we're significantly over total calorie target
                    if current_nutrition['calories'] >= total_target_calories * 1.15:  # Allow 15% overage
                        break
                    
                    # Calculate portion based on the PRIMARY macro for this category
                    if category == 'proteins' and nutrients['protein'] > 0:
                        # For proteins, target protein content first
                        target_protein_from_food = category_target_protein / len(foods)
                        target_portion = (target_protein_from_food / nutrients['protein']) * 100
                    elif category == 'carbs' and nutrients['carbs'] > 0:
                        # For carbs, target carb content first
                        target_carbs_from_food = category_target_carbs / len(foods)
                        target_portion = (target_carbs_from_food / nutrients['carbs']) * 100
                    elif category == 'fats' and nutrients['fat'] > 0:
                        # For fats, target fat content first
                        target_fat_from_food = category_target_fat / len(foods)
                        target_portion = (target_fat_from_food / nutrients['fat']) * 100
                    else:
                        # For other categories, use calorie-based calculation
                        if nutrients['calories'] > 0:
                            target_portion = (target_per_food / nutrients['calories']) * 100
                        else:
                            target_portion = 50  # fallback
                    
                    # Add buffer to ensure we hit targets
                    target_portion *= 1.2  # 20% buffer to better hit targets
                    
                    # Apply minimum and maximum portion constraints
                    min_portion = 40   # minimum 40g
                    max_portion = 400  # maximum 400g
                    
                    # Adjust limits for specific food types
                    if 'egg' in name.lower():
                        min_portion = 50   # 1 egg minimum
                        max_portion = 300  # 6 eggs maximum
                    elif 'protein' in name.lower() and 'whey' in name.lower():
                        min_portion = 30   # minimum 30g scoop
                        max_portion = 90   # maximum 90g (3 scoops)
                    elif 'oil' in name.lower():
                        min_portion = 10   # 2 tsp minimum
                        max_portion = 35   # 7 tsp maximum
                    elif any(veg in name.lower() for veg in ['spinach', 'lettuce', 'broccoli', 'cucumber']):
                        min_portion = 60   # vegetables can be larger
                        max_portion = 250
                    elif any(carb in name.lower() for carb in ['rice', 'pasta', 'potato', 'bread', 'oats']):
                        min_portion = 50   # carbs need decent portions
                        max_portion = 350  # allow large carb servings
                    
                    # Constrain portion to limits
                    portion = max(min_portion, min(target_portion, max_portion))
                    
                    # Determine appropriate unit and conversion factor
                    unit = 'g'
                    conversion_factor = 1
                    
                    # Handle special cases
                    if 'egg' in name.lower():
                        unit = 'piece'
                        conversion_factor = 50  # 50g per egg
                        portion = max(50, round(portion / 50) * 50)  # Round to whole eggs
                    elif 'protein' in name.lower() and 'whey' in name.lower():
                        unit = 'scoop'
                        conversion_factor = 30  # 30g per scoop
                        portion = max(25, round(portion / 25) * 25)  # Round to quarter scoops
                    elif 'bread' in name.lower():
                        unit = 'slice'
                        conversion_factor = 30  # 30g per slice
                        portion = max(30, round(portion / 30) * 30)  # Round to whole slices
                    elif 'oil' in name.lower():
                        unit = 'tsp'
                        conversion_factor = 5  # 5g per teaspoon
                        portion = max(5, round(portion / 5) * 5)  # Round to whole teaspoons
                    else:
                        portion = round(portion / 5) * 5  # Round to nearest 5g
                    
                    # Calculate display quantity
                    display_quantity = portion / conversion_factor if conversion_factor > 1 else portion
                    
                    # Calculate scaled nutrition values
                    scale_factor = portion / 100
                    food_item = {
                        'name': name.replace('_', ' ').title(),
                        'quantity': round(display_quantity, 1),
                        'unit': unit,
                        'calories': round(nutrients['calories'] * scale_factor, 1),
                        'protein': round(nutrients['protein'] * scale_factor, 1),
                        'carbs': round(nutrients['carbs'] * scale_factor, 1),
                        'fat': round(nutrients['fat'] * scale_factor, 1)
                    }
                    
                    # Ensure no zero values in nutrition
                    for key in ['calories', 'protein', 'carbs', 'fat']:
                        if food_item[key] == 0 and nutrients[key] > 0:
                            food_item[key] = round(nutrients[key] * scale_factor, 1)
                        if food_item[key] == 0:
                            food_item[key] = 0.1  # Set minimum value to avoid zero
                    
                    # Add to meal
                    meal['foods'].append(food_item)
                    
                    # Update meal nutrition totals
                    meal['nutrition']['calories'] += food_item['calories']
                    meal['nutrition']['protein'] += food_item['protein']
                    meal['nutrition']['carbs'] += food_item['carbs']
                    meal['nutrition']['fat'] += food_item['fat']
                    
                    current_nutrition['calories'] += food_item['calories']
                    current_nutrition['protein'] += food_item['protein']
                    current_nutrition['carbs'] += food_item['carbs']
                    current_nutrition['fat'] += food_item['fat']
        
        # Post-generation macro adjustment: scale to better hit targets
        calorie_ratio = total_target_calories / meal['nutrition']['calories'] if meal['nutrition']['calories'] > 0 else 1
        protein_ratio = target_protein / meal['nutrition']['protein'] if meal['nutrition']['protein'] > 0 else 1
        fat_ratio = target_fat / meal['nutrition']['fat'] if meal['nutrition']['fat'] > 0 else 1
        
        # If any macro is significantly off (>10% difference), apply targeted scaling
        needs_scaling = (abs(1 - calorie_ratio) > 0.10 or 
                        abs(1 - protein_ratio) > 0.10 or 
                        abs(1 - fat_ratio) > 0.10)
        
        if needs_scaling and meal['nutrition']['calories'] > 0:
            # Prioritize calorie accuracy since that's the main target
            if abs(1 - calorie_ratio) > 0.10:
                scaling_factor = calorie_ratio
            else:
                # Use a weighted average favoring calories
                scaling_factor = (calorie_ratio * 0.6 + protein_ratio * 0.25 + fat_ratio * 0.15)
            
            # Limit scaling to reasonable bounds - be more aggressive
            scaling_factor = max(0.7, min(1.6, scaling_factor))
            
            print(f"Meal needs macro adjustment. Calorie ratio: {calorie_ratio:.2f}, Protein ratio: {protein_ratio:.2f}, Fat ratio: {fat_ratio:.2f}")
            print(f"Applying scaling factor: {scaling_factor:.2f}")
            
            # Scale all food portions proportionally
            for food_item in meal['foods']:
                food_item['calories'] = round(food_item['calories'] * scaling_factor, 1)
                food_item['protein'] = round(food_item['protein'] * scaling_factor, 1)
                food_item['carbs'] = round(food_item['carbs'] * scaling_factor, 1)
                food_item['fat'] = round(food_item['fat'] * scaling_factor, 1)
                food_item['quantity'] = round(food_item['quantity'] * scaling_factor, 1)
            
            # Recalculate meal nutrition totals
            meal['nutrition'] = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
            for food_item in meal['foods']:
                meal['nutrition']['calories'] += food_item['calories']
                meal['nutrition']['protein'] += food_item['protein']
                meal['nutrition']['carbs'] += food_item['carbs']
                meal['nutrition']['fat'] += food_item['fat']
        
        return meal

    def generate_daily_plan(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a full day's meal plan using ML models"""
        daily_calories = user_data['daily_calories']
        daily_macros = user_data['daily_macros']

        # Define meal schedule based on goal and protein distribution
        if user_data.get('goal') == 'muscle_gain':
            meal_schedule = {
                'breakfast': {'time': '07:30', 'ratio': 0.22},
                'morning_snack': {'time': '10:00', 'ratio': 0.13},
                'lunch': {'time': '13:00', 'ratio': 0.22},
                'afternoon_snack': {'time': '16:00', 'ratio': 0.13},
                'dinner': {'time': '19:00', 'ratio': 0.20}
            }
        elif user_data.get('goal') == 'weight_loss':
            meal_schedule = {
                'breakfast': {'time': '08:00', 'ratio': 0.25},
                'morning_snack': {'time': '10:00', 'ratio': 0.13},
                'lunch': {'time': '13:00', 'ratio': 0.30},
                'afternoon_snack': {'time': '16:00', 'ratio': 0.10},
                'dinner': {'time': '19:00', 'ratio': 0.25}
            }
        else:  # maintenance
            meal_schedule = {
                'breakfast': {'time': '08:00', 'ratio': 0.22},
                'morning_snack': {'time': '10:00', 'ratio': 0.13},
                'lunch': {'time': '13:00', 'ratio': 0.33},
                'afternoon_snack': {'time': '16:00', 'ratio': 0.13},
                'dinner': {'time': '19:00', 'ratio': 0.22}
            }

        # Generate meals
        daily_plan = {
            'meals': {},
            'total_nutrition': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0},
            'targets': {
                'calories': daily_calories,
                'protein': daily_macros['protein'],
                'carbs': daily_macros['carbs'],
                'fat': daily_macros['fat']
            }
        }

        for meal_name, details in meal_schedule.items():
            # Get meal composition using ML model - normalize meal names
            normalized_meal_name = meal_name
            if 'snack' in meal_name:
                normalized_meal_name = 'snack'
            
            meal_composition = self.predict_meal_composition(normalized_meal_name, user_data)
            
            # Add meal type and targets to preferences
            meal_preferences = {
                **user_data,
                'meal_type': normalized_meal_name,
                'meal_composition': meal_composition,
                'target_calories': daily_calories * details['ratio'],
                'target_protein': daily_macros['protein'] * details['ratio'],
                'target_carbs': daily_macros['carbs'] * details['ratio'],
                'target_fat': daily_macros['fat'] * details['ratio']
            }
            
            generated_meal = self.generate_meal(meal_preferences['target_calories'], meal_preferences)
            
            # Add timing information with proper display names
            if meal_name == 'morning_snack':
                display_name = 'Morning Snack'
            elif meal_name == 'afternoon_snack':
                display_name = 'Afternoon Snack'
            else:
                display_name = meal_name.replace('_', ' ').title()
            
            daily_plan['meals'][meal_name] = {
                **generated_meal,
                'time': details['time'],
                'type': display_name,
                'target_calories': meal_preferences['target_calories'],
                'target_protein': meal_preferences['target_protein'],
                'target_carbs': meal_preferences['target_carbs'],
                'target_fat': meal_preferences['target_fat']
            }

            # Add to daily totals
            for key in daily_plan['total_nutrition']:
                daily_plan['total_nutrition'][key] += generated_meal['nutrition'][key]

        # Final daily-level adjustment to ensure we hit calorie targets
        actual_calories = daily_plan['total_nutrition']['calories']
        target_calories = daily_plan['targets']['calories']
        calorie_accuracy = actual_calories / target_calories if target_calories > 0 else 1
        
        # If we're significantly off target (>10%), scale all meals proportionally
        if abs(1 - calorie_accuracy) > 0.10:
            scaling_factor = target_calories / actual_calories
            scaling_factor = max(0.8, min(1.3, scaling_factor))  # Limit scaling
            
            print(f"Daily plan calorie adjustment needed: {actual_calories:.0f}/{target_calories:.0f} ({calorie_accuracy:.1%})")
            print(f"Applying daily scaling factor: {scaling_factor:.2f}")
            
            # Scale all meals in the day
            for meal_name, meal_data in daily_plan['meals'].items():
                # Scale nutrition values
                for nutrient in ['calories', 'protein', 'carbs', 'fat']:
                    meal_data['nutrition'][nutrient] *= scaling_factor
                
                # Scale individual food items
                for food_item in meal_data['foods']:
                    for nutrient in ['calories', 'protein', 'carbs', 'fat']:
                        food_item[nutrient] = round(food_item[nutrient] * scaling_factor, 1)
                    food_item['quantity'] = round(food_item['quantity'] * scaling_factor, 1)
            
            # Recalculate daily totals
            daily_plan['total_nutrition'] = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
            for meal_data in daily_plan['meals'].values():
                for key in daily_plan['total_nutrition']:
                    daily_plan['total_nutrition'][key] += meal_data['nutrition'][key]

        return daily_plan

    def generate_meal_plan(self, user_data: Dict[str, Any], duration_days: int = 7) -> Dict[str, Any]:
        """Generate a complete meal plan based on user profile and preferences using ML models"""
        print(f"\n=== Generating Meal Plan ===")
        print(f"User Data: Weight={user_data.get('weight')}kg, Height={user_data.get('height')}cm, Age={user_data.get('age')}, Gender={user_data.get('gender')}")
        print(f"Activity Level: {user_data.get('activity_level')}, Goal: {user_data.get('goal')}")
        
        # Filter foods based on preferences first
        self.filter_foods_by_preferences(user_data)
        print(f"Applied dietary filters: vegetarian={user_data.get('vegetarian')}, vegan={user_data.get('vegan')}, allergies={user_data.get('allergies', [])}")
        
        # Calculate daily caloric needs using ML model
        daily_calories = self.predict_calories(user_data)
        print(f"Calculated daily calories: {daily_calories:.0f}")
        
        # Calculate macros using ML model
        daily_macros = self.predict_macros(daily_calories, user_data)
        print(f"Calculated macros: Protein={daily_macros['protein']:.0f}g, Carbs={daily_macros['carbs']:.0f}g, Fat={daily_macros['fat']:.0f}g")

        meal_plan = {
            'user_data': user_data,
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=duration_days-1)).strftime('%Y-%m-%d'),
            'daily_plans': {},
            'weekly_totals': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0},
            'targets': {
                'calories': daily_calories,
                'protein': daily_macros['protein'],
                'carbs': daily_macros['carbs'],
                'fat': daily_macros['fat']
            }
        }

        # Generate plans for each day
        for day in range(duration_days):
            date = (datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d')
            daily_plan = self.generate_daily_plan({
                **user_data,
                'daily_calories': daily_calories,
                'daily_macros': daily_macros
            })
            meal_plan['daily_plans'][date] = daily_plan

            # Add to weekly totals
            for key in meal_plan['weekly_totals']:
                meal_plan['weekly_totals'][key] += daily_plan['total_nutrition'][key]

        # Calculate averages
        for key in meal_plan['weekly_totals']:
            meal_plan['weekly_totals'][key] = round(meal_plan['weekly_totals'][key] / duration_days, 1)

        return meal_plan

    def _select_foods_for_meal(self, meal_type: str, meal_composition: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
        """Select appropriate foods for a meal based on type and composition"""
        selected_foods = {
            'proteins': {},
            'carbs': {},
            'fats': {},
            'vegetables': {},
            'fruits': {},
            'dairy': {}
        }
        
        # Define food groups for different meal types
        meal_foods = {
            'breakfast': {
                'proteins': ['eggs', 'egg_whites', 'greek_yogurt', 'whey_protein', 'cottage_cheese'],
                'carbs': ['oats', 'whole_wheat_bread', 'ezekiel_bread', 'granola', 'muesli'],
                'fats': ['almond_butter', 'peanut_butter', 'avocado'],
                'fruits': ['banana', 'apple', 'berries', 'orange'],
                'dairy': ['milk', 'yogurt']
            },
            'lunch': {
                'proteins': ['chicken_breast', 'salmon', 'lean_beef', 'tofu', 'tempeh', 'cod', 'turkey_breast'],
                'carbs': ['brown_rice', 'quinoa', 'sweet_potato', 'whole_wheat_pasta', 'basmati_rice'],
                'fats': ['olive_oil', 'avocado', 'nuts'],
                'vegetables': ['broccoli', 'spinach', 'kale', 'mixed_greens', 'bell_peppers']
            },
            'dinner': {
                'proteins': ['chicken_breast', 'salmon', 'lean_beef', 'tofu', 'tempeh', 'cod', 'turkey_breast'],
                'carbs': ['brown_rice', 'quinoa', 'sweet_potato', 'whole_wheat_pasta', 'basmati_rice'],
                'fats': ['olive_oil', 'avocado', 'nuts'],
                'vegetables': ['broccoli', 'asparagus', 'green_beans', 'brussels_sprouts', 'cauliflower']
            },
            'snack': {
                'proteins': ['whey_protein', 'greek_yogurt', 'cottage_cheese'],
                'carbs': ['granola', 'muesli', 'ezekiel_bread', 'fruit'],
                'fats': ['nuts', 'seeds', 'nut_butter'],
                'fruits': ['apple', 'banana', 'berries']
            }
        }
        
        # Get appropriate food groups for meal type
        meal_type_lower = meal_type.lower()
        if 'snack' in meal_type_lower:
            meal_type_lower = 'snack'
        food_groups = meal_foods.get(meal_type_lower, meal_foods['snack'])
        
        # Select foods based on composition (more conservative)
        for category, ratio in meal_composition.items():
            if ratio > 0.05 and category in food_groups:  # Only include if ratio > 5%
                available_foods = {
                    k: v for k, v in self.food_database.get(category, {}).items()
                    if k in food_groups[category]
                }
                
                # Select fewer items - usually just 1 item per category
                if ratio > 0.4:
                    num_items = 2  # Only for dominant categories
                elif ratio > 0.15:
                    num_items = 1  # Standard selection
                else:
                    num_items = 1 if ratio > 0.08 else 0  # Small portions or skip
                
                if available_foods and num_items > 0:
                    selected = random.sample(list(available_foods.items()),
                                          min(num_items, len(available_foods)))
                    selected_foods[category].update(dict(selected))
        
        return selected_foods 