import pyodbc

def _conn():
    conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=DELL;"
                        "Database=DATA_IMPACTA;"
                        "Trusted_Connection=yes;")
    
