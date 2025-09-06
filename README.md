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
   - Copy `.env.example` to `.env` and update the database connection settings:
      ```bash
      cp .env.example .env
      ```
   - Edit `.env` file with your PostgreSQL credentials:
      ```env
      DATABASE_URL=postgresql://postgres:your_password@localhost/SharkTankDB
      ADMIN_API_KEY=your-secure-admin-key-here
      ```

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
   pip install -r requirements.txt

4. **Run FastAPI Development Server**
   - Recommended - wait to do this step until you complete Postgres and PgAdmin4Setup
   - uvicorn main:app --reload
   - Visit http://127.0.0.1:8000/docs to explore the API documentation.

### Load Data
1. I created a Loader functions for each of the tables (sharks, seasons, episodes, and pitches).
   - The `/bulk_load_data` endpoint is now protected with admin authentication
   - Include the `X-Admin-API-Key` header with your admin key when calling this endpoint
   - Example using curl:
     ```bash
     curl -X POST "http://127.0.0.1:8000/bulk_load_data" \
          -H "X-Admin-API-Key: your-secure-admin-key-here"
     ```
2. Happy Coding



### Contributing
Feel free to contribute to this project by opening issues or creating pull requests. For major changes, please open an issue first to discuss the changes.

