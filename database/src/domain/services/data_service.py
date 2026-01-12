from typing import Dict, Any, List, Callable
from ..models.table import Table
from ..exceptions import (
    PrimaryKeyViolationException,
    UniqueConstraintViolationException
)

class DataService:
    """Service for managing table data operations"""
    
    def __init__(self, storage, schema_service):
        self.storage = storage
        self.schema_service = schema_service
    
    def insert_row(self, table_name: str, row: Dict[str, Any]) -> None:
        """Insert a new row into table"""
        # Load table
        table = self.schema_service.get_table(table_name)
        
        # Validate row against schema
        self.schema_service.validate_row(table, row)
        
        # Check PRIMARY KEY uniqueness
        pk_column = table.get_primary_key_column()
        if pk_column and row.get(pk_column.name) is not None:
            for existing_row in table.rows:
                if existing_row.get(pk_column.name) == row.get(pk_column.name):
                    raise PrimaryKeyViolationException(
                        f"PRIMARY KEY violation: value '{row.get(pk_column.name)}' already exists"
                    )
        
        # Check UNIQUE constraints
        for column in table.columns:
            if 'UNIQUE' in column.constraints and row.get(column.name) is not None:
                for existing_row in table.rows:
                    if existing_row.get(column.name) == row.get(column.name):
                        raise UniqueConstraintViolationException(
                            f"UNIQUE constraint violation on column '{column.name}'"
                        )
        
        # Add row to table
        table.rows.append(row)
        
        # Save to storage
        self.storage.save_table_data(table_name, table.rows)
    
    def select_rows(self, table_name: str, columns: List[str] = None, 
                   where_condition: Callable = None) -> List[Dict[str, Any]]:
        """Select rows from table with optional filtering"""
        # Load table
        table = self.schema_service.get_table(table_name)
        
        # Apply WHERE condition if provided
        if where_condition:
            filtered_rows = [row for row in table.rows if where_condition(row)]
        else:
            filtered_rows = table.rows
        
        # Select specific columns if provided
        if columns and columns != ['*']:
            result = []
            for row in filtered_rows:
                selected_row = {col: row.get(col) for col in columns if col in row}
                result.append(selected_row)
            return result
        
        return filtered_rows
    
    def update_rows(self, table_name: str, updates: Dict[str, Any], 
                   where_condition: Callable = None) -> int:
        """Update rows in table"""
        # Load table
        table = self.schema_service.get_table(table_name)
        
        updated_count = 0
        
        for i, row in enumerate(table.rows):
            # Check if row matches WHERE condition
            if where_condition is None or where_condition(row):
                # Create updated row
                updated_row = row.copy()
                updated_row.update(updates)
                
                # Validate updated row
                self.schema_service.validate_row(table, updated_row)
                
                # Check PRIMARY KEY uniqueness (if PK is being updated)
                pk_column = table.get_primary_key_column()
                if pk_column and pk_column.name in updates:
                    for j, existing_row in enumerate(table.rows):
                        if i != j and existing_row.get(pk_column.name) == updated_row.get(pk_column.name):
                            raise PrimaryKeyViolationException(
                                f"PRIMARY KEY violation: value '{updated_row.get(pk_column.name)}' already exists"
                            )
                
                # Check UNIQUE constraints (if unique column is being updated)
                for column in table.columns:
                    if 'UNIQUE' in column.constraints and column.name in updates:
                        for j, existing_row in enumerate(table.rows):
                            if i != j and existing_row.get(column.name) == updated_row.get(column.name):
                                raise UniqueConstraintViolationException(
                                    f"UNIQUE constraint violation on column '{column.name}'"
                                )
                
                # Apply update
                table.rows[i] = updated_row
                updated_count += 1
        
        # Save to storage
        self.storage.save_table_data(table_name, table.rows)
        
        return updated_count
    
    def delete_rows(self, table_name: str, where_condition: Callable = None) -> int:
        """Delete rows from table"""
        # Load table
        table = self.schema_service.get_table(table_name)
        
        original_count = len(table.rows)
        
        # Filter out rows that match the WHERE condition
        if where_condition:
            table.rows = [row for row in table.rows if not where_condition(row)]
        else:
            table.rows = []
        
        deleted_count = original_count - len(table.rows)
        
        # Save to storage
        self.storage.save_table_data(table_name, table.rows)
        
        return deleted_count
    
    def join_tables(self, left_table_name: str, right_table_name: str,
                   left_column: str, right_column: str,
                   select_columns: List[str] = None) -> List[Dict[str, Any]]:
        """Perform INNER JOIN between two tables"""
        # Load both tables
        left_table = self.schema_service.get_table(left_table_name)
        right_table = self.schema_service.get_table(right_table_name)
        
        result = []
        
        # Nested loop join
        for left_row in left_table.rows:
            for right_row in right_table.rows:
                # Check join condition
                if left_row.get(left_column) == right_row.get(right_column):
                    # Combine rows with table prefixes
                    joined_row = {}
                    
                    # Add left table columns with prefix
                    for key, value in left_row.items():
                        joined_row[f"{left_table_name}.{key}"] = value
                    
                    # Add right table columns with prefix
                    for key, value in right_row.items():
                        joined_row[f"{right_table_name}.{key}"] = value
                    
                    # Select specific columns if provided
                    if select_columns and select_columns != ['*']:
                        selected_row = {col: joined_row.get(col) for col in select_columns}
                        result.append(selected_row)
                    else:
                        result.append(joined_row)
        
        return result