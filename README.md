# Calisthenics Tracker API

Backend API for tracking calisthenics exercises, workouts, and progress.

Built as part of a DevOps learning project.

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pytest
- Docker

## Features

- Manage exercises
- Manage workouts
- Track training progress
- REST API with automatic documentation
- Automated tests

## Run the API

Create a virtual environment and install dependencies:

pip install -r requirements.txt

Start the server:

uvicorn src.main:app --reload

API will be available at:

http://localhost:8000

Swagger documentation:

http://localhost:8000/docs

## Run tests

pytest
