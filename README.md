# Patent Search Engine

## Problem Statement

**The Core Challenge**: Patent attorneys and inventors spend weeks manually searching through thousands of patents to identify potential conflicts and prior art. This manual process is time-consuming, expensive, and prone to missing critical similarities that could lead to costly legal disputes.

**Specific Problem Solved**: Build an automated patent comparison system that can instantly identify similar patents and assess conflict risk levels. This directly supports ThinkStruct's mission of using advanced technology to improve patent law processes and make intellectual property analysis more efficient and accurate.

**Business Impact**: Transform patent conflict detection from a tedious manual process into a seconds-long automated analysis, enabling faster innovation cycles and reducing legal risks for inventors and companies.

## Data

### Dataset
- **Source**: 640 vehicle patent applications (2024-present)
- **Format**: JSON files named `patents_ipa{DATE}.json`
- **Fields**: Title, Document Number, Abstract, Detailed Description, Claims, Bibtex Citation, Classification Code
- **Domain**: Vehicle technology (sensors, safety systems, communication)

### Data Quality & Missing Field Strategy
**Choice Made**: EXCLUDE patents missing critical fields (title, abstract, claims)
**Rationale**: Ensures searchable text while maximizing dataset size
**Result**: 100% field coverage across 640 patents

```bash
# Verify data quality
python3 src/data_loader.py
# Output: Total patents loaded: 640, 100% field coverage
```

## Part 1: Basic Search Engine

### Design Decisions

**Inputs Chosen:**
- Natural language queries (e.g., "wireless vehicle sensor")
- Patent IDs for similarity analysis (e.g., "20240293901")

**Outputs Chosen:**
- Patent metadata (ID, title, similarity scores)
- Risk assessment (HIGH/MEDIUM/LOW conflict levels)
- Ranked similar patents

**Technical Approach:**
- **Claims-First**: Focus on legally binding patent claims
- **TF-IDF Vectorization**: Handles technical patent language effectively
- **Cosine Similarity**: Standard semantic similarity measurement
- **Risk Scoring**: >70% = High Risk, 40-70% = Medium Risk, <40% = Low Risk

### Implementation

```python
# Core search functionality
engine = BasicPatentSearchEngine(patents_df)

# Text search
results = engine.search_text("wireless vehicle sensor", top_k=5)

# Patent similarity (conflict detection)
similar = engine.find_similar_patents("20240293901", top_k=5)
```

### Performance
- **Speed**: Sub-second search across 640 patents
- **Accuracy**: Claims-focused analysis (most legally relevant)
- **Scalability**: Modular design for larger datasets

## Part 2: Enhancement - Hybrid Search

### Enhancement Selected: Hybrid Search

**Why Chosen**: Patent attorneys need precise filtering beyond semantic search

### Features Implemented

**1. Classification Code Constraints**
```python
# Filter by patent classification (e.g., vehicle wheels = B60B)
results = engine.hybrid_search(
    query="sensor", 
    classification_filter="B60B"
)
```

**2. Title Keyword Search**
```python
# Search for specific keywords in patent titles
results = engine.hybrid_search(
    query="sensor", 
    title_keywords="tire pressure"
)
```

**3. Specific Title Search**
```python
# Find patents with specific title content
results = engine.hybrid_search(
    query="sensor", 
    specific_title="TPMS"
)
```

### Performance Analysis

**Timing Results:**
- Hybrid search: ~1.84ms
- Regular search: ~0.5ms
- Overhead: ~1.34ms for filtering

**Efficiency Commentary:**
- **Current approach**: Semantic search first, then filter (efficient for small datasets)
- **Large-scale optimizations**: 
  - Pre-index classifications for O(1) lookup
  - Parallel filtering across multiple threads
  - Bloom filters for quick exclusion
  - Inverted indices for keyword matching

## How to Run Code

**Setup** (one-time):
```bash
pip install pandas numpy scikit-learn
```

**Run the Demo**:
```bash
python3 src/search_engine.py
```
This shows text search, patent similarity analysis, and hybrid search with timing.

**Run Tests**:
```bash
python3 tests/test_search_engine.py
```
Verifies all functionality works correctly with the patent data.

## Example Usage

### Basic Search
```bash
Query: 'wireless vehicle sensor'
Results:
  LOW: 20240391278 (0.199) - TWO-WAY TIRE PRESSURE MONITORING SYSTEM
  LOW: 20240278598 (0.193) - WHEEL HUB...
```

### Hybrid Search
```bash
Query: 'sensor' + classification 'B60'
Results:
  LOW: 20250083480 (0.352) - EXTERNAL TPMS SENSOR FOR HEAVY-DUTY TRUCKS
  LOW: 20240408920 (0.347) - SYSTEMS AND METHODS FOR TIRE TREADWEAR SENSING
Search time: 1.84ms
```

### Patent Conflict Detection
```bash
Analyzing: 20240293901
Similar patents:
  LOW: 20250128543 (0.211)
  LOW: 20240246364 (0.209)
```

## How Code Addresses Problem Statement

**Direct Patent Comparison**: The system compares any patent against the entire database to find similar inventions, exactly what patent attorneys need for conflict assessment.

**Technical Solution**:
1. **Claims-Focused Analysis**: Analyzes the legally binding claims section of patents (not just abstracts) to identify genuine conflicts
2. **Semantic Understanding**: Uses TF-IDF vectorization to understand technical patent language and find conceptual similarities beyond keyword matching
3. **Risk Assessment**: Automatically categorizes similarity levels (HIGH/MEDIUM/LOW) to guide legal decision-making
4. **Hybrid Search Enhancement**: Combines semantic search with precise metadata filtering (classification codes, title keywords) that patent professionals actually use in practice
5. **Speed**: Processes searches in milliseconds, making it practical for daily use in legal workflows

**Why Hybrid Search Enhancement**: Patent agents don't just want semantically similar patents - they need patents within specific classification codes (like B60B for vehicle wheels) or with particular keywords in titles. This enhancement bridges the gap between pure semantic search and the practical filtering needs of patent law professionals.

**Alignment with ThinkStruct's Mission**: This search engine demonstrates the core technology needed to modernize patent law - automated analysis that maintains legal precision while dramatically reducing time and cost. It shows how intelligent systems can augment human expertise in intellectual property analysis.

## Project Structure

```
thinkStruct-search-engine/
├── src/
│   ├── data_loader.py      # Data loading and validation
│   └── search_engine.py    # Core search + hybrid functionality
├── tests/
│   └── test_search_engine.py # Comprehensive tests
├── data/patent_data_small/ # 640 vehicle patents
└── requirements.txt        # Dependencies
```

## Testing

```bash
python3 tests/test_search_engine.py
```

Verifies:
- Data loading (640 patents)
- Text search functionality
- Patent similarity detection
- Hybrid search with filters
- Risk assessment accuracy