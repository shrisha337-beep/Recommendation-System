# 🎬 CineMatch | NLP-Powered Content-Based Movie Recommendation System

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey.svg)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg)
![Deployment](https://img.shields.io/badge/Deployment-Render-brightgreen.svg)

> Built and deployed an NLP-powered movie recommendation engine using content-based filtering, processing 4,800+ movies and generating real-time recommendations through a Flask REST API integrated with OMDB.

---

## 📌 Overview

CineMatch is an NLP-powered content-based movie recommendation system that recommends movies based on their content rather than user watch history. By analyzing movie overviews, genres, keywords, cast members, and directors, the system identifies similar movies and provides highly relevant recommendations.

The recommendation engine leverages Natural Language Processing (NLP), Bag-of-Words vectorization, and Cosine Similarity to process over 4,800 movies and generate recommendations in real time through a Flask-powered web application.

🌐 **Live Demo:** YOUR_RENDER_URL_HERE

---

## ✨ Features

* 🎥 Content-Based Movie Recommendation Engine
* 🧠 NLP-Powered Similarity Analysis
* ⚡ Instant Top-5 Movie Recommendations
* 🖼️ Real-Time Movie Poster Retrieval using OMDB API
* 🌙 Responsive Cinematic User Interface
* 🔄 Flask REST API Backend
* ☁️ Render Deployment
* 📱 Mobile-Friendly Design

---

## 📸 Screenshots

### Home Page

![Home Page](screenshots/home-page.png)

### Recommendations

![Recommendations](screenshots/recommendations-page.png)

---

## 🧠 Machine Learning Pipeline

### 1. Data Preprocessing & Feature Engineering

The TMDB 5000 Movies Dataset was cleaned and transformed by extracting key features:

* Movie Title
* Overview
* Genres
* Keywords
* Top 3 Cast Members
* Director

These features were merged into a unified metadata field called `tags`, representing each movie's content profile.

---

### 2. Natural Language Processing (NLP)

#### Text Normalization

* Converted text to lowercase
* Removed inconsistencies across metadata

#### Stemming

Implemented using NLTK's Porter Stemmer.

Example:

```text
acting, actor, acted → act
```

This reduces redundant vocabulary and improves feature representation.

---

### 3. Feature Extraction

#### Bag of Words Vectorization

Implemented using Scikit-Learn's CountVectorizer.

```python
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(
    max_features=5000,
    stop_words='english'
)
```

Each movie is transformed into a vector in a 5000-dimensional feature space.

---

### 4. Recommendation Algorithm

#### Cosine Similarity

The recommendation engine measures similarity using cosine similarity.

```text
Cosine Similarity = (A · B) / (||A|| × ||B||)
```

Interpretation:

* 1.0 → Highly Similar
* 0.0 → Completely Different

The system generates a similarity matrix of approximately:

```text
4806 × 4806
```

allowing fast retrieval of the most similar movies.

---

## 📊 Model Statistics

| Metric                | Value                   |
| --------------------- | ----------------------- |
| Movies Processed      | 4,806                   |
| Vocabulary Size       | 5,000 Features          |
| Similarity Matrix     | 4,806 × 4,806           |
| Recommendation Type   | Content-Based Filtering |
| Average Response Time | < 1 Second              |

---

## 🛠️ Tech Stack

### Machine Learning & Data Science

* Python
* Pandas
* NumPy
* Scikit-Learn
* NLTK

### Backend

* Flask
* Gunicorn
* Requests

### Frontend

* HTML5
* CSS3
* JavaScript
* Tailwind CSS

### Deployment

* Render
* GitHub
* Git LFS

---

## 🔌 API Documentation

### Recommendation Endpoint

```http
POST /api/recommend
```

### Request

```json
{
    "movie": "Avatar"
}
```

### Response

```json
{
    "recommendations": [
        {
            "title": "John Carter",
            "poster": "poster_url"
        },
        {
            "title": "Guardians of the Galaxy",
            "poster": "poster_url"
        }
    ]
}
```

---

## 📂 Project Structure

```text
Movie-Recommendation-System/
│
├── app.py
├── movie_dict.pkl
├── similarity.pkl
├── requirements.txt
├── Procfile
├── runtime.txt
│
├── templates/
│   └── index.html
│
├── Movie REcommendation System.ipynb
│   
│
└── README.md
```

---

## 📊 Dataset

**TMDB 5000 Movies Dataset**

Source:

https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

The dataset contains:

* Movie Metadata
* Genres
* Keywords
* Cast Information
* Crew Information
* Movie Overviews

---

## ⚙️ Local Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Movie-Recommendation-System.git

cd Movie-Recommendation-System
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
OMDB_API_KEY
```

Get a free API key from:

https://www.omdbapi.com/apikey.aspx

### 5. Run the Application

```bash
python app.py
```

Visit:

```text
(https://recommendation-system-1-gjc3.onrender.com)
```

---

## 🚀 Deployment

The application is deployed on Render using:

* Flask
* Gunicorn
* GitHub Integration

Start Command:

```bash
gunicorn app:app
```

---

## 🔮 Future Enhancements

* Hybrid Recommendation System
* Collaborative Filtering Integration
* User Authentication
* Personalized Recommendations
* Watchlist Functionality
* Movie Trailer Integration
* Sentiment Analysis of Reviews
* Genre-Based Filtering
* Recommendation Explanation Engine

---

## 👩‍💻 Author

**Shrisha**

Computer Science Engineering Student
Ajay Kumar Garg Engineering College (AKGEC)

### Connect With Me

* GitHub: https://github.com/shrisha337-beep
* LinkedIn: YOUR_LINKEDIN_URL

---

## 📄 License

This project is licensed under the MIT License.
