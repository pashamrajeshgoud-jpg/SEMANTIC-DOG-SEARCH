from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DOG_API_BASE = os.getenv("DOG_API_BASE", "https://api.thedogapi.com/v1")
DOG_API_KEY = os.getenv("DOG_API_KEY")
HEADERS = {"x-api-key": DOG_API_KEY} if DOG_API_KEY else {}

# Initialize FastAPI
app = FastAPI(title="Dog Search API", version="1.1")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

breed_cache = []
breed_index = None

from semantic import SemanticIndex

async def load_breeds():
    """
    Fetches all breeds from The Dog API and builds the semantic index.
    Includes name, temperament, and description fields.
    """
    global breed_cache, breed_index

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(f"{DOG_API_BASE}/breeds", headers=HEADERS)
        response.raise_for_status()
        breed_cache = response.json()

    # Build semantic documents from all relevant text fields
    docs = []
    for b in breed_cache:
        text = (
            f"Name: {b.get('name', '')}. "
            f"Temperament: {b.get('temperament', '')}. "
            f"Bred group: {b.get('breed_group', '')}. "
            f"Life span: {b.get('life_span', '')}. "
            f"Bred for: {b.get('bred_for', '')}. "
            f"Description: {b.get('description', '')}."
        )
        docs.append(text)
        
    breed_index = SemanticIndex(docs)
    print(f"✅ Loaded {len(breed_cache)} breeds into memory with semantic index.")


@app.on_event("startup")
async def startup_event():
    await load_breeds()

class SearchResult(BaseModel):
    id: int
    name: str
    temperament: Optional[str]
    description: Optional[str]
    life_span: Optional[str]
    bred_for: Optional[str]
    image: Optional[str]
    score: Optional[float]

@app.get("/search", response_model=List[SearchResult])
async def search(q: str):
    """
    Search breeds using semantic similarity and return enriched results.
    """
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")

    global breed_index

    ranked = breed_index.query(q, top_k=5)
    if not ranked:
        raise HTTPException(status_code=404, detail="No breeds found")

    results = []
    async with httpx.AsyncClient(timeout=15) as client:
        for idx, score in ranked:
            b = breed_cache[idx]
            breed_id = b.get("id")

            try:
                params = {"breed_id": breed_id, "limit": 1}
                r = await client.get(f"{DOG_API_BASE}/images/search", params=params, headers=HEADERS)
                r.raise_for_status()
                img_data = r.json()
                image_url = img_data[0]["url"] if img_data else None
            except Exception:
                image_url = None

            results.append(
                SearchResult(
                    id=breed_id,
                    name=b.get("name"),
                    temperament=b.get("temperament"),
                    description=b.get("description"),
                    life_span=b.get("life_span"),
                    bred_for=b.get("bred_for"),
                    image=image_url,
                    score=float(score),
                )
            )

    return results
