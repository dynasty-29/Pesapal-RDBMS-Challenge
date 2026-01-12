from typing import Dict, Any, List
from ...domain.services.schema_service import SchemaService
from ...domain.services.data_service import DataService
from ..parsers.sql_parser import SQLParser

class QueryExecutor:
    """Executes parsed SQL queries"""
    
    def __init__(self, storage):
        self.storage = storage
        self.schema_service = SchemaService(storage)
        self.data_service = DataService(storage, self.schema_service)
        self.parser = SQLParser()
    
    def execute(self, sql: str) -> Dict[str, Any]:
        """Execute SQL statement and return result"""
        # Parse SQL
        parsed = self.parser.parse(sql)
        
        # Route to appropriate executor
        if parsed['type'] == 'CREATE':
            return self._execute_create(parsed)
        elif parsed['type'] == 'DROP':
            return self._execute_drop(parsed)
        elif parsed['type'] == 'INSERT':
            return self._execute_insert(parsed)
        elif parsed['type'] == 'SELECT':
            return self._execute_select(parsed)
        elif parsed['type'] == 'UPDATE':
            return self._execute_update(parsed)
        elif parsed['type'] == 'DELETE':
            return self._execute_delete(parsed)
    
    def _execute_create(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Execute CREATE TABLE"""
        table = self.schema_service.create_table(
            table_name=parsed['table_name'],
            columns=parsed['columns']
        )
        
        return {
            'success': True,
            'message': f"Table '{parsed['table_name']}' created successfully",
            'affected_rows': 0
        }
    
    def _execute_drop(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Execute DROP TABLE"""
        self.schema_service.drop_table(parsed['table_name'])
        
        return {
            'success': True,
            'message': f"Table '{parsed['table_name']}' dropped successfully",
            'affected_rows': 0
        }
    
    def _execute_insert(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Execute INSERT"""
        # Create row dictionary from columns and values
        row = dict(zip(parsed['columns'], parsed['values']))
        
        self.data_service.insert_row(parsed['table_name'], row)
        
        return {
            'success': True,
            'message': f"1 row inserted into '{parsed['table_name']}'",
            'affected_rows': 1
        }
    
    def _execute_select(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Execute SELECT"""
        # Check if it's a JOIN query
        if 'join' in parsed:
            rows = self.data_service.join_tables(
                left_table_name=parsed['join']['left_table'],
                right_table_name=parsed['join']['right_table'],
                left_column=parsed['join']['left_column'],
                right_column=parsed['join']['right_column'],
                select_columns=parsed['columns']
            )
        else:
            # Build WHERE condition function if present
            where_func = None
            if 'where' in parsed:
                where_func = self._build_where_function(parsed['where'])
            
            rows = self.data_service.select_rows(
                table_name=parsed['table_name'],
                columns=parsed['columns'],
                where_condition=where_func
            )
        
        return {
            'success': True,
            'message': f"{len(rows)} row(s) returned",
            'rows': rows,
            'row_count': len(rows)
        }
    
    def _execute_update(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Execute UPDATE"""
        # Build updates dictionary
        updates = {parsed['set']['column']: parsed['set']['value']}
        
        # Build WHERE condition function if present
        where_func = None
        if 'where' in parsed:
            where_func = self._build_where_function(parsed['where'])
        
        count = self.data_service.update_rows(
            table_name=parsed['table_name'],
            updates=updates,
            where_condition=where_func
        )
        
        return {
            'success': True,
            'message': f"{count} row(s) updated in '{parsed['table_name']}'",
            'affected_rows': count
        }
    
    def _execute_delete(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Execute DELETE"""
        # Build WHERE condition function if present
        where_func = None
        if 'where' in parsed:
            where_func = self._build_where_function(parsed['where'])
        
        count = self.data_service.delete_rows(
            table_name=parsed['table_name'],
            where_condition=where_func
        )
        
        return {
            'success': True,
            'message': f"{count} row(s) deleted from '{parsed['table_name']}'",
            'affected_rows': count
        }
    
    def _build_where_function(self, where_clause: Dict[str, Any]):
        """Build a WHERE condition function from parsed clause"""
        column = where_clause['column']
        operator = where_clause['operator']
        value = where_clause['value']
        
        
        def where_func(row: Dict[str, Any]) -> bool:
            row_value = row.get(column)
            
            # Handle None values
            if row_value is None:
                return False
            
            # Try to convert both values to the same type for comparison
            try:
                # If value is int, try to convert row_value to int
                if isinstance(value, int):
                    row_value = int(row_value)
                # If value is float, try to convert row_value to float
                elif isinstance(value, float):
                    row_value = float(row_value)
            except (ValueError, TypeError):
                pass  # Keep original types if conversion fails
            
            result = False
            if operator == '=':
                result = row_value == value
            elif operator == '!=':
                result = row_value != value
            elif operator == '>':
                result = row_value > value
            elif operator == '<':
                result = row_value < value
            elif operator == '>=':
                result = row_value >= value
            elif operator == '<=':
                result = row_value <= value
            
            return result
        
        return where_func