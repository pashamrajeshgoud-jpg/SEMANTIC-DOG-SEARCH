from typing import List, Tuple
import numpy as np

# TfidfVectorizer is used to convert text into numerical TF-IDF vectors
# cosine_similarity computes the similarity between two vectors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticIndex:
    """
    Indexes a collection of documents using TF-IDF and allows querying for similar documents.

    Attributes:
        docs (List[str]): A list of input documents.
        vectorizer (TfidfVectorizer): A fitted TF-IDF vectorizer used to convert text to vectors.
        embeddings (np.ndarray): The TF-IDF transformed representation of the documents.
    """
    def __init__(self, 
                 docs: List[str]) -> None:
        self.docs = docs
        self.vectorizer = TfidfVectorizer().fit(docs)
        
        # Transform the documents into TF-IDF vectors (sparse matrix)
        self.embeddings = self.vectorizer.transform(docs)

    def query(self, 
              q: str, 
              top_k: int = 5,
              threshold: int = 0.2) -> List[Tuple[int, float]]:
        # Transform the query string into a TF-IDF vector
        q_vec = self.vectorizer.transform([q])
        sims = cosine_similarity(q_vec, self.embeddings)[0]

        filtered = [(i, sims[i]) for i in range(len(sims)) if sims[i] >= threshold]
        
        if not filtered:
            return []  # No results if all are below threshold

        # Sort the documents by similarity score in descending order
        filtered.sort(key=lambda x: -x[1])
        return [(int(i), float(sim)) for i, sim in filtered[:top_k]]