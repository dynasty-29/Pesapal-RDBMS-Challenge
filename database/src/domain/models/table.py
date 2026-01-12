from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Column:
    """Represents a table column with its properties"""
    name: str
    data_type: str
    max_length: Optional[int] = None
    constraints: List[str] = None
    
    def __post_init__(self):
        if self.constraints is None:
            self.constraints = []

@dataclass
class Table:
    """Represents a database table"""
    name: str
    columns: List[Column]
    rows: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.rows is None:
            self.rows = []
    
    def get_column(self, column_name: str) -> Optional[Column]:
        """Get a column by name"""
        for col in self.columns:
            if col.name == column_name:
                return col
        return None
    
    def has_primary_key(self) -> bool:
        """Check if table has a primary key"""
        for col in self.columns:
            if 'PRIMARY KEY' in col.constraints:
                return True
        return False
    
    def get_primary_key_column(self) -> Optional[Column]:
        """Get the primary key column"""
        for col in self.columns:
            if 'PRIMARY KEY' in col.constraints:
                return col
        return None