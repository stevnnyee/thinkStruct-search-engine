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
- **Fields Available**: 
  - `claims` - Legal definitions of the invention
  - `abstract` - Summary of the patent
  - `title` - Patent title
  - `detailed_description` - Full technical description
  - `doc_number` - Patent identifier
  - `classification` - Classification codes
- **Data Quality**: 100% field coverage across all patents

## Approach

## Data Loading Verification
```bash
python3 src/data_loader.py
# Output: Successfully loaded 640 patents
# Field Coverage: All fields 100.0%
# DataFrame ready: 640 rows
