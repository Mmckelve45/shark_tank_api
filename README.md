# Shark Tank FastAPI Implementation

This project is a FastAPI implementation of the Shark Tank API. It provides endpoints for querying and managing data related to Shark Tank all the Shark Tank data.

## Table of Contents

- [Setup](#setup)
  - [FastAPI Setup](#fastapi-setup)
  - [PostgreSQL and PgAdmin4 Setup](#postgresql-and-pgadmin4-setup)
  - [Load Data](#load-data)

## Setup

Here is a [video demo](https://youtu.be/pX8suqmkSPE) of the project and high level touch points of the setup.

### PostgreSQL and PgAdmin4 Setup

1. **Install PostgreSQL:**
   - Follow the instructions on the [PostgreSQL official website](https://www.postgresql.org/download/) to install PostgreSQL. 
     - When I did this with Windows, it installed both postgres and pgAdmin4, so you can skip step 2 if it allows you to do so.
2. **Install PgAdmin4:**
   - Follow the instructions on the [PgAdmin4 official website](https://www.pgadmin.org/download/) to install PgAdmin4.
3. **Create a Server in PgAdmin4**
   - Create a server and call it SharkTankServer
   - Under the connection tab
     - Set hostname/address to localhost
     - Set up username and password to access the server (if you already used a password for postgres, use the same one)
4. **Create Database:**
   - Open PgAdmin4 and create a new database called SharkTankDB under the SharkTankServer.
   - On the Definition tab
     - Set encoding to UTF8 if not already set to it.
     - Tablespace to pg_default
     - Locale Provider to lib-c
     - For Mac I set the Locale Provider to icu.
     - For Mac I set the ICU Locale to en-US

5. **Configure Database Connection:**
   - Update the database connection settings in the FastAPI app (app/database.py) with your PostgreSQL database credentials.  I have provided a place for you to alter your SQLALCHEMY_DATABASE_URL with your own connection.
      ```bash
      # ----- Postgres ------ (Best Option for easy setup - Recommended)
      # Load the data with postgres localDB - create a Server/DB in postgres and give it a password
      SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Testme321!@localhost/SharkTankDB'
      engine = create_engine(SQLALCHEMY_DATABASE_URL)

### FastAPI Setup

1. **Clone the Repository:**
   ```bash
   gh repo clone Mmckelve45/shark_tank_api
   cd shark-tank-api

2. **Create a Virtual Environment:**
   - python -m venv fastapienv
   - fastapienv/bin/activate  | On Windows, use `venv\Scripts\activate`

3. **Install Dependencies:**
   ```bash
   pip install uvicorn['standard']
   pip install fastapi
   pip install sqlalchemy
   pip install sqlalchemy-orm
   pip install psycopg2
   pip install pydantic
   pip install starlette
   pip install typing

4. **Run FastAPI Development Server**
   - Recommended - wait to do this step until you complete Postgres and PgAdmin4Setup
   - uvicorn main:app --reload
   - Visit http://127.0.0.1:8000/docs to explore the API documentation.

### Load Data
1. I created a Loader functions for each of the tables (sharks, seasons, episodes, and pitches).
   - At the bottom of the http://127.0.0.1:8000/docs page there is a Bulk Load function that will load all the data from the asset files in one click.
2. Happy Coding



### Contributing
Feel free to contribute to this project by opening issues or creating pull requests. For major changes, please open an issue first to discuss the changes.

