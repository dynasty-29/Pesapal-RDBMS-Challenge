import pyparsing as pp
from typing import Dict, Any, List
from ...domain.exceptions import ParseException

class SQLParser:
    """Parser for SQL-like commands"""
    
    def __init__(self):
        # Define SQL keywords (case-insensitive)
        CREATE = pp.CaselessKeyword("CREATE")
        TABLE = pp.CaselessKeyword("TABLE")
        DROP = pp.CaselessKeyword("DROP")
        INSERT = pp.CaselessKeyword("INSERT")
        INTO = pp.CaselessKeyword("INTO")
        VALUES = pp.CaselessKeyword("VALUES")
        SELECT = pp.CaselessKeyword("SELECT")
        FROM = pp.CaselessKeyword("FROM")
        WHERE = pp.CaselessKeyword("WHERE")
        UPDATE = pp.CaselessKeyword("UPDATE")
        SET = pp.CaselessKeyword("SET")
        DELETE = pp.CaselessKeyword("DELETE")
        INNER = pp.CaselessKeyword("INNER")
        JOIN = pp.CaselessKeyword("JOIN")
        ON = pp.CaselessKeyword("ON")
        PRIMARY = pp.CaselessKeyword("PRIMARY")
        KEY = pp.CaselessKeyword("KEY")
        UNIQUE = pp.CaselessKeyword("UNIQUE")
        NOT = pp.CaselessKeyword("NOT")
        NULL = pp.CaselessKeyword("NULL")
        
        # Define basic elements
        identifier = pp.Word(pp.alphas, pp.alphanums + "_")
        integer = pp.Word(pp.nums)
        string = pp.QuotedString("'") | pp.QuotedString('"')
        
        # Data types
        data_type = (
            pp.CaselessKeyword("INTEGER") |
            pp.CaselessKeyword("FLOAT") |
            pp.CaselessKeyword("BOOLEAN") |
            pp.CaselessKeyword("DATE") |
            (pp.CaselessKeyword("VARCHAR") + pp.Suppress("(") + integer("max_length") + pp.Suppress(")"))
        )
        
        # Constraints
        primary_key = PRIMARY + KEY
        not_null = NOT + NULL
        constraint = primary_key | UNIQUE | not_null
        
        # Column definition for CREATE TABLE
        column_def = (
            identifier("name") + 
            data_type("type") + 
            pp.Optional(pp.Group(pp.OneOrMore(constraint))("constraints"))
        )
        
        # CREATE TABLE statement
        create_table = (
            CREATE + TABLE + identifier("table_name") +
            pp.Suppress("(") +
            pp.delimitedList(pp.Group(column_def))("columns") +
            pp.Suppress(")")
        )
        
        # DROP TABLE statement
        drop_table = DROP + TABLE + identifier("table_name")
        
        # INSERT statement
        insert_stmt = (
            INSERT + INTO + identifier("table_name") +
            pp.Suppress("(") + pp.delimitedList(identifier)("columns") + pp.Suppress(")") +
            VALUES +
            pp.Suppress("(") + pp.delimitedList(string | integer)("values") + pp.Suppress(")")
        )
        
        # WHERE clause
        comparison_op = pp.oneOf("= != > < >= <=")
        where_clause = pp.Group(
            pp.Suppress(WHERE) + 
            identifier("column") + 
            comparison_op("operator") + 
            (string | integer)("value")
        )("where")
        
        # Column list with optional table prefix (table.column)
        qualified_column = pp.Combine(identifier + pp.Literal(".") + identifier)
        column_list = pp.delimitedList(qualified_column | identifier) | pp.Literal("*")
        
        select_simple = (
            SELECT + column_list("columns") +
            FROM + identifier("table_name") +
            pp.Optional(where_clause)
        )
        
        join_clause = pp.Group(
            pp.Suppress(INNER) + pp.Suppress(JOIN) + 
            identifier("right_table") +
            pp.Suppress(ON) + 
            identifier("left_table_ref") + pp.Suppress(".") + identifier("left_column") +
            pp.Suppress("=") +
            identifier("right_table_ref") + pp.Suppress(".") + identifier("right_column")
        )("join")
        
        select_join = (
            SELECT + column_list("columns") +
            FROM + identifier("left_table") +
            join_clause
        )
        
        select_stmt = select_join | select_simple
        
        # UPDATE statement
        # set_clause = identifier("column") + pp.Suppress("=") + (string | integer)("value")
        set_clause = pp.Group(
            identifier("column") + pp.Suppress("=") + (string | integer)("value")
        )("set")
        update_stmt = (
            UPDATE + identifier("table_name") +
            SET + set_clause +
            pp.Optional(where_clause)
        )
        
        # DELETE statement
        delete_stmt = (
            DELETE + FROM + identifier("table_name") +
            pp.Optional(where_clause)
        )
        
        # Main SQL statement
        self.sql_statement = (
            create_table("create") |
            drop_table("drop") |
            insert_stmt("insert") |
            select_stmt("select") |
            update_stmt("update") |
            delete_stmt("delete")
        )
    
    def parse(self, sql: str) -> Dict[str, Any]:
        """Parse SQL statement and return structured result"""
        try:
            # Remove trailing semicolon if present
            sql = sql.strip().rstrip(';')
            
            # Parse the SQL
            result = self.sql_statement.parseString(sql, parseAll=True)
            
            # Determine statement type and structure result
            if 'create' in result:
                return self._parse_create(result)
            elif 'drop' in result:
                return self._parse_drop(result)
            elif 'insert' in result:
                return self._parse_insert(result)
            elif 'select' in result:
                return self._parse_select(result)
            elif 'update' in result:
                return self._parse_update(result)
            elif 'delete' in result:
                return self._parse_delete(result)
            else:
                raise ParseException("Unknown statement type")
        
        except pp.ParseException as e:
            raise ParseException(f"Parse error: {str(e)}")
    
    def _parse_create(self, result: pp.ParseResults) -> Dict[str, Any]:
        """Parse CREATE TABLE result"""
        columns = []
        for col in result.columns:
            col_dict = {
                'name': col.name,
                'type': col.type[0] if isinstance(col.type, pp.ParseResults) else col.type,
                'constraints': []
            }
            
            # Handle VARCHAR max_length
            if 'max_length' in col:
                col_dict['max_length'] = int(col.max_length)
            
            # Handle constraints
            if 'constraints' in col:
                for constraint in col.constraints:
                    if len(constraint) == 2 and constraint[0].upper() == 'PRIMARY':
                        col_dict['constraints'].append('PRIMARY KEY')
                    elif len(constraint) == 2 and constraint[0].upper() == 'NOT':
                        col_dict['constraints'].append('NOT NULL')
                    elif constraint.upper() == 'UNIQUE':
                        col_dict['constraints'].append('UNIQUE')
            
            columns.append(col_dict)
        
        return {
            'type': 'CREATE',
            'table_name': result.table_name,
            'columns': columns
        }
    
    def _parse_drop(self, result: pp.ParseResults) -> Dict[str, Any]:
        """Parse DROP TABLE result"""
        return {
            'type': 'DROP',
            'table_name': result.table_name
        }
    
    def _parse_insert(self, result: pp.ParseResults) -> Dict[str, Any]:
        """Parse INSERT result"""
        
        # Convert values to appropriate types
        values = []
        
        # Check if values is callable (a method)
        if callable(result.values):
            values_data = result['values']
        else:
            values_data = result.values
        
        for val in values_data:
            # Convert to proper type
            val_str = str(val)
            
            # Try to convert to int first
            try:
                values.append(int(val_str))
                continue
            except ValueError:
                pass
            
            # Try to convert to float
            try:
                values.append(float(val_str))
                continue
            except ValueError:
                pass
            
            # Keep as string
            values.append(val_str)
        
        return {
            'type': 'INSERT',
            'table_name': str(result.table_name),
            'columns': [str(col) for col in result.columns],
            'values': values
        }
    
    def _parse_select(self, result: pp.ParseResults) -> Dict[str, Any]:
        """Parse SELECT result"""
        parsed = {
            'type': 'SELECT',
            'columns': list(result['columns']) if result['columns'] != '*' else ['*']
        }
        
        # Check if it's a JOIN
        if 'join' in result:
            join_data = result['join']
            parsed['join'] = {
                'left_table': str(result['left_table']),
                'right_table': str(join_data['right_table']),
                'left_column': str(join_data['left_column']),
                'right_column': str(join_data['right_column'])
            }
        else:
            parsed['table_name'] = str(result['table_name'])
        
        # Add WHERE clause if present
        if 'where' in result:
            where_data = result['where']
            parsed['where'] = {
                'column': str(where_data['column']),
                'operator': str(where_data['operator']),
                'value': self._convert_value(where_data['value'])
            }
        
        return parsed
    
    def _parse_update(self, result: pp.ParseResults) -> Dict[str, Any]:
        """Parse UPDATE result"""
        parsed = {
            'type': 'UPDATE',
            'table_name': str(result['table_name']),
            'set': {
                'column': str(result['set']['column']),
                'value': self._convert_value(result['set']['value'])
            }
        }
        
        # Add WHERE clause if present
        if 'where' in result:
            where_data = result['where']
            parsed['where'] = {
                'column': str(where_data['column']),
                'operator': str(where_data['operator']),
                'value': self._convert_value(where_data['value'])
            }
        
        return parsed
    
    def _parse_delete(self, result: pp.ParseResults) -> Dict[str, Any]:
        """Parse DELETE result"""
        parsed = {
            'type': 'DELETE',
            'table_name': str(result['table_name'])
        }
        
        # Add WHERE clause if present
        if 'where' in result:
            where_data = result['where']
            parsed['where'] = {
                'column': str(where_data['column']),
                'operator': str(where_data['operator']),
                'value': self._convert_value(where_data['value'])
            }
        
        return parsed
    
    def _convert_value(self, value: str) -> Any:
        """Convert string value to appropriate type"""
        # Try to convert to int
        try:
            return int(value)
        except ValueError:
            pass
        
        # Try to convert to float
        try:
            return float(value)
        except ValueError:
            pass
        
        # Return as string
        return value