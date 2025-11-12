### B. Setup Notes for Managed (`setup_notes_managed.md`)

## Cloud & Region

- **Cloud:** Microsoft Azure
- **Region:** Chile Central
- **DBA:** phil
- **Initial Admin User:** phil

## Ordered steps you executed:**

1. I had created a resource named "phil" under Azure Database for MySQL flexible server
2. I had created as per the screen shots  Compute tier "Burstable (1-20 vCores) - Best for workloads that don’t need the full CPU continuously"
3. Set up admin username/password
4. I was able to deploy rather easily with Chile Central region.
5. DB name = phil
6. Use Azure portal  to set up user/db with provided endpoint info
7. .env.example for connection secrets; do not commit real .env.

## Troubles you hit and how you solved them**

1. I had issues with SSL and had written in the notes  along iwith the modified code.
2. I had to reference Perplexity in order to understand the issue .
3. I had to remove  ssl= or ?ssl= part from SQLAlchemy connection string and engine call.

## Start-to-finish elapsed time**

(6.6s) measured by me

Later runs gave me 6.0 s , 6.4 s
