from url_tool import UniversalURLTool

db_url = "postgresql://dbuser:dbpass@mydbserver.com:5432/production_db?sslmode=require&timeout=30"
db_tool = UniversalURLTool(db_url)

db_conn_string = db_tool.generate_connection_string(prefix="DB_CONN", include_full_url=False, custom_separator=" | ")
print(f"Database Connection String:\n{db_conn_string}")
# Example Output: DB_CONN_SCHEME=postgresql | DB_CONN_HOST=mydbserver.com | DB_CONN_PORT=5432 | DB_CONN_PATH=/production_db | DB_CONN_QUERY_SSLMODE=require | DB_CONN_QUERY_TIMEOUT=30