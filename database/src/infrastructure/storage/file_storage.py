import json
import os
from typing import Dict, Any, List
from pathlib import Path
from .storage_interface import StorageInterface
from ...domain.exceptions import TableNotFoundException, TableAlreadyExistsException

class FileStorage(StorageInterface):
    """JSON file-based storage implementation"""
    
    def __init__(self, db_path: str = "./db_data"):
        self.db_path = Path(db_path)
        self.schemas_path = self.db_path / "schemas"
        self.tables_path = self.db_path / "tables"
    
    def initialize_database(self, db_path: str = None) -> None:
        """Initialize the database directory structure"""
        if db_path:
            self.db_path = Path(db_path)
            self.schemas_path = self.db_path / "schemas"
            self.tables_path = self.db_path / "tables"
        
        # Create directories if they don't exist
        self.schemas_path.mkdir(parents=True, exist_ok=True)
        self.tables_path.mkdir(parents=True, exist_ok=True)
    
    def save_table_schema(self, table_name: str, schema: Dict[str, Any]) -> None:
        """Save table schema to JSON file"""
        schema_file = self.schemas_path / f"{table_name}.json"
        with open(schema_file, 'w') as f:
            json.dump(schema, f, indent=2)
    
    def load_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Load table schema from JSON file"""
        schema_file = self.schemas_path / f"{table_name}.json"
        if not schema_file.exists():
            raise TableNotFoundException(f"Table '{table_name}' does not exist")
        
        with open(schema_file, 'r') as f:
            return json.load(f)
    
    def table_exists(self, table_name: str) -> bool:
        """Check if table exists"""
        schema_file = self.schemas_path / f"{table_name}.json"
        return schema_file.exists()
    
    def save_table_data(self, table_name: str, rows: List[Dict[str, Any]]) -> None:
        """Save table data to JSON file"""
        if not self.table_exists(table_name):
            raise TableNotFoundException(f"Table '{table_name}' does not exist")
        
        data_file = self.tables_path / f"{table_name}.json"
        with open(data_file, 'w') as f:
            json.dump(rows, f, indent=2)
    
    def load_table_data(self, table_name: str) -> List[Dict[str, Any]]:
        """Load table data from JSON file"""
        if not self.table_exists(table_name):
            raise TableNotFoundException(f"Table '{table_name}' does not exist")
        
        data_file = self.tables_path / f"{table_name}.json"
        if not data_file.exists():
            return []  # Return empty list if data file doesn't exist yet
        
        with open(data_file, 'r') as f:
            return json.load(f)
    
    def delete_table(self, table_name: str) -> None:
        """Delete table schema and data files"""
        if not self.table_exists(table_name):
            raise TableNotFoundException(f"Table '{table_name}' does not exist")
        
        schema_file = self.schemas_path / f"{table_name}.json"
        data_file = self.tables_path / f"{table_name}.json"
        
        schema_file.unlink()  # Delete schema file
        if data_file.exists():
            data_file.unlink()  # Delete data file if exists
    
    def list_tables(self) -> List[str]:
        """List all tables in the database"""
        if not self.schemas_path.exists():
            return []
        
        tables = []
        for schema_file in self.schemas_path.glob("*.json"):
            tables.append(schema_file.stem)  # Get filename without extension
        
        return sorted(tables)