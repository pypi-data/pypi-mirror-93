from skidings import *

host = "DB IP/URL"
username = "DB USERNAME"
password = "DB PASSWORD"
database = "DB NAME"
query = "SQL QUERY"

connect = get_sql_data(host,username,password,database,query)

print(connect)

input()