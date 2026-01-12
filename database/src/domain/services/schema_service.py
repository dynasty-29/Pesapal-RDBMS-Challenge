from typing import Dict, Any, List
from ..models.table import Table, Column
from ..exceptions import (
    InvalidDataTypeException,
    TableAlreadyExistsException,
    TableNotFoundException,
    NotNullConstraintViolationException,
    UniqueConstraintViolationException,
    PrimaryKeyViolationException
)

class SchemaService:
    """Service for managing table schemas and validation"""
    
    VALID_DATA_TYPES = ['INTEGER', 'VARCHAR', 'FLOAT', 'BOOLEAN', 'DATE']
    
    def __init__(self, storage):
        self.storage = storage
    
    def create_table(self, table_name: str, columns: List[Dict[str, Any]]) -> Table:
        """Create a new table with schema validation"""
        # Check if table already exists
        if self.storage.table_exists(table_name):
            raise TableAlreadyExistsException(f"Table '{table_name}' already exists")
        
        # Validate and create columns
        column_objects = []
        has_primary_key = False
        
        for col_def in columns:
            # Validate data type
            data_type = col_def['type'].upper()
            if data_type not in self.VALID_DATA_TYPES:
                raise InvalidDataTypeException(f"Invalid data type: {col_def['type']}")
            
            # Check for duplicate primary keys
            constraints = col_def.get('constraints', [])
            if 'PRIMARY KEY' in constraints:
                if has_primary_key:
                    raise InvalidDataTypeException("Table can only have one PRIMARY KEY")
                has_primary_key = True
            
            # Create column object
            column = Column(
                name=col_def['name'],
                data_type=data_type,
                max_length=col_def.get('max_length'),
                constraints=constraints
            )
            column_objects.append(column)
        
        # Create table object
        table = Table(name=table_name, columns=column_objects)
        
        # Save schema to storage
        schema = self._table_to_schema(table)
        self.storage.save_table_schema(table_name, schema)
        
        # Initialize empty data file
        self.storage.save_table_data(table_name, [])
        
        return table
    
    def get_table(self, table_name: str) -> Table:
        """Load table from storage"""
        if not self.storage.table_exists(table_name):
            raise TableNotFoundException(f"Table '{table_name}' does not exist")
        
        schema = self.storage.load_table_schema(table_name)
        rows = self.storage.load_table_data(table_name)
        
        return self._schema_to_table(schema, rows)
    
    def drop_table(self, table_name: str) -> None:
        """Delete a table"""
        self.storage.delete_table(table_name)
    
    def list_tables(self) -> List[str]:
        """List all tables"""
        return self.storage.list_tables()
    
    def validate_row(self, table: Table, row: Dict[str, Any]) -> None:
        """Validate a row against table schema"""
        # Check all columns exist
        for col_name in row.keys():
            if not table.get_column(col_name):
                raise InvalidDataTypeException(f"Column '{col_name}' does not exist in table '{table.name}'")
        
        # Validate each column
        for column in table.columns:
            value = row.get(column.name)
            
            # Check NOT NULL constraint
            if 'NOT NULL' in column.constraints and value is None:
                raise NotNullConstraintViolationException(
                    f"Column '{column.name}' cannot be NULL"
                )
            
            # Check PRIMARY KEY constraint (includes NOT NULL)
            if 'PRIMARY KEY' in column.constraints and value is None:
                raise PrimaryKeyViolationException(
                    f"PRIMARY KEY column '{column.name}' cannot be NULL"
                )
            
            # Validate data type if value is not None
            if value is not None:
                self._validate_data_type(column, value)
    
    def _validate_data_type(self, column: Column, value: Any) -> None:
        """Validate value matches column data type"""
        if column.data_type == 'INTEGER':
            if not isinstance(value, int):
                raise InvalidDataTypeException(
                    f"Column '{column.name}' expects INTEGER, got {type(value).__name__}"
                )
        
        elif column.data_type == 'VARCHAR':
            if not isinstance(value, str):
                raise InvalidDataTypeException(
                    f"Column '{column.name}' expects VARCHAR, got {type(value).__name__}"
                )
            if column.max_length and len(value) > column.max_length:
                raise InvalidDataTypeException(
                    f"Column '{column.name}' max length is {column.max_length}, got {len(value)}"
                )
        
        elif column.data_type == 'FLOAT':
            if not isinstance(value, (int, float)):
                raise InvalidDataTypeException(
                    f"Column '{column.name}' expects FLOAT, got {type(value).__name__}"
                )
        
        elif column.data_type == 'BOOLEAN':
            if not isinstance(value, bool):
                raise InvalidDataTypeException(
                    f"Column '{column.name}' expects BOOLEAN, got {type(value).__name__}"
                )
        
        elif column.data_type == 'DATE':
            if not isinstance(value, str):
                raise InvalidDataTypeException(
                    f"Column '{column.name}' expects DATE string, got {type(value).__name__}"
                )
            # TODO: Add date format validation
    
    def _table_to_schema(self, table: Table) -> Dict[str, Any]:
        """Convert Table object to schema dictionary"""
        return {
            'name': table.name,
            'columns': [
                {
                    'name': col.name,
                    'type': col.data_type,
                    'max_length': col.max_length,
                    'constraints': col.constraints
                }
                for col in table.columns
            ]
        }
    
    def _schema_to_table(self, schema: Dict[str, Any], rows: List[Dict[str, Any]]) -> Table:
        """Convert schema dictionary to Table object"""
        columns = [
            Column(
                name=col['name'],
                data_type=col['type'],
                max_length=col.get('max_length'),
                constraints=col.get('constraints', [])
            )
            for col in schema['columns']
        ]
        
        return Table(name=schema['name'], columns=columns, rows=rows)