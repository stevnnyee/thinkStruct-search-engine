# Patent Search Engine

## Project Overview

**Problem**: Patent attorneys spend days manually searching for similar patents before filing applications.

**Solution**: Automated patent similarity search that finds potential conflicts in seconds.

## What It Does

**Inputs** (as specified in project guidelines):
- Natural language query (e.g., "wireless vehicle sensor")
- Patent ID (e.g., "20240293901")

**Outputs** (as specified in project guidelines):
- Patent metadata (ID, title, similarity score)
- Risk assessment (HIGH/MEDIUM/LOW conflict risk)
- Ranked similar patents

## Quick Start

```bash
# 1. Setup
pip install pandas numpy scikit-learn

# 2. Run demo
python3 src/search_engine.py

# 3. Run tests
python3 tests/test_search_engine.py

# 4. Interactive mode
python3 src/search_engine.py interactive
```

## Example Usage

```bash
# Demo output
Query: 'wireless vehicle sensor'
Results:
  LOW: 20240391278 (0.199) - TWO-WAY TIRE PRESSURE MONITORING SYSTEM
  LOW: 20240278598 (0.193) - WHEEL HUB...
  LOW: 20240239143 (0.191) - SYSTEMS AND METHODS TO SELECTIVELY ACTIVATE TPMS...
```

## Technical Implementation

- **Data**: 640 vehicle patents (2024-present)
- **Algorithm**: TF-IDF vectorization + cosine similarity
- **Focus**: Patent claims (legally binding definitions)
- **Risk Scoring**: >70% = High, 40-70% = Medium, <40% = Low

## Project Structure

```
thinkStruct-search-engine/
├── src/
│   ├── data_loader.py      # Loads patent data
│   └── search_engine.py    # Core search functionality
├── tests/
│   └── test_search_engine.py # Simple tests
├── data/patent_data_small/ # 640 vehicle patents
└── requirements.txt        # Dependencies
```

## Testing

```bash
python3 tests/test_search_engine.py
```

Tests verify:
- Data loading works
- Text search functionality
- Patent similarity detection
- Risk assessment accuracy

---

*Built for ThinkStruct interview - demonstrates patent analysis capabilities*

