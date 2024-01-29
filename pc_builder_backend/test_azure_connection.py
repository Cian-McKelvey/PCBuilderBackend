import pyodbc
from constants import AZURE_RELATIONAL_DATABASE_URL

try:
    # Establish connection
    conn = pyodbc.connect(AZURE_RELATIONAL_DATABASE_URL)

    # Connection successful
    print("Connection to Azure SQL Database successful")

    # Optionally, execute a test query
    cursor = conn.cursor()
    cursor.execute("SELECT @@version;")
    row = cursor.fetchone()
    print("SQL Server version:", row[0])

    # Close cursor and connection
    cursor.close()
    conn.close()
except Exception as e:
    # Connection failed
    print("Error connecting to Azure SQL Database:", e)
