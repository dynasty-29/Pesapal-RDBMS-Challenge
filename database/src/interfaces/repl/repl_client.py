import sys
from tabulate import tabulate
from ...infrastructure.storage.file_storage import FileStorage
from ...application.executors.query_executor import QueryExecutor
from ...domain.exceptions import DatabaseException
from typing import Dict, Any

class REPLClient:
    """Interactive REPL for database operations"""
    
    def __init__(self, db_path: str = "./db_data"):
        self.storage = FileStorage(db_path)
        self.storage.initialize_database()
        self.executor = QueryExecutor(self.storage)
        self.running = False
    
    def start(self):
        """Start the REPL"""
        self.running = True
        
        print("=" * 60)
        print("Pesapal RDBMS - Interactive SQL Shell")
        print("=" * 60)
        print("Type your SQL commands. Type 'EXIT' or 'QUIT' to exit.")
        print("Type 'HELP' for available commands.")
        print("=" * 60)
        print()
        
        while self.running:
            try:
                # Read SQL command (support multi-line)
                sql = self._read_sql()
                sql = sql.rstrip(';').strip()
                
                if not sql:
                    continue
                
                # Check for exit commands
                if sql.upper() in ['EXIT', 'QUIT']:
                    print("Goodbye!")
                    break
                
                # Check for help command
                if sql.upper() == 'HELP':
                    self._show_help()
                    continue
                
                # Check for list tables command
                if sql.upper() == 'SHOW TABLES':
                    self._show_tables()
                    continue
                
                # Execute SQL
                result = self.executor.execute(sql)
                
                # Display result
                self._display_result(result)
            
            except DatabaseException as e:
                print(f"Error: {e}")
                print()
            
            except KeyboardInterrupt:
                print("\nUse EXIT or QUIT to exit.")
                print()
            
            except Exception as e:
                print(f"Unexpected error: {e}")
                print()
    
    def _read_sql(self) -> str:
        """Read SQL command (supports multi-line)"""
        lines = []
        prompt = "sql> "
        
        while True:
            try:
                line = input(prompt).strip()
                
                if not line:
                    if lines:
                        # Empty line after some input, continue reading
                        prompt = "...> "
                        continue
                    else:
                        # Empty line with no input, return empty
                        return ""
                
                lines.append(line)
                
                # Check if command is complete (ends with semicolon)
                if line.endswith(';'):
                    return ' '.join(lines)
                
                # Continue reading on next line
                prompt = "...> "
            
            except EOFError:
                return ""
    
    def _display_result(self, result: Dict[str, Any]):
        """Display query result"""
        if 'rows' in result:
            # SELECT query - display as table
            rows = result['rows']
            
            if not rows:
                print("No rows returned.")
            else:
                # Extract headers from first row
                headers = list(rows[0].keys())
                
                # Extract values
                table_data = [[row.get(col) for col in headers] for row in rows]
                
                # Print table
                print(tabulate(table_data, headers=headers, tablefmt='grid'))
            
            print(f"\n{result['message']}")
        else:
            # DDL or DML query - display message
            print(result['message'])
        
        print()
    
    def _show_help(self):
        """Show help information"""
        help_text = """
Available Commands:
-------------------

DDL Commands:
  CREATE TABLE table_name (column1 TYPE constraints, column2 TYPE, ...);
  DROP TABLE table_name;

DML Commands:
  INSERT INTO table_name (col1, col2, ...) VALUES (val1, val2, ...);
  SELECT * FROM table_name;
  SELECT col1, col2 FROM table_name WHERE column = value;
  UPDATE table_name SET column = value WHERE column = value;
  DELETE FROM table_name WHERE column = value;

JOIN:
  SELECT col1, col2 FROM table1 INNER JOIN table2 ON table1.col = table2.col;

Data Types:
  INTEGER, VARCHAR(n), FLOAT, BOOLEAN, DATE

Constraints:
  PRIMARY KEY, UNIQUE, NOT NULL

Special Commands:
  SHOW TABLES  - List all tables
  HELP         - Show this help
  EXIT / QUIT  - Exit the REPL

Examples:
---------
CREATE TABLE users (id INTEGER PRIMARY KEY, name VARCHAR(100) NOT NULL);
INSERT INTO users (id, name) VALUES (1, 'Alice');
SELECT * FROM users;
UPDATE users SET name = 'Bob' WHERE id = 1;
DELETE FROM users WHERE id = 1;
"""
        print(help_text)
    
    def _show_tables(self):
        """Show all tables in database"""
        tables = self.storage.list_tables()
        
        if not tables:
            print("No tables found.")
        else:
            print("Tables:")
            for table in tables:
                print(f"  - {table}")
        
        print()

def main():
    """Main entry point for REPL"""
    # Check for custom database path
    db_path = "./db_data"
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    
    repl = REPLClient(db_path)
    repl.start()

if __name__ == '__main__':
    main()