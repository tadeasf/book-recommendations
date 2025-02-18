from typing import List, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai
import os
from dotenv import load_dotenv
from ..models.Book import Book

class BookRecommender:
    def __init__(self):
        load_dotenv()
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = None
        self.openai_client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        
    def _update_tfidf(self, books: List[Book]) -> None:
        """Update TF-IDF matrix with current books."""
        descriptions = [f"{book.title} {book.description} {' '.join(book.genres)}" 
                       for book in books]
        self.tfidf_matrix = self.tfidf.fit_transform(descriptions)
        
    def get_traditional_recommendations(self, books: List[Book], book_index: int, n: int = 5) -> List[Book]:
        """Get recommendations using TF-IDF and cosine similarity."""
        if not books or book_index >= len(books):
            return []
            
        self._update_tfidf(books)
        similarities = cosine_similarity(self.tfidf_matrix[book_index:book_index+1], 
                                      self.tfidf_matrix).flatten()
        similar_indices = np.argsort(similarities)[::-1][1:n+1]
        return [books[i] for i in similar_indices]
        
    async def get_ai_enhanced_recommendations(self, book: Book, n: int = 5) -> List[str]:
        """Get AI-enhanced recommendations using OpenAI."""
        prompt = f"""Based on the book:
        Title: {book.title}
        Author: {book.author}
        Description: {book.description}
        Genres: {', '.join(book.genres)}
        
        Please recommend {n} similar books that readers might enjoy. 
        Focus on thematic similarities, writing style, and genre elements.
        Format as a simple list with title and author only."""
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable book recommendation expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip().split("\n")
