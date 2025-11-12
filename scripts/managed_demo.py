# managed_demo.py — Linear, step-by-step demo for managed MySQL (Azure)
# Run this file top-to-bottom OR run it cell-by-cell in VS Code.
# Prereqs:
#   pip install sqlalchemy pymysql pandas python-dotenv
#
# Env vars (populate a local .env):
#   MAN_DB_HOST, MAN_DB_PORT, MAN_DB_USER, MAN_DB_PASS, MAN_DB_NAME

import os, time
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# --- 0) Load environment ---
# Make sure your .env.example (or .env) contains MAN_DB_HOST, MAN_DB_USER, etc.
load_dotenv(".env.example") 

MAN_DB_HOST = os.getenv("MAN_DB_HOST")
MAN_DB_PORT = os.getenv("MAN_DB_PORT")
MAN_DB_USER = os.getenv("MAN_DB_USER")
MAN_DB_PASS = os.getenv("MAN_DB_PASS")
MAN_DB_NAME = os.getenv("MAN_DB_NAME")

print("[ENV] MAN_DB_HOST:", MAN_DB_HOST)
print("[ENV] MAN_DB_PORT:", MAN_DB_PORT)
print("[ENV] MAN_DB_USER:", MAN_DB_USER)
print("[ENV] MAN_DB_NAME:", MAN_DB_NAME)

# PyMySQL fix: Explicitly set SSL to False using connect_args
# The query parameter '?ssl=false' often leads to errors.
PYMYSQL_NO_SSL_ARGS = {'ssl': False}

# --- 1) Connect to server (no DB) and ensure database exists ---
# Remove the '?ssl=false' query parameter from the URL
server_url = f"mysql+pymysql://{MAN_DB_USER}:{MAN_DB_PASS}@{MAN_DB_HOST}:{MAN_DB_PORT}"

print("[STEP 1] Connecting to Managed MySQL (no DB):", server_url.replace(MAN_DB_PASS, "*****"))
t0 = time.time()

# Pass the SSL configuration directly to connect_args
engine_server = create_engine(
    server_url, 
    pool_pre_ping=True,
    connect_args=PYMYSQL_NO_SSL_ARGS  # <-- FIX APPLIED HERE
)

with engine_server.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{MAN_DB_NAME}`"))
    conn.commit()
print(f"[OK] Ensured database `{MAN_DB_NAME}` exists on managed instance.")

# --- 2) Connect to the target database ---
# Construct the DB URL including the database name
db_url = f"mysql+pymysql://{MAN_DB_USER}:{MAN_DB_PASS}@{MAN_DB_HOST}:{MAN_DB_PORT}/{MAN_DB_NAME}"

# Pass the SSL configuration directly to connect_args
engine = create_engine(
    db_url, 
    pool_pre_ping=True,
    connect_args=PYMYSQL_NO_SSL_ARGS # <-- FIX APPLIED HERE
)

# --- 3) Create a DataFrame and write to a table ---
table_name = "visits"
df = pd.DataFrame(
    [
        {"patient_id": 10, "visit_date": "2025-10-01", "bp_sys": 117, "bp_dia": 75},
        {"patient_id": 11, "visit_date": "2025-10-02", "bp_sys": 131, "bp_dia": 86},
        {"patient_id": 12, "visit_date": "2025-10-03", "bp_sys": 122, "bp_dia": 80},
        {"patient_id": 13, "visit_date": "2025-10-04", "bp_sys": 111, "bp_dia": 71},
        {"patient_id": 14, "visit_date": "2025-10-05", "bp_sys": 126, "bp_dia": 83},
    ]
)
print("[STEP 3] Writing DataFrame to table:", table_name)
with engine.begin() as conn:
    # Use chunksize for efficiency, though not strictly necessary for this small dataframe
    df.to_sql(table_name, con=conn, if_exists="replace", index=False) 
print("[OK] Wrote DataFrame to table.")

# --- 4) Read back a quick check ---
print("[STEP 4] Reading back row count ...")
with engine.connect() as conn:
    count_df = pd.read_sql(f"SELECT COUNT(*) AS n_rows FROM `{table_name}`", con=conn)
print(count_df)

elapsed = time.time() - t0
print(f"[DONE] Managed path completed in {elapsed:.1f}s at {datetime.utcnow().isoformat()}Z")
