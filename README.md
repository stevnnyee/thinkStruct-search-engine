# Patent Search Engine

## Problem Statement
The goal is to build a search engine that applies search techniques to patent claims and descriptions within patent filings, improving how relevant information is found and compared.

## Installation

### Prerequisites
- Python 3.8+ (tested with Python 3.12)
- pip package manager

### Setup
1. Clone the repository:
```bash
git clone https://github.com/stevnnyee/thinkStruct-search-engine.git
cd thinkStruct-search-engine


## Data Overview
- **Dataset**: Vehicle patent applications (2024-present)
- **Size**: 640 patents loaded successfully
- **File Pattern**: patents_ipa*.json (10 patents per file)

- **Fields Available**: 
  - `claims` - Legal definitions of the invention
  - `abstract` - Summary of the patent
  - `title` - Patent title
  - `detailed_description` - Full technical description
  - `doc_number` - Patent identifier
  - `classification` - Classification codes
  - `bibtex` - Citation information
  - `filename` - Source file reference
- **Data Quality**: 
  - 100% field coverage across all patents
  - Missing Data: None detected
  - Data Integrity: All 640 patents have complete information


## Approach

## Data Loading Verification
```bash
python3 src/data_loader.py
# INFO: Total patents loaded: 640
# Filtered patents: 640 retained, 0 excluded due to missing critical fields
# DataFrame ready for search implementation: 640 rows
# Final Data Field Coverage: All fields 100.0%


## Part 1: Core Search Implementation

### Technical Decisions
1. **Primary Text Field**: [Claims/Abstract] - chosen because...
2. **Search Algorithm**: TF-IDF with [specific enhancement] - rationale...
3. **Preprocessing Approach**: [conservative/aggressive] - patent considerations...

### Key Insights Discovered
- Patent text differs from web content because...
- Main challenges for patent search are...
- Quality vs speed trade-off manifests as...

### Performance Baseline
- Average search time: X seconds
- Vocabulary size: Y terms
- Result relevance: [qualitative assessment]