#!/usr/bin/env python3
"""
Simple tests for the patent search engine.
Tests the core functionality as specified in the project guidelines.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import PatentDataLoader
from src.search_engine import BasicPatentSearchEngine

def test_data_loading():
    """Test 1: Verify data loading works"""
    print("Test 1: Data Loading")
    
    loader = PatentDataLoader()
    patents = loader.load_all_patents()
    df = loader.patents_to_dataframe(patents)
    
    assert len(df) > 0, "No patents loaded"
    assert 'claims' in df.columns, "Claims column missing"
    assert 'title' in df.columns, "Title column missing"
    
    print(f"Loaded {len(df)} patents successfully")
    print(f"Found columns: {list(df.columns)}")
    return df

def test_search_functionality():
    """Test 2: Verify search works with text query"""
    print("\nTest 2: Text Search")
    
    # Load data
    loader = PatentDataLoader()
    patents = loader.load_all_patents()
    df = loader.patents_to_dataframe(patents)
    
    # Initialize engine
    engine = BasicPatentSearchEngine(df)
    
    # Test text search
    query = "vehicle sensor"
    results = engine.search_text(query, top_k=3)
    
    assert len(results) > 0, "No search results returned"
    assert all('patent_id' in result for result in results), "Missing patent_id in results"
    assert all('risk_level' in result for result in results), "Missing risk_level in results"
    
    print(f"Search query: '{query}'")
    print(f"Found {len(results)} results")
    for result in results:
        print(f"  {result['risk_level']}: {result['patent_id']} ({result['similarity_score']:.3f})")
    
    return results

def test_patent_similarity():
    """Test 3: Verify patent similarity works"""
    print("\nTest 3: Patent Similarity")
    
    # Load data
    loader = PatentDataLoader()
    patents = loader.load_all_patents()
    df = loader.patents_to_dataframe(patents)
    
    # Initialize engine
    engine = BasicPatentSearchEngine(df)
    
    # Get a sample patent ID
    sample_patent_id = df.iloc[0]['doc_number']
    
    # Test patent similarity
    similar_patents = engine.find_similar_patents(sample_patent_id, top_k=3)
    
    assert len(similar_patents) > 0, "No similar patents found"
    assert all('patent_id' in result for result in similar_patents), "Missing patent_id in results"
    assert all('risk_level' in result for result in similar_patents), "Missing risk_level in results"
    
    print(f"Analyzing patent: {sample_patent_id}")
    print(f"Found {len(similar_patents)} similar patents")
    for result in similar_patents:
        if 'error' not in result:
            print(f"  {result['risk_level']}: {result['patent_id']} ({result['similarity_score']:.3f})")
    
    return similar_patents

def run_all_tests():
    """Run all tests and report results"""
    print("Patent Search Engine - Tests")
    
    try:
        # Test 1: Data loading
        df = test_data_loading()
        
        # Test 2: Text search
        search_results = test_search_functionality()
        
        # Test 3: Patent similarity
        similarity_results = test_patent_similarity()
        
        print("\nALL TESTS PASSED")
        print("Data loading works")
        print("Text search works") 
        print("Patent similarity works")
        print("Search engine follows project guidelines")
        
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 