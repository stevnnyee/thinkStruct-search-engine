import numpy as np
import pandas as pd
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import PatentDataLoader

class BasicPatentSearchEngine:
    def __init__(self, patents_df: pd.DataFrame):
        self.patents_df = patents_df.copy()
        self.vectorizer = None
        self.patent_vectors = None
        self.is_indexed = False
        
    def preprocess_text(self, text) -> str:
        """Simple text cleaning"""
        try:
            # Handle pandas Series
            if hasattr(text, 'iloc'):
                if len(text) == 0:
                    return ""
                text = text.iloc[0]
            
            # Handle None/NaN
            if text is None or (hasattr(text, 'isna') and text.isna()):
                return ""
            
            # If text is a list (like claims), join it
            if isinstance(text, list):
                text = " ".join(str(item) for item in text if item)
            
            text = str(text).lower()
            text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
            return text.strip()
        except:
            return ""
    
    def build_index(self, text_field: str = 'claims'):
        """Build TF-IDF index"""
        print(f"Building index from '{text_field}' field...")
        
        # Extract text
        texts = [self.preprocess_text(text) for text in self.patents_df[text_field]]
        
        # Create TF-IDF vectors
        self.vectorizer = TfidfVectorizer(
            max_features=3000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        
        self.patent_vectors = self.vectorizer.fit_transform(texts)
        self.text_field = text_field
        self.is_indexed = True
        
        print(f"Indexed {len(texts)} patents")
        
    def find_similar_patents(self, patent_id: str, top_k: int = 5) -> List[Dict]:
        """Find similar patents (conflict detection)"""
        if not self.is_indexed:
            self.build_index()
        
        # Find reference patent
        ref_patent = self.patents_df[self.patents_df['doc_number'] == patent_id]
        if ref_patent.empty:
            return [{"error": f"Patent {patent_id} not found"}]
        
        # Get similarity scores
        ref_text = self.preprocess_text(ref_patent.iloc[0][self.text_field])
        query_vector = self.vectorizer.transform([ref_text])
        similarities = cosine_similarity(query_vector, self.patent_vectors)[0]
        
        # Get top similar patents (excluding self)
        results = []
        top_indices = np.argsort(similarities)[::-1]
        
        for idx in top_indices:
            if len(results) >= top_k:
                break
                
            patent = self.patents_df.iloc[idx]
            score = similarities[idx]
            
            # Skip self
            if patent['doc_number'] == patent_id:
                continue
                
            # Risk assessment
            if score > 0.7:
                risk = "HIGH"
            elif score > 0.4:
                risk = "MEDIUM"
            else:
                risk = "LOW"
            
            results.append({
                'patent_id': patent['doc_number'],
                'title': patent.get('title', 'No Title'),
                'similarity_score': float(score),
                'risk_level': risk
            })
        
        return results
    
    def search_text(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search by text query"""
        if not self.is_indexed:
            self.build_index()
        
        # Get similarities
        processed_query = self.preprocess_text(query)
        query_vector = self.vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vector, self.patent_vectors)[0]
        
        # Get top results
        results = []
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        for idx in top_indices:
            patent = self.patents_df.iloc[idx]
            score = similarities[idx]
            
            results.append({
                'patent_id': patent['doc_number'],
                'title': patent.get('title', 'No Title'),
                'similarity_score': float(score),
                'risk_level': "HIGH" if score > 0.7 else "MEDIUM" if score > 0.4 else "LOW"
            })
        
        return results

    def hybrid_search(self, query: str, classification_filter: str = None, 
                     title_keywords: str = None, specific_title: str = None, 
                     top_k: int = 5) -> List[Dict]:
        """
        Hybrid search with filters:
        - query: semantic search query
        - classification_filter: filter by classification code (e.g., "B60B")
        - title_keywords: keywords that must appear in title
        - specific_title: exact title to search for
        """
        import time
        start_time = time.time()
        
        # Step 1: Get semantic search results
        semantic_results = self.search_text(query, top_k=top_k*3)  # Get more candidates
        
        # Step 2: Apply filters
        filtered_results = []
        
        for result in semantic_results:
            patent_id = result['patent_id']
            patent_data = self.patents_df[self.patents_df['doc_number'] == patent_id].iloc[0]
            
            # Filter by classification
            if classification_filter:
                classification = str(patent_data.get('classification', ''))
                if not classification.startswith(classification_filter):
                    continue
            
            # Filter by title keywords
            if title_keywords:
                title = str(patent_data.get('title', '')).lower()
                keywords = title_keywords.lower().split()
                if not all(keyword in title for keyword in keywords):
                    continue
            
            # Filter by specific title
            if specific_title:
                title = str(patent_data.get('title', '')).lower()
                if specific_title.lower() not in title:
                    continue
            
            filtered_results.append(result)
            
            # Stop if we have enough results
            if len(filtered_results) >= top_k:
                break
        
        end_time = time.time()
        search_time = end_time - start_time
        
        # Add timing info to first result
        if filtered_results:
            filtered_results[0]['search_time_ms'] = round(search_time * 1000, 2)
        
        return filtered_results

def demo_search_engine():
    """Simple demo for presentation"""
    # Load data
    print("Loading patent database...")
    loader = PatentDataLoader()
    patents = loader.load_all_patents()
    df = loader.patents_to_dataframe(patents)
    
    # Initialize engine
    engine = BasicPatentSearchEngine(df)
    
    print(f"Database: {len(df)} patents loaded")
    
    # Demo 1: Text search
    print(f"\nDemo 1: Text Search")
    query = "wireless vehicle sensor"
    results = engine.search_text(query, top_k=3)
    
    print(f"Query: '{query}'")
    for result in results:
        print(f"  {result['risk_level']}: {result['patent_id']} ({result['similarity_score']:.3f})")
        print(f"       {result['title'][:60]}...")
    
    # Demo 2: Patent similarity
    print(f"\nDemo 2: Patent Conflict Detection")
    sample_patent = df.iloc[0]['doc_number']
    similar = engine.find_similar_patents(sample_patent, top_k=3)
    
    print(f"Analyzing: {sample_patent}")
    for result in similar:
        if 'error' not in result:
            print(f"  {result['risk_level']}: {result['patent_id']} ({result['similarity_score']:.3f})")
    
    # Demo 3: Hybrid search
    print(f"\nDemo 3: Hybrid Search")
    print("Query: 'sensor' + classification starts with 'B60'")
    hybrid_results = engine.hybrid_search(
        query="sensor", 
        classification_filter="B60", 
        top_k=3
    )
    
    for result in hybrid_results:
        print(f"  {result['risk_level']}: {result['patent_id']} ({result['similarity_score']:.3f})")
        print(f"       {result['title'][:60]}...")
    
    if hybrid_results:
        print(f"Search time: {hybrid_results[0].get('search_time_ms', 0)}ms")

if __name__ == "__main__":
    demo_search_engine()