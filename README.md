# Azure SQL: VM vs Managed Project

## Overview - Project summary and goals

This project compares deploying a MySQL database on an Azure Virtual Machine (VM) versus using the Azure Database for MySQL Flexible Server (Managed Service). Python scripts (SQLAlchemy, Pandas) are used for direct data interaction with both services.

- **Self-managed VM:** You provision, configure, and secure a MySQL server instance on an Azure Virtual Machine.
- **Managed Service:** You deploy MySQL using Azure Database for MySQL Flexible Server, leveraging platform automation for setup and maintenance.

## 1. Cloud and region details

- **Azure / Managed / Chile Central**
- **Azure / VM/ Norway East**

## 2. Workflow steps - - Links to all setup notes and evidence

 2–4 minute **recording** (Zoom/Loom link in README) showing:

# Youtube Video recording

[MySQL on VM vs Managed Service (YouTube Video)](https://youtu.be/78j4WsGiqzI)

[![MySQL on VM vs Managed Service](screenshots/vm/Screenshot%202025-11-12%20175029.png)](https://youtu.be/78j4WsGiqzI)

showing

* My repo
* Running each script end-to-end (VM then Managed) and printed results

[Setup Notes for Managed](docs/setup_notes_managed.md)

[Setup Notes for VM](docs/setup_notes_vm.md)

[Comparison Notes for Both](docs/comparison.md)

## 3. Python Scripts With explanation

### A. `vmdemo.py`

1. Imports and Environment Initialization
   from dotenv import load_dotenv: Imports the function to load environment variable values from a .env file.
   import os, time: Imports modules for accessing environment variables (os) and measuring elapsed time (time).
   from datetime import datetime: Imports the class to generate timestamps.
   import pandas as pd: Imports pandas, a data analysis and table-handling library, under the alias pd.
   from sqlalchemy import create_engine, text: Imports functions to connect to SQL databases and execute custom SQL statements.
2. Load Environment Variables
   load_dotenv(): Loads key-value pairs from .env into environment, so credentials and secrets stay out of source code.
3. Set Connection Variables
   VM_DB_USER = os.getenv("VM_DB_USER"): Gets the database user name from the environment.
   VM_DB_PASS = os.getenv("VM_DB_PASS"): Gets the database password from the environment.
   VM_DB_HOST = os.getenv("VM_DB_HOST", "51.120.121.142"): Gets the database server host/IP, or defaults to the public IP if unset.
   VM_DB_PORT = os.getenv("VM_DB_PORT", "3306"): Gets the port for MySQL; defaults to 3306 for MySQL.
   VM_DB_NAME = os.getenv("VM_DB_NAME"): Gets the database name from the env file.
4. Connect to Server and Ensure Database Exists
   server_url = f"mysql+pymysql://{VM_DB_USER}:{VM_DB_PASS}@{VM_DB_HOST}:{VM_DB_PORT}/": Constructs a connection string to MySQL (without specifying database).
5. print("[STEP 1] Connecting to MySQL server (no DB):", server_url.replace(VM_DB_PASS, "*****")): Logs the connection URL, hiding the password for safety.
6. t0 = time.time(): Records the start time for measuring execution duration.
   engine_server = create_engine(server_url, pool_pre_ping=True): Creates an SQLAlchemy engine for connecting to the server. with engine_server.connect() as conn:: Opens a connection context to the server.
7. conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {VM_DB_NAME}")): Runs a SQL command to create the database if it doesn’t exist.
   conn.commit(): Commits the change (creates DB).
   print(f"[OK] Ensured database {VM_DB_NAME} exists."): Reports success.
8. Connect to the Target Database
   db_url = f"mysql+pymysql://{VM_DB_USER}:{VM_DB_PASS}@{VM_DB_HOST}:{VM_DB_PORT}/{VM_DB_NAME}": Constructs the connection string including the database name.
9. engine = create_engine(db_url, pool_pre_ping=True): Instantiates an SQLAlchemy engine for the specific database.
   Create a DataFrame and Write to Table
   table_name = "visits": Sets table name to visits.
   df = pd.DataFrame([...]): Creates a pandas DataFrame from a list of patient visit records.
   df.to_sql(table_name, con=engine, if_exists="replace", index=False): Uploads the DataFrame to the SQL table visits, replacing the table if it already exists.
   Check Data Insertion
   print("[STEP 4] Reading back row count ..."): Prints progress update.
10. with engine.connect() as conn:: Opens connection to the database.
    count_df = pd.read_sql(f"SELECT COUNT(*) AS n_rows FROM {table_name}", con=conn): Runs a SQL query to count rows in the table and loads it into a DataFrame.
    print(count_df): Shows the number of rows written to the table.
    Final Time Report
    elapsed = time.time() - t0: Calculates time elapsed since the start of the workflow.
    print(f"[DONE] VM path completed in {elapsed:.1f}s at {datetime.utcnow().isoformat()}Z"): Prints completion message and UTC timestamp.

### B. `manageddemo.py`

This script demonstrates a step-by-step workflow for connecting to a managed MySQL database , writing data, and verifying the results.

1. Prerequisites and Imports
   Requires installation of the libraries: sqlalchemy, pymysql, pandas, and python-dotenv.
   Imports necessary modules for environment management, timing, date tracking, data manipulation, and database connection.
2. Loading Environment Variables
   Loads database connection details (MAN_DB_HOST, MAN_DB_PORT, MAN_DB_USER, MAN_DB_PASS, MAN_DB_NAME) from .env.example, so I don’t hard-code secrets.
   Prints the key environment variables to verify they are loaded correctly.
3. PyMySQL SSL Configuration
   Sets SSL to False using connect_args for compatibility with managed MySQL; removes the problematic ?ssl=false URL parameter.
4. Connect to Managed MySQL Server
   Creates a connection URL to the MySQL server without specifying a database.
   Connects to the server and ensures the target database exists (using CREATE DATABASE IF NOT EXISTS).
   Outputs the connection status, hiding the password for safety.
5. Connect to the Target Database
   Builds the URL for connecting directly to the database.
   Initializes the SQLAlchemy engine with SSL settings.
6. Write a DataFrame to the Database Table
   Prepares a small DataFrame of sample visit data (patient_id, visit_date, blood pressure measurements).
   Writes the DataFrame to the table named visits, replacing any table of the same name.
7. Verify Data Insertion
   Reads the row count from the visits table to confirm successful data write.
   Displays the verification result.
8. Final Time Report
   Prints the total elapsed time for the workflow, along with the UTC timestamp of completion.

## 4. Environment Variable Example

- `.env`:  for all connection secrets (do NOT commit  `.env`)

I had accidentally committed env.example with actual psw and ip addresses and then realized my mistake.
I then moved the real secrets to .env and deleted .env.example ensuring .env was in gitignore.

The recording was taken with .env example which I had deleted and replaced with .env

## 5. Screenshots/Evidence

### VM and managed instance portal views

- **Managed**
  ![Managed](screenshots/vm/Screenshot%202025-11-12%20153607.png)
- **VM**
  ![VM](screenshots/vm/Screenshot%202025-11-12%20153607.png)

### Firewall/network config (for VM and managed)

- **Managed**

![Managed](screenshots/managed/Screenshot%202025-11-06%20205558.png)

- **VM**

![VM](screenshots/vm/Screenshot%202025-11-12%20153607.png)

### MySQL install/output (CLI or GUI)

- **Managed**

![Managed](screenshots/managed/Screenshot%202025-11-06%20205558.png)

![Managed](screenshots/vm/Screenshot%202025-11-13%20094639.png)

![Managed](screenshots/vm/Screenshot%202025-11-13%20094704.png)

- **VM**

powershell- changing bind address

![VM](screenshots/vm/Screenshot%202025-11-12%20143645.png)

Powershell - sql - showing databases

![VM](screenshots/vm/Screenshot%202025-11-12%20144324.png)

Powershell- sudo updates

![VM](screenshots/vm/Screenshot%202025-11-11%20211143.png)

### Query results from Python scripts (row count, sample table)

- **Managed**

![Managed](screenshots/managed/Screenshot%202025-11-13%20104246.png)

- **VM**

![VM](screenshots/vm/Screenshot%202025-11-13%20104315.png)

### Any troubleshooting/error screens

I had out of memory issues and was forced to increase RAM size. LLM was used to troubleshoot as well.

![VM](screenshots/vm/Screenshot%202025-11-11%20161810.png)

![VM](screenshots/vm/Screenshot%202025-11-11%20161908.png)

Also began getting this error in vscode and with help from stackoverflow
https://stackoverflow.com/questions/71106136/jupyter-extension-for-vscode-on-linux-throws-error-when-doing-anything-jupyter-r
was able to resolve it for now.

![VM](screenshots/vm/Screenshot%202025-11-13%20103225.png)

I also had to spend some time troubleshooting either due to wrong vm user name input or forgotten password.

![VM](screenshots/vm/Screenshot%202025-11-11%20160051.png)

## Further screenshots of steps are in the screenshots folder.
