# Shark Tank FastAPI Implementation

This project is a FastAPI implementation of the Shark Tank API. It provides endpoints for querying and managing data related to Shark Tank all the Shark Tank data.

## Table of Contents

- [Setup](#setup)
  - [FastAPI Setup](#fastapi-setup)
  - [PostgreSQL and PgAdmin4 Setup](#postgresql-and-pgadmin4-setup)
  - [Load Data](#load-data)

## Setup

### PostgreSQL and PgAdmin4 Setup

1. **Install PostgreSQL:**
Follow the instructions on the [PostgreSQL official website](https://www.postgresql.org/download/) to install PostgreSQL.

2. **Install PgAdmin4:**
Follow the instructions on the [PgAdmin4 official website](https://www.pgadmin.org/download/) to install PgAdmin4.

3. **Create Database:**
Open PgAdmin4 and create a new database for the Shark Tank API.

4. **Configure Database Connection:**
Update the database connection settings in the FastAPI app (app/database.py) with your PostgreSQL database credentials.  I have provided a place for you to alter your SQLALCHEMY_DATABASE_URL with your own connection.
   ```bash
   # ----- Postgres ------ (Best Option for easy setup - Recommended)
   # Load the data with postgres localDB - create a Server/DB in postgres and give it a password
   SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Testme321!@localhost/SharkTankDB'
   engine = create_engine(SQLALCHEMY_DATABASE_URL)

### FastAPI Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/shark-tank-fastapi.git
   cd shark-tank-fastapi

2. **Create a Virtual Environment:**
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install Dependencies:**
pip install -r requirements.txt

4. **Run FastAPI Development Server**
uvicorn main:app --reload
Visit http://127.0.0.1:8000/docs to explore the API documentation.

