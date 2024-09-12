# FastAPI CSV & JSON Converter API
This repository contains a simple API built using FastAPI that allows for converting CSV files to JSON and vice versa, and stores the parsed data in an SQLite database.

# Features
- Convert CSV files to JSON format
- Convert JSON files to CSV format
- Store parsed data in an SQLite database
- Retrieve stored data using API endpoints
- Data validation with Pydantic
- Dependency injection

# Tech Stack
- **FastAPI** A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **SQLAlchemy ORM**: A powerful and flexible ORM for interacting with SQL databases.
- **SQLite**: A lightweight, disk-based database.
- **Pandas**: A data manipulation library used for CSV and JSON conversions.
- **Pydantic**: A data validation library for Python, used for request validation.
