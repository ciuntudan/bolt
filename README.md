# CNTApp - AI-Powered Nutrition and Training App

## Development Setup

### Model Files
The application uses machine learning models for meal plan generation. These files are not included in the repository due to their size. You have two options:

1. Train the models locally:
```bash
cd backend/users
python train_models.py
```
This will generate the following model files in `backend/users/models/`:
- calorie_model.joblib
- macro_model.joblib
- meal_composition_model.joblib
- meal_timing_model.joblib

2. Use rule-based fallback:
The application will automatically fall back to traditional calculation methods if model files are not present. This includes:
- TDEE calculation for calories
- Standard macro ratios based on goals
- Default meal compositions

### Installation
1. Clone the repository
2. Install frontend dependencies:
```bash
npm install
```
3. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### Running the Application
1. Start the backend server:
```bash
cd backend
python manage.py runserver
```

2. Start the frontend development server:
```bash
npm start
``` 