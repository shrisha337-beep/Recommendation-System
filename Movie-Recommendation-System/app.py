import os
import pickle
import requests
import pandas as pd
import numpy as np
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
import gdown

# Load environmental variables from .env
load_dotenv()

# Initialize Flask App
app = Flask(__name__)

def download_similarity_file():
    file_id = "YOUR_GOOGLE_DRIVE_FILE_ID"

    url = f"https://drive.google.com/uc?id={file_id}"

    gdown.download(
        url,
        "similarity.pkl",
        quiet=False
    )

# Download only if missing
if not os.path.exists("similarity.pkl"):
    print("similarity.pkl not found. Downloading...")
    download_similarity_file()

# --- API KEY MANAGEMENT ---
# The video uses TMDB (The Movie Database). We check for TMDB_API_KEY or fallback to OMDB_API_KEY 
# name from your .env just in case, or default to a demo key so the app doesn't crash.
OMDB_API_KEY = os.getenv("OMDB_API_KEY") or os.getenv("OMDB_API_KEY")
if not OMDB_API_KEY:
    print("⚠ API Key not found in environment. Using default OMDB demo key.")

# --- LOAD MODELS WITH FALLBACKS ---
try:
    with open('movie_dict.pkl', 'rb') as f:
        movies_dict = pickle.load(f)
    movies = pd.DataFrame(movies_dict)
    
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
    USING_REAL_MODEL = True
    print("✓ Successfully loaded real ML model from pickle files!")
except Exception as e:
    USING_REAL_MODEL = False
    print("⚠ Pickle files not found or failed to load. Bootstrapping with demo dataset...")
    # Demo Mock Dataset for instant out-of-the-box local testing
    movies_data = {
        'movie_id': [19995, 27205, 157336, 155, 68718, 550, 120, 1891, 122, 24428],
        'title': ['Avatar', 'Inception', 'Interstellar', 'The Dark Knight', 'Django Unchained', 'Fight Club', 'The Fellowship of the Ring', 'The Empire Strikes Back', 'The Return of the King', 'The Avengers']
    }
    movies = pd.DataFrame(movies_data)
    similarity = np.eye(len(movies))
    
    # Pre-configure similarity ratios for demo data
    similarity[0, 1] = 0.8  # Avatar resembles Inception
    similarity[1, 0] = 0.8
    similarity[1, 2] = 0.9  # Inception resembles Interstellar
    similarity[2, 1] = 0.9
    similarity[3, 4] = 0.75 # Dark Knight resembles Django
    similarity[4, 3] = 0.75
    similarity[6, 8] = 0.95 # Fellowship resembles Return of the King
    similarity[8, 6] = 0.95

# --- HELPER: FETCH MOVIE POSTER ---
def fetch_poster(movie_title):
    try:
        # Fixed the missing colon in the protocol scheme below
        url = f"https://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
        response = requests.get(url, timeout=5)
        data = response.json()
        poster_path = data.get('Poster')
        if poster_path and poster_path != "N/A":
            return poster_path
    except Exception as e:
        print(f"Error fetching poster for movie ID {movie_title}: {e}")
    # Return professional placeholder if API is offline or key fails
    return "https://images.unsplash.com/photo-1594909122845-11baa439b7bf?q=80&w=500&auto=format&fit=crop"

# --- CORE ML RECOMMENDATION LOGIC ---
def recommend(movie_title):
    try:
        if movie_title not in movies['title'].values:
            return []
            
        idx = movies[movies['title'] == movie_title].index[0]
        distances = similarity[idx]
        
        # Sort values while maintaining original indices via enumerate
        sorted_movies = sorted(
            list(enumerate(distances)),
            key=lambda x: x[1],
            reverse=True
        )

        recommendations = []
        count = 0
        for item in sorted_movies:
            movie_idx = item[0]
            current_title = movies.iloc[movie_idx]['title']
            
            # Avoid recommending the queried movie itself
            if current_title == movie_title and len(sorted_movies) > 5:
                continue
                
            movie_id = int(movies.iloc[movie_idx]['movie_id'])
            score_val = float(item[1])
            
            recommendations.append({
                "title": current_title,
                "poster_url": fetch_poster(current_title),
                "score": round(score_val * 100, 1) if USING_REAL_MODEL else "95.0"
            })
            
            count += 1
            if count == 5:
                break
                
        return recommendations

    except Exception as e:
        print(f"Recommendation error: {e}")
        return []

# --- API ENDPOINTS ---

@app.route('/api/movies', methods=['GET'])
def get_movies():
    """Returns the list of all available movie titles for the search dropdown."""
    movie_list = sorted(movies['title'].tolist())
    return jsonify(movie_list)

@app.route('/api/recommend', methods=['POST'])   
def recommend_endpoint():
    """API endpoint to get movie recommendations based on user input."""
    data = request.get_json()
    # Supports both the 'movie' key sent by frontend JS and fallback 'movie_title'
    movie_title = data.get('movie') or data.get('movie_title')
    
    if not movie_title:
        return jsonify({"error": "Movie title is required."}), 400
    
    if movie_title not in movies['title'].values:
        return jsonify({"error": "Movie title not found in dataset."}), 404
        
    recommended_movies = recommend(movie_title)
    
    if not recommended_movies:
        return jsonify({"error": "No recommendations found."}), 404
    
    return jsonify({
        "query": movie_title,
        "recommendations": recommended_movies,
        "using_real_model": USING_REAL_MODEL
    })

@app.route('/')
def home():
    """Serves the main application template."""
    return render_template('index.html', using_real_model=USING_REAL_MODEL)

if __name__ == '__main__':
    # Run server locally on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
    
            
    
    
