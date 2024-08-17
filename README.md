# Sogang AI MBA 2024 Summer Team Project

This project is kick scooter service.

## Project Structure
- `app.py`: Main backend script using Flask.
- `static/`: Contains static assets like images and stylesheets.
- `templates/`: Contains HTML templates for rendering web pages.
- `node_modules/`: Node.js dependencies (this is ignored in `.gitignore`).
- `favicon.ico`: Icons for the web application.
- `uploaded_image.jpg`: Example image used for testing.

## Installation

### Prerequisites
Ensure you have the following installed on your system:
- **Conda**: For managing Python environments.
- **Node.js and npm**: For frontend dependencies.

### How to run

#### 1. Clone the repository
```b
git clone git@github.com:yesjuhyeong/sogang_ai_mba_2024_summer_team_project.git
```

#### 2. Navigate to the project directory
```
cd sogang_ai_mba_2024_summer_team_project
```
#### 3. Create and activate a Conda environment
To manage dependencies cleanly, it’s recommended to create a new Conda environment with Python 3.8:

```
conda create -n kick_scooter python==3.8
conda activate kick_scooter
```

#### 4. Install Python dependencies

```
pip install -r requirements.txt
```
#### 5. Install Node.js dependencies
```
npm install
```

#### 6. Running the Application
Start the Flask application:
```
python app.py
```
By default, the app will run on http://localhost:5000.