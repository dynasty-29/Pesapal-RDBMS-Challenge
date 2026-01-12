# Pesapal RDBMS Feature List & Architecture

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


## Clean Architecture & Microservices Design

                ┌─────────────────────────────────────────────────────────────┐
                │                     PRESENTATION LAYER                       │
                │  ┌──────────────────┐              ┌────────────────────┐  │
                │  │   REPL Client    │              │  Web Frontend      │  │
                │  │   (CLI Tool)     │              │  (React + TS)      │  │
                │  └──────────────────┘              └────────────────────┘  │
                └────────────┬─────────────────────────────────┬──────────────┘
                            │                                 │
                            │ SQL Commands                    │ HTTP/REST
                            │                                 │
                ┌────────────┴─────────────────────────────────┴──────────────┐
                │                     APPLICATION LAYER                        │
                │  ┌──────────────────────────────────────────────────────┐  │
                │  │              API Gateway Service (Flask)              │  │
                │  │  - Routes requests                                    │  │
                │  │  - Authentication/Authorization (future)              │  │
                │  │  - Request validation                                 │  │
                │  └──────────────────────────────────────────────────────┘  │
                └────────────┬─────────────────────────────────────────────────┘
                            │
                            │ Service Calls
                            │
                ┌────────────┴─────────────────────────────────────────────────┐
                │                   DOMAIN/BUSINESS LAYER                      │
                │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
                │  │ Query Service   │  │ Schema Service  │  │ Index       │ │
                │  │                 │  │                 │  │ Service     │ │
                │  │ - Parse SQL     │  │ - Manage schema │  │             │ │
                │  │ - Execute query │  │ - Validate data │  │ - Maintain  │ │
                │  │ - Join logic    │  │ - Constraints   │  │   indexes   │ │
                │  └─────────────────┘  └─────────────────┘  └─────────────┘ │
                └────────────┬─────────────────────────────────────────────────┘
                            │
                            │ Data Operations
                            │
                ┌────────────┴─────────────────────────────────────────────────┐
                │                   INFRASTRUCTURE LAYER                       │
                │  ┌──────────────────────────────────────────────────────┐  │
                │  │              Storage Repository                       │  │
                │  │  - File I/O operations                               │  │
                │  │  - JSON serialization                                │  │
                │  │  - Data persistence                                  │  │
                │  └──────────────────────────────────────────────────────┘  │
                └──────────────────────────────────────────────────────────────┘
                                            │
                                            │ Disk Operations
                                            ▼
                                    ┌───────────────┐
                                    │  File System  │
                                    │  (JSON files) │
                                    └───────────────┘

