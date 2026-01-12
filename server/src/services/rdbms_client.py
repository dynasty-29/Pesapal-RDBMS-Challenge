import os
from src.infrastructure.storage.file_storage import FileStorage
from src.application.executors.query_executor import QueryExecutor
from src.domain.exceptions import DatabaseException

class RDBMSClient:
    """Client for interacting with the RDBMS"""
    
    def __init__(self, db_path: str = None):
        """Initialize the RDBMS client"""
        # Set default path relative to this file
        if db_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, '../../../database/db_data')
            db_path = os.path.abspath(db_path)
        
        self.storage = FileStorage(db_path)
        self.storage.initialize_database()
        self.executor = QueryExecutor(self.storage)
    
    def execute_query(self, sql: str):
        """Execute a SQL query and return results"""
        try:
            result = self.executor.execute(sql)
            return {
                'success': True,
                'data': result
            }
        except DatabaseException as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': 'DatabaseException'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': 'UnexpectedException'
            }
    
    def get_all_tables(self):
        """Get list of all tables"""
        try:
            tables = self.storage.list_tables()
            return {
                'success': True,
                'data': tables
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }