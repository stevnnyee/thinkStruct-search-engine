import json
import pandas as pd
from pathlib import Path
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)

class PatentDataLoader:
    def __init__(self, data_dir: str = "data/patent_data_small"):
        self.data_dir = Path(data_dir)
        self.logger = logging.getLogger(__name__)
        
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
    """Test the data loading functionality"""
    loader = PatentDataLoader()
    patents = loader.load_all_patents()
    
    if patents:
        print(f"Successfully loaded {len(patents)} patents")
        analysis = loader.analyze_data_structure(patents)
        print(f"Available fields: {analysis['unique_fields']}")
        
        # Show field coverage to check data quality
        print("Field Coverage:")
        for field, coverage in analysis['field_coverage'].items():
            print(f"  {field}: {coverage:.1%}")
            
        df = loader.patents_to_dataframe(patents)
        print(f"DataFrame ready: {len(df)} rows")
    else:
        print("No patents loaded")

if __name__ == "__main__":
    test_data_loading()