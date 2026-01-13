# JDEV26 Pesapal RDBMS challenge

Designing and implementing a simple relational database management system. 

The system should be support for declaring tables with a few column data types, CRUD operations, basic indexing and primary and unique keying and some joining. 

The interface should be SQL or something similar, and it should have an interactive REPL mode.

Demonstrate the use of your RDBMS by writing a trivial web app that requires CRUD to the DB.



## Video Demo
![RDMS DEMo.mp4]

To achieve this i ensured these are core features required for this RDMS
- **Custom SQL Parser** using pyparsing
- **File-based Storage Engine** with JSON persistence
- **Interactive REPL** for direct SQL queries
- **REST API** built with Flask
- **Modern Web UI** built with React + TypeScript
- **Healthcare Management System** as a practical demonstration

## Core Features Checklist
1. Storage Engine

    * File-based JSON storage for tables
    * Persistent data storage
    * Schema metadata management
    * Data integrity on disk writes

2. Data Types Support

    * INTEGER
    * VARCHAR(n) with length validation
    * FLOAT
    * BOOLEAN
    * DATE

3. SQL Operations (DDL)

    * CREATE TABLE with column definitions
    * DROP TABLE
    * Table existence validation

4. SQL Operations (DML - CRUD)

    * INSERT INTO with values
    * SELECT * FROM table
    * SELECT specific columns
    * SELECT with WHERE clause (=, >, <, >=, <=, !=)
    * UPDATE with WHERE clause
    * DELETE with WHERE clause

5. Constraints

    * PRIMARY KEY (unique, not null, one per table)
    * UNIQUE constraint
    * NOT NULL constraint
    * Constraint validation on INSERT/UPDATE

6. Indexing

    * Hash-based index implementation
    * Auto-indexing for PRIMARY KEY
    * Auto-indexing for UNIQUE columns
    * Fast lookup using indexes

7. JOIN Operations

    * INNER JOIN
    * JOIN with ON clause
    * Multi-table SELECT results

8. REPL Interface

    * Interactive SQL prompt
    * Multi-line SQL support
    * Pretty-printed table results
    * Error messages with helpful feedback
    * EXIT/QUIT command
    * Command history

9. Demo Web Application

    * REST API with Flask
    * React TypeScript frontend
    * Full CRUD operations via UI
    * Demonstrates JOIN operations
    * Real-world use case (Healthcare/Appointment System)

10. Testing & Quality

    * Unit tests for core components
    * Integration tests
    * Error handling throughout
    * Input validation



#### To run it locally 

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

### clone the repo
git clone https://github.com/YOUR_USERNAME/pesapal-rdbms.git


### Set Up the Database Engine
        cd database
        python3 -m venv venv
        source venv/bin/activate  
        pip install -e .


### Set Up the Flask API
        cd ../server
        python3 -m venv venv
        source venv/bin/activate  
        pip install -r requirements.txt


#### View on frontend
        cd client
        npm run dev