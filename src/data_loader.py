import json
import pandas as pd
from pathlib import Path
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)

class PatentDataLoader:
    """
    MISSING FIELD HANDLING STRATEGY:
    Patents with missing critical fields (title, abstract, claims) are EXCLUDED from the dataset.
    Patents with missing non-critical fields (classification, bibtex) are RETAINED.
    This ensures we have searchable text while maximizing dataset size.
    """
    
    def __init__(self, data_dir: str = "data/patent_data_small"):
        self.data_dir = Path(data_dir)
        self.logger = logging.getLogger(__name__)
        
        # Define critical fields needed for search functionality
        self.critical_fields = ['title', 'abstract', 'claims']
        self.optional_fields = ['doc_number', 'detailed_description', 'classification', 'bibtex']
        
    def load_all_patents(self) -> List[Dict]:
        """Load all patent JSON files from the data directory"""
        patents = []
        json_files = list(self.data_dir.glob("patents_ipa*.json"))
        
        if not json_files:
            self.logger.warning(f"No patent files found in {self.data_dir}")
            return patents
            
        for file_path in json_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    batch_patents = json.load(f)
                    patents.extend(batch_patents)
                    self.logger.info(f"Loaded {len(batch_patents)} patents from {file_path.name}")
            except Exception as e:
                self.logger.error(f"Error loading {file_path}: {e}")
                
        self.logger.info(f"Total patents loaded: {len(patents)}")
        return patents
    
    def filter_valid_patents(self, patents: List[Dict]) -> List[Dict]:
        """
        Filter patents based on missing field handling strategy.
        EXCLUDES patents missing critical fields (Title, Abstract, Claims).
        RETAINS patents with missing optional fields.
        """
        valid_patents = []
        excluded_count = 0
        
        for patent in patents:
            # Check if patent has all critical fields with non-empty values
            has_critical_fields = True
            for field in self.critical_fields:
                if field not in patent or not patent[field] or str(patent[field]).strip() == "":
                    has_critical_fields = False
                    break
            
            if has_critical_fields:
                valid_patents.append(patent)
            else:
                excluded_count += 1
        
        self.logger.info(f"Filtered patents: {len(valid_patents)} retained, {excluded_count} excluded due to missing critical fields")
        return valid_patents
    
    def patents_to_dataframe(self, patents: List[Dict]) -> pd.DataFrame:
        """Convert patents list to pandas DataFrame"""
        if not patents:
            return pd.DataFrame()
        return pd.DataFrame(patents)
    
    def analyze_data_structure(self, patents: List[Dict]) -> Dict:
        """Analyze the structure and quality of patent data"""
        if not patents:
            return {"error": "No patents to analyze"}
            
        all_keys = set()
        for patent in patents:
            all_keys.update(patent.keys())
            
        field_coverage = {}
        for key in all_keys:
            # Check for truly empty fields (None, empty string, whitespace only)
            non_empty_count = sum(1 for patent in patents 
                                if key in patent and patent[key] and str(patent[key]).strip())
            field_coverage[key] = non_empty_count / len(patents)
            
        return {
            "total_patents": len(patents),
            "unique_fields": list(all_keys),
            "field_coverage": field_coverage
        }

def test_data_loading():
    """Test the data loading functionality with missing field handling"""
    loader = PatentDataLoader()
    
    # Load raw patents
    raw_patents = loader.load_all_patents()
    
    if raw_patents:
        print(f"Raw patents loaded: {len(raw_patents)}")
        
        # Analyze raw data structure
        raw_analysis = loader.analyze_data_structure(raw_patents)
        print(f"Available fields: {raw_analysis['unique_fields']}")
        
        print("\nRaw Data Field Coverage:")
        for field, coverage in raw_analysis['field_coverage'].items():
            print(f"  {field}: {coverage:.1%}")
        
        # Filter valid patents (handles missing fields according to strategy)
        valid_patents = loader.filter_valid_patents(raw_patents)
        
        if valid_patents:
            print(f"\nValid patents after filtering: {len(valid_patents)}")
            
            # Create DataFrame from filtered patents
            df = loader.patents_to_dataframe(valid_patents)
            print(f"DataFrame ready for search implementation: {len(df)} rows")
            
            # Show final field coverage
            final_analysis = loader.analyze_data_structure(valid_patents)
            print("\nFinal Data Field Coverage:")
            for field, coverage in final_analysis['field_coverage'].items():
                print(f"  {field}: {coverage:.1%}")
        else:
            print("No valid patents remaining after filtering")
    else:
        print("No patents loaded")

if __name__ == "__main__":
    test_data_loading()