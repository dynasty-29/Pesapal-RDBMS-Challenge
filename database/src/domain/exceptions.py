class DatabaseException(Exception):
    """Base exception for all database errors"""
    pass

class TableNotFoundException(DatabaseException):
    """Raised when a table doesn't exist"""
    pass

class TableAlreadyExistsException(DatabaseException):
    """Raised when trying to create a table that already exists"""
    pass

class ColumnNotFoundException(DatabaseException):
    """Raised when a column doesn't exist"""
    pass

class InvalidDataTypeException(DatabaseException):
    """Raised when an invalid data type is used"""
    pass

class ConstraintViolationException(DatabaseException):
    """Raised when a constraint is violated"""
    pass

class PrimaryKeyViolationException(ConstraintViolationException):
    """Raised when primary key constraint is violated"""
    pass

class UniqueConstraintViolationException(ConstraintViolationException):
    """Raised when unique constraint is violated"""
    pass

class NotNullConstraintViolationException(ConstraintViolationException):
    """Raised when not null constraint is violated"""
    pass

class ParseException(DatabaseException):
    """Raised when SQL parsing fails"""
    pass