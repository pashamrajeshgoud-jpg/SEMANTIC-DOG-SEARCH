# Semantic Dog Search System

## Overview

The Semantic Dog Search System is a web-based application designed to provide users with a semantic search experience for dog breeds using 3rd party api (https://docs.thedogapi.com/)

## Features

- **Semantic Search:** Utilizes TF-IDF vectorization and cosine similarity to match user queries with breed data.
- **Real-Time Data:** Fetches breed information and images from The Dog API.
- **Responsive UI:** Built with React JS and styled with Tailwind CSS for a seamless desktop and mobile experience.
- **Efficient Backend:** FastAPI in Python, with asynchronous processing for fast response times.

## Architecture
The system follows a modular architecture:
- **User Interface:** React JS application handling user input and displaying search results.
- **Backend Server:** FastAPI (Python) server with an integrated semantic layer for processing queries.
- Includes TF-IDF vectorization, cosine similarity search, and an in-memory breed cache built on startup.
- Features a `/search` endpoint and a query processor to augment results with images.
- **External API:** The Dog API provides breed data and images via a 3rd party REST API.

## Setup Instructions

### Prerequisites
- Python `3.8+`
- Node.js and npm
- API key for The Dog API (store in .env)

### Installation
1. Clone the Repository
```bash
git clone https://github.com/yourusername/semantic-dog-search.git
cd semantic-dog-search
```

2. Backend Setup

Create a virtual environment and activate it:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```


4. Create a .env file with your The Dog API key:
```
DOG_API_KEY=your_api_key_here
DOG_API_BASE=https://docs.thedogapi.com/
```


### Frontend Setup
1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Run the Application

Start the backend:
```
uvicorn main:app --reload
```


#### Start the frontend:
```
npm run dev
```


Access the app at `http://localhost:5173`


## Usage
- Enter a search query (e.g., "friendly dog"") in the UI.
- View the top matching breeds with names, temperaments, descriptions, life spans, bred-for details, and images.
- Results are ranked by semantic similarity and augmented with real-time data from The Dog API.