from abc import ABC, abstractmethod
from typing import Dict, Any, List

class StorageInterface(ABC):
    """Abstract interface for storage implementations"""
    
    @abstractmethod
    def initialize_database(self, db_path: str) -> None:
        """Initialize the database storage"""
        pass
    
    @abstractmethod
    def save_table_schema(self, table_name: str, schema: Dict[str, Any]) -> None:
        """Save table schema to storage"""
        pass
    
    @abstractmethod
    def load_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Load table schema from storage"""
        pass
    
    @abstractmethod
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists"""
        pass
    
    @abstractmethod
    def save_table_data(self, table_name: str, rows: List[Dict[str, Any]]) -> None:
        """Save table data to storage"""
        pass
    
    @abstractmethod
    def load_table_data(self, table_name: str) -> List[Dict[str, Any]]:
        """Load table data from storage"""
        pass
    
    @abstractmethod
    def delete_table(self, table_name: str) -> None:
        """Delete a table from storage"""
        pass
    
    @abstractmethod
    def list_tables(self) -> List[str]:
        """List all tables in the database"""
        pass